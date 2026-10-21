"""Run the built UI and API on loopback. No tunnel, deployment, or paid service."""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import time
from dotenv import load_dotenv
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / '.env')
node = shutil.which('node')
if not node:
    bundled = Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
    if bundled.exists(): node = str(bundled)
if not node:
    raise SystemExit('Node.js 24 is required. Install Node or add it to PATH.')
if not (ROOT / 'frontend/.next/BUILD_ID').exists():
    raise SystemExit('Build the UI first: cd frontend && pnpm build')
env = {**os.environ, 'NEXT_TELEMETRY_DISABLED': '1'}
commands = [([sys.executable, '-m', 'uvicorn', 'backend.api.app:app', '--host', '127.0.0.1', '--port', '8000'], ROOT),
    ([node, 'node_modules/next/dist/bin/next', 'start', '--hostname', '127.0.0.1', '--port', '3000'], ROOT / 'frontend')]
children = []
exit_code = 0
try:
    for command, cwd in commands:
        children.append(subprocess.Popen(command, cwd=cwd, env=env))
    print('DecisionOS: http://127.0.0.1:3000 — API docs: http://127.0.0.1:8000/docs', flush=True)
    print('Synthetic data and simulated roles only. Press Ctrl+C to stop both services.', flush=True)
    while all(p.poll() is None for p in children): time.sleep(1)
    exit_code = next((p.returncode for p in children if p.returncode is not None), 0)
except KeyboardInterrupt:
    print('Stopping local DecisionOS services.', flush=True)
finally:
    for child in children:
        if child.poll() is None: child.terminate()
    for child in children:
        try: child.wait(timeout=10)
        except subprocess.TimeoutExpired: child.kill()

raise SystemExit(exit_code)
