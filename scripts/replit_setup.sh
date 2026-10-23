#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -c 'import sys; assert (3,11) <= sys.version_info[:2] <= (3,12), "Use Python 3.12 for this project"'
node -e 'if(Number(process.versions.node.split(".")[0])<22) throw Error("Use Node.js 24")'
python3 -m venv .venv
.venv/bin/python -m pip install --no-user -r backend/requirements.lock
npm install --prefix .tools --no-save pnpm@11.25.0
.tools/node_modules/.bin/pnpm --dir frontend install --frozen-lockfile
BACKEND_URL=http://127.0.0.1:8000 NEXT_TELEMETRY_DISABLED=1 .tools/node_modules/.bin/pnpm --dir frontend build
printf 'Setup complete. Use the Replit Run button for the synthetic preview.\n'
