# Replit verification - 23 October 2026

Workspace: [https://replit.com/@jeremyjunxuanta/orbyte-decisionos](https://replit.com/@jeremyjunxuanta/orbyte-decisionos). Imported from the source ZIP based on local commit `ef2db83`. Public synthetic demo: [https://orbyte-decisionos--jeremyjunxuanta.replit.app/](https://orbyte-decisionos--jeremyjunxuanta.replit.app/), published on the free Starter plan on 24 October 2026.

## Actual results

- Python 3.12.12, Node 24.22.1 and installed Chromium 152.0.7977.64.
- Production build passed; 33 backend tests, three component tests and TypeScript checks passed.
- Four Playwright tests passed in 1.0 minute: approval/persistence, rejection, unavailable simulation and mobile navigation.
- Native browser created decision `e4dc959a-2ce6-4ea4-adcc-e6307028f737`, approved Supplier B for RM660, and retained PO `B65F9B8C` and audit events after reload.
- Screenshots: `docs/screenshots/replit-workspace.jpg`, `replit-approved-workflow.jpg`, `replit-test-results.jpg`. Team-named proof PDF: `submission/SDC2026_Us!_Replit_POU.pdf`.

## Reproduce

1. Import the source into a Replit Python 3.12 / Node 24 workspace. ZIP import does not preserve Git history; the local Git bundle does.
2. Run `bash scripts/replit_setup.sh`. The script uses `pip install --no-user` because Replit's pip user-install default conflicts with a virtual environment.
3. Press Run. The UI uses port 3000 and the API stays on loopback port 8000. Paid simulation execution is forced off.
4. Run `.venv/bin/python -m pytest backend/tests -q`, then `pnpm --dir frontend typecheck` and `pnpm --dir frontend test` using the installed `.tools/node_modules/.bin/pnpm`.
5. Replit's bundled Playwright Chromium lacked `libglib-2.0.so.0`. Use its installed browser explicitly:

```bash
PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/repl/tools/bin/chromium .tools/node_modules/.bin/pnpm --dir frontend test:e2e
```

The test harness forces an isolated SQLite configuration before ASGI imports, avoiding Replit's injected PostgreSQL URL. Tests use separate ports 8001/3001 and a temporary database. Default CI continues to use Playwright's own Chromium unless the executable override is explicitly set.

Logs were retained in the Replit workspace as `docs/replit-unit-results.txt` and `docs/replit-e2e-results.txt`. Replit Agent automatically began inspecting the import; it was stopped after 16 seconds / five actions. Setup and verification were then performed manually through the shell and UI with Codex.

The development preview may sleep and is not the public link. After explicitly pinning safe `anyio`, `certifi`, `idna` and `Pygments` versions in `backend/requirements.txt`, Replit's fresh security scan reported **0 active issues** and its publish security checks passed. An unauthenticated HTTP request to the published URL returned 200. The public browser loaded the dashboard, created synthetic decision `d0081965-6656-4a55-8f2e-fef3460ebe9e`, approved Supplier B as the simulated owner, produced draft `PO-63D4B847`, and retained approval and draft after reload. No supplier message, payment or stock receipt occurred. The service uses shared synthetic data; anyone with the URL can choose a simulated role and change it. The free-plan deployment warns it will expire after 29 days unless upgraded; no upgrade or payment was made. The organiser Core voucher remains expired and eligibility needs organiser clarification.
