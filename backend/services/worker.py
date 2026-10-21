"""Single local worker. Start explicitly after approved external-service configuration."""
import asyncio
import fcntl
import os
import time
from sqlalchemy import select, update
from backend.db import ROOT, make_engine, session_factory
from backend.models.entities import SimulationRun, now
from backend.adapters.mirofish import MiroFishAdapter, MiroFishConfig, SimulationError


async def process(factory, run_id, adapter):
    with factory() as db:
        run = db.get(SimulationRun, run_id)
        if not run or run.status != "QUEUED":
            return
        claim = db.execute(update(SimulationRun).where(SimulationRun.id == run_id, SimulationRun.status == "QUEUED").values(status="RUNNING", updated_at=now()))
        if claim.rowcount != 1:
            return
        scenario = run.scenario
        db.commit()
    start = time.monotonic()

    def progress(provenance):
        with factory() as db:
            run = db.get(SimulationRun, run_id)
            run.provenance = provenance
            run.updated_at = now()
            db.commit()

    def cancelled():
        with factory() as db:
            return db.get(SimulationRun, run_id).cancel_requested

    try:
        report, provenance, elapsed = await adapter.run(scenario, progress, cancelled)
        with factory() as db:
            run = db.get(SimulationRun, run_id)
            if run.cancel_requested:
                run.status = "CANCELLED"
                run.error = "Cancelled before report publication; inspect upstream for completed artifacts."
            else:
                run.status, run.report, run.provenance = "COMPLETED", report, provenance
            run.elapsed_seconds, run.updated_at = elapsed, now()
            # Upstream exposes no reliable aggregate token count; preserve NULL.
            db.commit()
    except SimulationError as exc:
        with factory() as db:
            run = db.get(SimulationRun, run_id)
            run.status = exc.code if exc.code in {"CANCELLED", "TIMEOUT", "UNAVAILABLE", "RATE_LIMITED"} else "FAILED"
            run.error, run.elapsed_seconds, run.updated_at = str(exc), round(time.monotonic() - start), now()
            db.commit()
    except Exception:
        with factory() as db:
            run = db.get(SimulationRun, run_id)
            run.status, run.error, run.updated_at = "FAILED", "Worker error. Inspect local logs; no report was fabricated or automatically retried.", now()
            db.commit()
        raise


async def main():
    if os.getenv("MIROFISH_ALLOW_EXTERNAL", "false").lower() != "true" or not os.getenv("MIROFISH_BASE_URL"):
        raise SystemExit("External execution is disabled. Configure approved services before starting this worker.")
    factory = session_factory(make_engine())
    # Advisory lock prevents multiple workers in this local MVP.
    lock = open(ROOT / "data/runtime/simulation-worker.lock", "w")
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    with factory() as db:
        for run in db.scalars(select(SimulationRun).where(SimulationRun.status.in_(["RUNNING", "CANCEL_REQUESTED"]))):
            run.status = "INTERRUPTED"
            run.error = "Worker restarted. Upstream tasks may remain active; inspect saved provenance. No automatic paid replay."
        db.commit()
    adapter = MiroFishAdapter(MiroFishConfig(base_url=os.environ["MIROFISH_BASE_URL"], allow_external=True,
        job_timeout=float(os.getenv("MIROFISH_JOB_TIMEOUT", "600"))))
    try:
        while True:
            with factory() as db:
                id = db.scalar(select(SimulationRun.id).where(SimulationRun.status == "QUEUED").order_by(SimulationRun.created_at).limit(1))
            if id:
                await process(factory, id, adapter)
            else:
                await asyncio.sleep(2)
    finally:
        await adapter.close()
        lock.close()


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
    asyncio.run(main())
