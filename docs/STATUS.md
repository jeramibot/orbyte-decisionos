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
- **M6:** `README.md`, `docs/`, `scripts/`, `.github/workflows/ci.yml`, `submission/README.md`. Playwright: four tests passed in Replit; the earlier macOS launch attempt was blocked. CI is authored but unrun; this is not a passing CI claim.

See [detailed test results](TESTING.md) for commands and boundaries. An empty private GitHub repository exists, but no code was pushed. Anonymous requests to the Replit workspace and old development-preview URL returned 404 on 24 October, so judge access is not verified. No production service was published, no live MiroFish simulation occurred and no real procurement was performed.

## Next work

1. Complete GitHub sign-in, push the locally prepared history to the authorised private repository and verify the separate CI run; Replit browser tests already pass. The user approved a private push, but the CLI is not authenticated yet.
2. Resolve judge access: check Replit Starter publishing availability and settings, then publish only with the required approval and verify the resulting URL while signed out. The current development links return 404 anonymously.
3. Ask the organisers to reactivate the expired Replit Core voucher or clarify in writing whether verified free-plan Replit use is eligible. Obtain the designated committee GitHub usernames.
4. Have the registered team review the private PDFs and deck, add verified links, and have Pau personally sign and date the declarations. The user is handling the 5–7 minute video. Submit the final materials through the official portal and retain confirmation.
5. Optional after the required preliminary submission is ready: replace the masked Zep dashboard value with a valid full key, then validate one small synthetic MiroFish run within the chosen provider limits. No live result is currently claimed.

## Submission preparation — 23 October

Both official template PDFs have technical answers and appendices. The user confirmed a two-person registered roster and completion of the mandatory workshops; private review copies include leader contact details outside this repository. Public draft copies retain placeholders, and leader review/signatures remain pending. All 34 pages were rendered and visually reviewed; narrative word limits and overlay bounds passed. The nine-slide PowerPoint passed package/layout/font/native-table checks and artifact-runtime re-import; each slide was visually checked. This does not establish native PowerPoint rendering.

Replit import, setup, production build and all 40 tests (33 backend, 3 component, 4 browser) are verified. A synthetic approval and reload check passed in the hosted development preview. The setup/test harness now handles Replit pip and injected-database defaults. Small Gemini API verification calls succeeded, but the saved Zep value is masked and invalid; no live MiroFish simulation occurred. No remote Git push, production publication or final submission occurred.
