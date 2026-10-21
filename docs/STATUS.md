# Implementation checklist

- [x] M0: workspace, Domain 2 and upstream source inspection
- [x] M1: deterministic backend and persistence tests
- [ ] M2: connected Next.js UI
- [ ] M3: approval → PO → audit, end-to-end test
- [ ] M4: adapter contracts and unavailable mode; genuine run needs approved credentials
- [ ] M5: narrow scenario template (no fabricated outcomes)
- [ ] M6: runnable scripts, verification, demo and limitations

## Milestone 1 verification
Created backend models, validated request schemas, pure rules engine, mock hub connector, procurement service and FastAPI routes.
Command: `.venv/bin/python -m pytest backend/tests -q` — **16 passed**.
Includes injected database failure rollback, concurrent approval, stale offers, role checks and restart persistence.
One dependency deprecation warning from Starlette TestClient/httpx; no test failures.
Next: connect frontend and run browser workflow. No live MiroFish run.
