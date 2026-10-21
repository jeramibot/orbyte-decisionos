"""Original HTTP adapter, inspected against MiroFish 7657031. No upstream code imports.

Contract tests use a mocked HTTP transport. A genuine paid-service run remains unverified.
"""
import asyncio
import json
import re
import time
from dataclasses import dataclass
from typing import Callable
from urllib.parse import urlparse
import httpx
from pydantic import BaseModel, ConfigDict, StrictBool, ValidationError
from backend.schemas.contracts import DecisionInsights

PINNED_COMMIT = "7657031ac01184afe2cb220f5ee3545573b5e843"


class SimulationError(Exception):
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


class Envelope(BaseModel):
    model_config = ConfigDict(extra="ignore")
    success: StrictBool
    data: dict | None = None


@dataclass(frozen=True)
class MiroFishConfig:
    base_url: str = "http://127.0.0.1:5001"
    allow_external: bool = False
    request_timeout: float = 90
    job_timeout: float = 600
    poll_interval: float = 2


class MiroFishAdapter:
    def __init__(self, config: MiroFishConfig, transport=None):
        self.config = config
        parsed = urlparse(config.base_url)
        if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"} or parsed.username or parsed.password:
            raise ValueError("MiroFish must be a separate local HTTP service; remote service URLs are not enabled")
        self.client = httpx.AsyncClient(base_url=config.base_url, timeout=config.request_timeout,
            transport=transport, follow_redirects=False, trust_env=False)

    async def close(self):
        await self.client.aclose()

    async def request(self, method, path, **kwargs):
        if not self.config.allow_external:
            raise SimulationError("UNAVAILABLE", "External execution is disabled. Approve and configure LLM/Zep services first.")
        try:
            response = await self.client.request(method, path, **kwargs)
            if response.status_code == 429:
                raise SimulationError("RATE_LIMITED", "Upstream provider usage limit reached. No automatic paid retry was attempted.")
            if response.status_code in {401, 403}:
                raise SimulationError("CREDENTIALS", "Upstream credentials are missing, invalid or unauthorised.")
            response.raise_for_status()
            value = Envelope.model_validate(response.json())
            if not value.success:
                raise SimulationError("UPSTREAM_FAILED", "MiroFish reported a failure. Check its local logs and provider configuration.")
            if value.data is None:
                raise SimulationError("INVALID_RESPONSE", "MiroFish response omitted its data object.")
            return value.data
        except httpx.TimeoutException as exc:
            raise SimulationError("TIMEOUT", "MiroFish request timed out; no report was generated here.") from exc
        except httpx.HTTPStatusError as exc:
            raise SimulationError("UPSTREAM_HTTP", f"MiroFish returned HTTP {exc.response.status_code}; inspect its local logs.") from exc
        except httpx.RequestError as exc:
            raise SimulationError("UNAVAILABLE", "Cannot reach the configured local MiroFish service.") from exc
        except (ValueError, ValidationError) as exc:
            raise SimulationError("INVALID_RESPONSE", "Unexpected MiroFish response format.") from exc

    @staticmethod
    def identifier(data, field):
        value = data.get(field)
        if not isinstance(value, str) or not re.fullmatch(r"[a-zA-Z0-9_-]{1,150}", value):
            raise SimulationError("INVALID_RESPONSE", f"Upstream response has no valid {field}.")
        return value

    async def create_scenario(self, scenario):
        document = json.dumps(scenario, ensure_ascii=False, indent=2)
        return await self.request("POST", "/api/graph/ontology/generate", data={
            "simulation_requirement": scenario["question"] + "\nUse the requested report sections. Hypothetical reactions only, never numerical forecasts.",
            "project_name": "DecisionOS synthetic café scenario", "additional_context": "All records and stakeholders are fictional."},
            files={"files": ("synthetic-scenario.txt", document.encode(), "text/plain")})

    async def prepare_agents(self, project_id):
        created = await self.request("POST", "/api/simulation/create", json={"project_id": project_id, "enable_twitter": True, "enable_reddit": False})
        return created

    async def start_simulation(self, simulation_id, rounds):
        return await self.request("POST", "/api/simulation/start", json={"simulation_id": simulation_id,
            "platform": "twitter", "max_rounds": rounds, "enable_graph_memory_update": False, "force": False})

    async def get_simulation_status(self, simulation_id):
        return await self.request("GET", f"/api/simulation/{simulation_id}/run-status")

    async def get_simulation_report(self, simulation_id):
        report = await self.request("GET", f"/api/report/by-simulation/{simulation_id}")
        if report.get("status") != "completed" or not isinstance(report.get("markdown_content"), str) or not report["markdown_content"].strip():
            raise SimulationError("INCOMPLETE_REPORT", "MiroFish has not returned a nonempty completed report.")
        if report.get("simulation_id") != simulation_id:
            raise SimulationError("INVALID_RESPONSE", "Report provenance does not match the requested simulation.")
        self.identifier(report, "report_id")
        return report

    async def cancel_simulation(self, simulation_id):
        return await self.request("POST", "/api/simulation/stop", json={"simulation_id": simulation_id})

    async def run(self, scenario, progress: Callable[[dict], None], cancelled: Callable[[], bool]):
        provenance = {"upstream_commit": PINNED_COMMIT, "genuine_completed_run": False,
            "seed_input_token_estimate": len(json.dumps(scenario)) // 4,
            "token_estimate_scope": "Rough English seed-text chars/4 only; excludes graph, profiles, rounds and report calls."}
        start = time.monotonic()

        def check():
            if cancelled():
                raise SimulationError("CANCELLED", "Owner requested cancellation. Graph/preparation calls may continue upstream.")
            if time.monotonic() - start > self.config.job_timeout:
                raise SimulationError("TIMEOUT", "Simulation exceeded the configured job time limit.")

        async def poll(method, path, payload=None, field="status", complete=("completed", "ready")):
            while True:
                check()
                result = await self.request(method, path, **({"json": payload} if payload is not None else {}))
                state = result.get(field)
                if state in complete:
                    return result
                if state in {"failed", "error", "stopped", "cancelled"}:
                    raise SimulationError("FAILED", "MiroFish terminated without a successful complete run.")
                if not isinstance(state, str):
                    raise SimulationError("INVALID_RESPONSE", "Upstream progress response omitted status.")
                await asyncio.sleep(self.config.poll_interval)

        try:
            # The outer timeout also covers a single long graph/LLM request.
            async with asyncio.timeout(self.config.job_timeout):
                check()
                created = await self.create_scenario(scenario)
                project_id = self.identifier(created, "project_id")
                provenance.update(project_id=project_id, stage="BUILDING_GRAPH"); progress(provenance.copy())
                graph = await self.request("POST", "/api/graph/build", json={"project_id": project_id, "graph_name": "DecisionOS synthetic SME"})
                task_id = self.identifier(graph, "task_id")
                await poll("GET", f"/api/graph/task/{task_id}")
                project = await self.request("GET", f"/api/graph/project/{project_id}")
                provenance["graph_id"] = self.identifier(project, "graph_id")
                check()
                simulation = await self.prepare_agents(project_id)
                simulation_id = self.identifier(simulation, "simulation_id")
                provenance.update(simulation_id=simulation_id, stage="PREPARING_AGENTS"); progress(provenance.copy())
                prep = await self.request("POST", "/api/simulation/prepare", json={"simulation_id": simulation_id,
                    "use_llm_for_profiles": False, "parallel_profile_count": 2})
                if prep.get("status") != "ready":
                    await poll("POST", "/api/simulation/prepare/status", {"simulation_id": simulation_id, "task_id": self.identifier(prep, "task_id")})
                check()
                await self.start_simulation(simulation_id, scenario["rounds"])
                provenance["stage"] = "SIMULATING"; progress(provenance.copy())
                await poll("GET", f"/api/simulation/{simulation_id}/run-status", field="runner_status", complete=("completed",))
                check()
                generated = await self.request("POST", "/api/report/generate", json={"simulation_id": simulation_id, "force_regenerate": False})
                provenance["stage"] = "GENERATING_REPORT"; progress(provenance.copy())
                if generated.get("status") != "completed":
                    await poll("POST", "/api/report/generate/status", {"simulation_id": simulation_id, "task_id": self.identifier(generated, "task_id")})
                report = await self.get_simulation_report(simulation_id)
                check()
                provenance.update(report_id=report["report_id"], genuine_completed_run=True, stage="COMPLETED")
                return structure_report(report, scenario), provenance, round(time.monotonic() - start)
        except TimeoutError as exc:
            await self._stop_best_effort(provenance, progress)
            raise SimulationError("TIMEOUT", "Job time limit reached. Check upstream for any still-running graph/report tasks.") from exc
        except SimulationError:
            await self._stop_best_effort(provenance, progress)
            raise

    async def _stop_best_effort(self, provenance, progress):
        if provenance.get("simulation_id"):
            try:
                await self.cancel_simulation(provenance["simulation_id"])
                provenance["stop_requested"] = True
            except SimulationError:
                provenance["stop_requested"] = False
            progress(provenance.copy())


def structure_report(report, scenario):
    """Extract only existing named sections; never invent missing insights."""
    sections = {}
    heading = None
    for line in report["markdown_content"].splitlines():
        if line.startswith("#"):
            heading = line.lstrip("# ").lower().strip()
            sections.setdefault(heading, [])
        elif heading and line.strip():
            sections[heading].append(line.strip().lstrip("-* "))
    return DecisionInsights(assumptions=scenario["assumptions"],
        stakeholder_reactions=sections.get("stakeholder reactions", []), risks=sections.get("risks", []),
        mitigations=sections.get("mitigations", []), missing_information=sections.get("missing information", []),
        limitations=sections.get("limitations", []) + ["Hypothetical agent narratives are not validated forecasts.",
            "Missing or differently named report sections are left empty; consult the original narrative."],
        source_run_id=report["simulation_id"], report_id=report["report_id"], narrative=report["markdown_content"]).model_dump()
