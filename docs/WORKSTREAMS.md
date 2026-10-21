# Team workstreams and task specifications

The supplied prompt names six workstreams; the reviewed competition rules allow **at most five registered team members**. Combine workstreams 1 and 6 if needed; do not add an unregistered contributor. No GitHub issues have been posted and no remote branches pushed.

| Workstream / proposed branch | Owned files | Acceptance criteria |
|---|---|---|
| 1. Architecture/integration · `feat/integration` | `docs/ARCHITECTURE.md`, `docs/API.md`, OpenAPI, connector contract | Contracts agreed before cross-module changes; complete connected journey |
| 2. Frontend · `feat/frontend` | `frontend/app`, `frontend/components`, `frontend/lib` | Responsive screens, clear errors and loading, role-aware controls, component tests |
| 3. Backend/data · `feat/backend` | `backend/api`, `backend/models`, `backend/db.py`, `backend/schemas` | Tenant-scoped requests, atomic transactions, validation and persistent snapshots |
| 4. Simulations · `feat/mirofish` | `backend/adapters/mirofish.py`, `backend/services/worker.py`, `simulation/` | Pin source, contract tests, error handling; genuine approved run before claiming live integration |
| 5. Rules/data · `feat/rules` | `backend/services/rules.py`, `seed.py`, `scenarios.py`, `data/synthetic/` | Decimal calculations, RM570/RM660/RM90 example; no ungrounded forecasts |
| 6. QA/DevOps · `feat/verification` | `backend/tests`, `frontend/tests`, `scripts/`, `.github/`, demo docs | Fresh install, end-to-end approval/audit, failure and restart tests; truthful results |

Use small feature branches and pull requests with the problem, behaviour change and actual tests. Avoid concurrent edits to shared schemas; agree changes in API.md/OpenAPI first. Keep commits genuine and incremental. A local Git repository was created during this authorised build; nothing is pushed. Stop commits at the hackathon deadline unless organisers authorise further work.

## Outstanding task specifications
1. **Approved MiroFish live validation** — set up the pinned separate service, verify provider credentials/budget, run one two-round synthetic scenario, retain actual run IDs and report, measure elapsed time and provider token usage. Acceptance: no mocked report is presented as genuine.
2. **Replit proof** — import the real project into the team's Replit workspace, confirm runtime and record genuine usage. Acceptance: functioning deployed/access link or organiser-accepted project/history evidence. Public deployment needs user approval.
3. **Submission assembly** — complete team details, official proposal/declaration PDFs, slides and 5–7 minute video. Acceptance: accessible links, honest tool/AI disclosures, real proof PDFs and committee access, deadline freeze.
4. **SME usability validation** — ask an authorised tester to complete the synthetic workflow, record time and errors, compare with a declared manual baseline. Acceptance: observations are genuine; estimates are labelled.
