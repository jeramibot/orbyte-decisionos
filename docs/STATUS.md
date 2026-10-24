# Implementation status — 24 October 2026 MYT

| Milestone | Actual state |
|---|---|
| M0 — inspection and contracts | Complete: environment, Domain 2 requirements, MiroFish source/licence/routes, architecture and OpenAPI |
| M1 — operational backend | Complete: SQLite seed, rules, snapshots, lifecycle, roles, idempotent/atomic approval, PO draft and audit |
| M2 — connected frontend | Complete: eight requested routes, responsive interface, editable assumptions and clear errors |
| M3 — approved action | Working and checked in native browser, including reload persistence and rejection. All four Playwright tests passed in Replit with installed Chromium 152; the macOS runner remains restricted |
| M4 — MiroFish | Adapter, persistent worker, error handling and report viewer implemented; mocked contracts pass. Pinned upstream backend and 133 dependencies installed separately; entrypoint preflight correctly stops at missing LLM/Zep keys. **Live execution and usage measurement incomplete**, requiring approved credentials/budget |
| M5 — strategic prototype | Menu-price scenario configuration implemented; no generated outcome without genuine upstream execution |
| M6 — readiness | Local launcher, Replit import configuration, setup, demo script, architecture, tests, screenshots, draft official PDFs and a nine-slide editable deck prepared. **Actual competition submission remains incomplete** |

## Milestone evidence

- **M1:** `backend/models`, `schemas`, `services`, `api` and mock connector. Initial `.venv/bin/python -m pytest backend/tests -q`: 16 passed. Includes concurrent approval, stale data, injected write failure rollback and database-restart persistence.
- **M2/M3:** `frontend/app`, `components`, `lib`, component tests and `tests/e2e`. Typecheck, 3 component tests and production build passed. Browser workflow created a real local synthetic RM660 draft with audit events; reload retained it. A separate rejection created no draft. Native mobile navigation worked at 390px without page-level horizontal overflow.
- **M4/M5:** `backend/adapters/mirofish.py`, `services/worker.py`, 17 additional adapter/worker tests, pinned-source record and scenario templates. Combined backend suite: **33 passed**, one dependency deprecation warning. Unavailable requests persist without invented insights. No genuine simulation report exists.
- **M6:** `README.md`, `docs/`, `scripts/`, `.github/workflows/ci.yml`, `submission/README.md`. Playwright: four tests passed in Replit; the earlier macOS launch attempt was blocked. [Latest tested GitHub CI passed](https://github.com/jeramibot/orbyte-decisionos/actions/runs/40105180876), including its browser suite. Pytest was updated to 9.1.1; resolved safe transitive dependencies were pinned explicitly; all 33 backend tests passed locally.

See [detailed test results](TESTING.md) for commands and boundaries. The code and genuine local history were pushed to the public [GitHub repository](https://github.com/jeramibot/orbyte-decisionos); anonymous access returned HTTP 200. The [public Replit synthetic demo](https://orbyte-decisionos--jeremyjunxuanta.replit.app/) is live. Replit's fresh scan reported 0 active issues and publication passed its security checks after safe dependency pins were made explicit. An anonymous HTTP request returned 200; the public browser completed inventory check, owner approval, draft `PO-63D4B847` and reload persistence. No live MiroFish simulation or real procurement occurred.

## Next work

1. Ask the organisers to reactivate the expired Replit Core voucher or clarify in writing whether verified free-plan Replit use is eligible. Obtain the designated committee GitHub usernames and invite them after verifying their identities.
2. Have the registered team review the private PDFs and deck, add the verified public link, and have Pau personally sign and date the declarations. The user is handling the 5–7 minute video. Submit the final materials through the official portal and retain confirmation.
3. Optional after the required preliminary submission is ready: replace the masked Zep dashboard value with a valid full key, then validate one small synthetic MiroFish run within the chosen provider limits. No live result is currently claimed.

## Submission preparation — 23 October

Both official template PDFs have technical answers and appendices. The user confirmed a two-person registered roster and completion of the mandatory workshops; private review copies include leader contact details outside this repository. Public draft copies retain placeholders, and leader review/signatures remain pending. All 34 pages were rendered and visually reviewed; narrative word limits and overlay bounds passed. The nine-slide PowerPoint passed package/layout/font/native-table checks and artifact-runtime re-import; each slide was visually checked. This does not establish native PowerPoint rendering.

Replit import, setup, production build and all 40 tests (33 backend, 3 component, 4 browser) are verified. A synthetic approval and reload check passed in the hosted development preview and again on the public deployment. The setup/test harness handles Replit pip and injected-database defaults. GitHub CI passed. Small Gemini API verification calls succeeded, but the saved Zep value is masked and invalid; no live MiroFish simulation occurred. Final submission has not occurred.
