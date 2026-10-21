# Implementation status — 22 October 2026 MYT

| Milestone | Actual state |
|---|---|
| M0 — inspection and contracts | Complete: environment, Domain 2 requirements, MiroFish source/licence/routes, architecture and OpenAPI |
| M1 — operational backend | Complete: SQLite seed, rules, snapshots, lifecycle, roles, idempotent/atomic approval, PO draft and audit |
| M2 — connected frontend | Complete: eight requested routes, responsive interface, editable assumptions and clear errors |
| M3 — approved action | Working and checked in native browser, including reload persistence and rejection. Automated Playwright test suite exists but its local runner is blocked before Chromium startup |
| M4 — MiroFish | Adapter, persistent worker, error handling and report viewer implemented; mocked contracts pass. **Live service setup/run and usage measurement incomplete**, requiring approved credentials/budget |
| M5 — strategic prototype | Menu-price scenario configuration implemented; no generated outcome without genuine upstream execution |
| M6 — readiness | Local launcher, setup, demo script, architecture, tests, screenshots and limitations documented. **Actual competition submission remains incomplete** |

## Milestone evidence

- **M1:** `backend/models`, `schemas`, `services`, `api` and mock connector. Initial `.venv/bin/python -m pytest backend/tests -q`: 16 passed. Includes concurrent approval, stale data, injected write failure rollback and database-restart persistence.
- **M2/M3:** `frontend/app`, `components`, `lib`, component tests and `tests/e2e`. Typecheck, 3 component tests and production build passed. Browser workflow created a real local synthetic RM660 draft with audit events; reload retained it. A separate rejection created no draft. Native mobile navigation worked at 390px without page-level horizontal overflow.
- **M4/M5:** `backend/adapters/mirofish.py`, `services/worker.py`, 17 additional adapter/worker tests, pinned-source record and scenario templates. Combined backend suite: **33 passed**, one dependency deprecation warning. Unavailable requests persist without invented insights. No genuine simulation report exists.
- **M6:** `README.md`, `docs/`, `scripts/`, `.github/workflows/ci.yml`, `submission/README.md`. Playwright attempted: four tests blocked at browser launch by the macOS sandbox. CI is authored but unrun; this is not a passing CI claim.

See [detailed test results](TESTING.md) for commands and boundaries. No remote repository was pushed, no public service deployed, no paid API invoked and no real procurement performed.

## Next work

1. Run the committed Playwright suite in a browser-capable environment/authorised CI; resolve any actual test failures.
2. Complete registered-team review and genuine Replit usage/evidence, then assemble official PDFs, slides and 5–7 minute video.
3. After approved provider setup/budget, validate the pinned MiroFish integration with one real small run and actual runtime/usage evidence.
4. Authorise remote repository/public submission separately and verify organiser handles, links and deadline freeze.
