# Verification record

Executed locally on macOS during 21–22 October 2026 MYT, using Python 3.12.14 and Node.js 24.19.0. Commands below assume repository root unless stated otherwise. Results are observed checks, not planned pass claims.

| Check | Command | Actual result |
|---|---|---|
| Backend/rules/API/adapter/worker | `.venv/bin/python -m pytest backend/tests -q` | **33 passed**, one Starlette TestClient/httpx deprecation warning |
| Frontend types | `cd frontend && pnpm typecheck` | Passed |
| Frontend components | `cd frontend && pnpm test` | **3 passed** |
| Production bundle | `cd frontend && NEXT_TELEMETRY_DISABLED=1 pnpm build` | Passed |
| Automated browser suite | `cd frontend && pnpm test:e2e` | Attempted; **4 tests blocked at Chromium launch**, no E2E pass claimed |
| Native browser interaction | Codex in-app browser against running production UI/API | Checks below completed |
| GitHub CI | `.github/workflows/ci.yml` | Authored only; not run or pushed |

The initial frontend commands used the bundled Node executable directly; subsequent pnpm commands passed after configuring workspace build permissions. An initial Turbopack file-watcher error was addressed by using Webpack/polling for local E2E servers. The final production rebuild also hit a sandbox port-binding restriction in Turbopack; the build script now uses `next build --webpack`, which completed successfully. Chromium then exited before opening a test page because macOS denied its Mach-port bootstrap registration (`bootstrap_check_in ... MachPortRendezvousServer`). This is the current runner blocker. No browser test assertion results can be inferred from that failure.

## Automated coverage

Backend tests cover stock coverage/rounding and exact quote totals, threshold boundary, zero usage, invalid/NaN input, role restrictions and unknown identities, approval/rejection/cancellation, explicit risk acknowledgment, input version conflicts and stale quote/lead-time snapshots, active-decision deduplication, idempotency payload matching, simultaneous approval attempts, injected PO-write failure rollback and persistence after application restart.

Adapter/worker tests cover disabled external execution, missing/invalid credentials, rate limits, network errors, HTTP and overall timeouts, malformed envelopes, incomplete/mismatched reports, local destination validation, mocked full lifecycle, best-effort stop, cancellation and persisted worker failures. Test narratives are fixtures, not genuine reports.

Component tests check cost/risk presentation, selection callbacks and disabled actions. Four Playwright tests target the full approval journey, rejection, unavailable simulation, and mobile navigation/overflow. They use an isolated temporary database on API port 8001 and UI port 3001; ordinary demo history on ports 8000/3000 is preserved.

## Native browser checks actually completed

1. Opened the running production dashboard and triggered the milk inventory check.
2. Verified 1.5-day coverage, RM570/RM660 totals, RM90 premium and 2.5-day late-delivery gap.
3. Confirmed manager approval was disabled; selected Business owner and Supplier B, entered a reason and approved.
4. Observed an actual synthetic PO draft for RM660 with approval and PO audit events. Reload retained the draft and removed approval controls. Decision ID: `3a714d27-96f5-40a4-a7c4-eaf05d4c95dd`.
5. Requested simulation availability. A persistent `UNAVAILABLE` request showed no completed report, no generated insights, runtime Not measured and tokens Not reported. Request ID: `39f498ff` (prefix).
6. At a 390×844 viewport, opened navigation and visited Operations. Heading was visible; document width 375px was within the 390px viewport. Inventory table scrolls within its container. Desktop document width was also within the 1440px viewport.
7. Created a new request and rejected it with a reason. The UI reported no order generated, displayed REJECTED and saved the rejection audit. Decision ID: `066d5408-b950-4b7c-9c9d-e015a3158769`.

8. Restarted both servers after the final build. The rejected decision retained its audit and correct terminal progress label; the earlier approved decision retained the RM660 draft, audit and selected Supplier B. No warnings/errors were returned by the browser log query for this final page.

These are agent-driven checks through the native browser, using accessible controls/keyboard activation. They are separate from the blocked Playwright runner and are not a broad cross-browser or accessibility certification. Screenshot evidence is in `docs/screenshots/`. No paid external service was needed.

## Reproduce

Use README setup, then the commands above. For Playwright, install Chromium first with `pnpm exec playwright install chromium` (Linux CI uses `--with-deps`). CI keeps external execution disabled. Run the suite in an environment that permits Chromium; don't mark it passing until actual assertions finish successfully.

For future live MiroFish validation, follow `MIROFISH.md` and retain genuine upstream identifiers, complete report, elapsed time and provider usage. Current contract-test success does not establish live compatibility.
