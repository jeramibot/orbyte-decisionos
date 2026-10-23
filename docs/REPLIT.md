# Replit import and proof of use

Configuration is prepared but **not yet verified in an authenticated Replit project**. The browser currently requires sign-in. There is no proof-of-use claim or fabricated screenshot PDF.

1. Sign into the team's Replit account. Import the authorised GitHub repository or upload the prepared source ZIP. Keep project access private while developing.
2. Confirm Python 3.12 and Node.js 24 modules are available in the actual workspace. The `.replit` module names are prepared configuration and may need adjustment to the workspace's available versions.
3. In Shell run `bash scripts/replit_setup.sh`. It installs pinned app dependencies and builds the UI. It does not invoke AI providers.
4. Press Run. The launcher exposes only the UI port 3000 to Replit's preview proxy; FastAPI stays on loopback port 8000. The hosted demo forces paid simulation execution off.
5. Verify the complete shortage-to-approval workflow and a reload. Capture real project URL/history and a screenshot showing the app running in the team's Replit workspace. Record date, commit and what was tested.
6. Run backend/component checks in Shell. If Chromium is supported, run `cd frontend && ../.tools/node_modules/.bin/pnpm exec playwright install --with-deps chromium && ../.tools/node_modules/.bin/pnpm test:e2e`; system dependency installation may require the appropriate Replit environment.
7. Assemble genuine proof PDF after actual use. Do not confuse local screenshots with Replit evidence.

This configuration has no deployment block and does not automatically publish. Public access/deployment is a separate authorised step. The prototype has selectable demo roles and should contain only invented records. SQLite in a development workspace is not a claim of persistent storage across production deployments; use the workspace/history proof route or validate durable storage before offering a hosted persistent demo.

Sources: Replit configuration documentation, https://docs.replit.com/features/project-setup/configuration ; port mapping explanation, https://replit.com/blog/ports . Reviewed 22 October 2026.
