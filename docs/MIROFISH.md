# Optional MiroFish integration

## Verified scope

Inspected upstream README, licence, package/setup scripts, Python dependencies, route implementations and simulation lifecycle at commit **7657031ac01184afe2cb220f5ee3545573b5e843** of [666ghj/MiroFish](https://github.com/666ghj/MiroFish/tree/7657031ac01184afe2cb220f5ee3545573b5e843). The pin is recorded in `simulation/mirofish.lock.json` and adapter provenance. HTTP contract tests use mocked responses. **No actual MiroFish simulation, provider credential validation, live latency measurement or aggregate token measurement has been completed.** This is a source-inspected integration pin, not a live-tested compatibility claim.

Upstream creates social-agent environments using CAMEL/OASIS. Our owner, purchasing manager, supplier, delivery coordinator and customer group are fictional perspectives mapped into that environment. This is exploratory narrative, not a calibrated business forecast. Five seed perspectives do not guarantee exactly five extracted agents.

## Lifecycle verified from route source

| Stage | HTTP operation |
|---|---|
| Upload synthetic scenario and infer ontology | `POST /api/graph/ontology/generate`, multipart `files`, `simulation_requirement`, `project_name`, `additional_context` |
| Build knowledge graph | `POST /api/graph/build`, then `GET /api/graph/task/{task_id}` |
| Retrieve graph identifier | `GET /api/graph/project/{project_id}` |
| Create environment | `POST /api/simulation/create` |
| Prepare agents/config | `POST /api/simulation/prepare`, then **POST** `/api/simulation/prepare/status` |
| Start bounded rounds | `POST /api/simulation/start` |
| Poll execution | `GET /api/simulation/{simulation_id}/run-status`, field `runner_status` |
| Generate report | `POST /api/report/generate`, then **POST** `/api/report/generate/status` |
| Retrieve completed report | `GET /api/report/by-simulation/{simulation_id}` |
| Request simulation stop | `POST /api/simulation/stop` |

The POST status methods above follow actual route decorators; a source docstring saying GET is not the contract. The adapter validates success envelopes, identifiers, terminal status, nonempty narrative and matching simulation provenance. It extracts only existing named report sections. Missing/differently named sections remain empty; the original narrative is retained.

DecisionOS stores requests in SQLite. Start a separate single worker only after approved configuration. It claims queued jobs, records stages and IDs, and publishes completed reports. Restarted jobs become `INTERRUPTED`, with no automatic paid replay. UI polling reads local status. HTTP requests have a 90-second timeout and jobs default to 600 seconds. Errors and provider rate limits are persisted; no synthetic report substitutes for failure.

## Separate-service setup after approval

Do not run paid providers until the owner approves the provider, synthetic data transfer and budget. No upstream install script was executed during this build.

1. Obtain the exact pinned upstream source in a separate checkout/environment. Reinspect its setup scripts before running them; do not put upstream source into this Apache repository.
2. Use upstream-supported Python **3.11 or 3.12**. Inspected pinned dependencies include `zep-cloud==3.25.0`, `camel-oasis==0.2.5`, `camel-ai==0.2.78`, Flask, Flask-CORS and an OpenAI-compatible client. Upstream setup uses npm for its frontend and `uv sync` for its backend. Follow the pinned README's startup instructions and bind the backend to loopback.
3. Configure upstream `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL_NAME` and `ZEP_API_KEY` in that service's ignored `.env`. Choose a provider/model available to the team; the inspected upstream default is not a statement that the team owns an account or quota. Optional boost-model settings also require explicit cost awareness.
4. Confirm the upstream service is reachable locally at the chosen port. The DecisionOS adapter accepts only local HTTP destinations and does not follow redirects.
5. After approval, set DecisionOS `MIROFISH_BASE_URL` and `MIROFISH_ALLOW_EXTERNAL=true` in its root `.env`. Restart the API through `scripts/dev.py`, which loads that file. Start the worker in a separate terminal from the repository root:

   ```bash
   .venv/bin/python -m backend.services.worker
   ```

6. As the demo owner, request one delivery-delay scenario. Inspect persisted stage/source IDs, upstream logs and the provider dashboard. Stop and investigate failures before retrying.

API connection status is deliberately `CONFIGURED_UNVERIFIED` when enabled; configuration alone does not prove service health. The current launcher does not automatically start MiroFish or its worker.

## Small-run configuration and cost uncertainty

The UI requests one platform (Twitter), two rounds, five fictional seed perspectives, no LLM-generated profiles and no simulation graph-memory update. Backend schemas cap rounds at three. Ontology, graph extraction, preparation, simulation and report generation may still make multiple paid calls. Additional graph entities may become agents. This is **not a hard token or monetary cap**.

No reliable aggregate token-usage field was found in the inspected run/report API. `token_usage` therefore stays null, shown as **Not reported**. Provenance includes a rough seed-text characters/4 estimate labelled as seed-only; it is not the total run cost. Use actual provider usage records for a genuine run. Runtime is measured only when a worker executes a job; unavailable requests show **Not measured**.

Cancellation and timeout request a best-effort simulation stop once a simulation ID exists. Graph preparation or report generation may continue upstream, and stop failure is recorded. Check upstream/provider activity; elapsed-time limits do not guarantee billing stops.

## Required live evidence before claiming success

- Record actual upstream commit, provider/model, region where applicable, round count and extracted agent count.
- Complete one genuine two-round run and retain project, graph, simulation and report IDs.
- Save the unedited report, assumptions and provenance under `simulation/reports/` only after reviewing for secrets/data. Mark any replay as a recorded genuine run.
- Record wall-clock runtime and actual provider token/cost totals, or explicitly state unavailable fields.
- Verify cancel/error behaviour against the real service, and confirm procurement still works with it offline.
- Update the integration pin's verification status only after those checks pass.

## Licensing

MiroFish is AGPL-3.0. Its licence is preserved at `docs/licenses/MiroFish-AGPL-3.0.txt`; links and scope are in `LICENSES.md`. HTTP/process separation is an architectural boundary, not a legal guarantee that all obligations disappear. Review source/distribution/network-use obligations before any external deployment. Original DecisionOS code remains separately licensed under Apache-2.0.
