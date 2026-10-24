# Judge-access handoff

As of 24 October 2026, unauthenticated requests to the Replit workspace URL and the previously recorded `sisko.replit.dev` development-preview URL return HTTP 404. Screenshots prove the team used Replit, but neither URL is presently a verified judge-accessible prototype. The code is now in a private GitHub repository, which is not accessible to unauthenticated judges.

Replit's public pricing page currently advertises one live published project on the Starter plan: https://replit.com/pricing . This is a plan description, not a verified entitlement or successful publication for this account. The organiser flyer provided by the user separately says Replit **Core redemption** is required for judging and deposit refund; the user reports the voucher expired. Ask the organisers for reactivation or written clarification. A free-plan deployment alone does not establish eligibility under that flyer.

## Publication preparation

1. Confirm the account still owns the `orbyte-decisionos` Replit workspace and the current ZIP import. Keep the app synthetic; do not add real supplier, customer, payment or procurement records.
2. Build with `bash scripts/replit_setup.sh`; use `.venv/bin/python scripts/replit_run.py` as the launch command and expose only port 3000. The launcher forces `MIROFISH_ALLOW_EXTERNAL=false`, uses SQLite in `data/runtime`, and keeps FastAPI on loopback port 8000. This configuration worked in the authenticated development preview; published-app build/runtime settings remain unverified.
3. Review the publishing screen's access setting, build/run commands, region, quota and price before publishing. `X-Demo-User` is only a simulated role selector: any visitor can choose the demo owner and change the shared synthetic data. Do not present it as real authentication. Publishing is an explicit user-approved step under `AGENTS.md`.
4. After publication, check the public URL while signed out. Verify dashboard, inventory check, decision approval, PO draft and reload persistence with synthetic data; record the public URL, date and screenshot. If any step fails, do not mark it as a functional deployed prototype.
5. Replace the draft technical declaration's Live Prototype URL field, update README and the submission portal, and have Pau review/sign after all links and compliance boxes are accurate.

The fallback if Replit publishing is unavailable is a public source repository with complete setup instructions plus genuine Replit proof, subject to the organisers accepting it as an accessible build. Do not claim that fallback is accepted until confirmed.
