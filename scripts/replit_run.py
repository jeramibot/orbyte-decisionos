"""Replit synthetic preview: UI exposed to workspace proxy, API loopback only."""
from pathlib import Path
import os
import subprocess
import sys
import time
ROOT = Path(__file__).resolve().parents[1]
if not (ROOT / 'frontend/.next/BUILD_ID').exists():
    raise SystemExit('Run bash scripts/replit_setup.sh first.')
if not os.getenv('REPL_ID'):
    raise SystemExit('This launcher is for Replit only. Use scripts/dev.py locally.')
# This hosted demonstration never enables paid simulations, even if a secret was set.
env = {**os.environ, 'MIROFISH_ALLOW_EXTERNAL': 'false', 'NEXT_TELEMETRY_DISABLED': '1',
       'DATABASE_URL': f"sqlite:///{ROOT / 'data/runtime/decisionos.db'}"}
commands = [([str(ROOT / '.venv/bin/python'), '-m', 'uvicorn', 'backend.api.app:app', '--host', '127.0.0.1', '--port', '8000'], ROOT),
            (['node', 'node_modules/next/dist/bin/next', 'start', '--hostname', '0.0.0.0', '--port', '3000'], ROOT / 'frontend')]
children=[]
exit_code=0
try:
    for command,cwd in commands:
        children.append(subprocess.Popen(command,cwd=cwd,env=env))
    print('Synthetic Replit preview. Selectable demo roles; no real transactions. Keep workspace access private until publication is authorised.',flush=True)
    while all(p.poll() is None for p in children): time.sleep(1)
    exit_code=next((p.returncode for p in children if p.returncode is not None),0)
except KeyboardInterrupt:
    pass
finally:
    for p in children:
        if p.poll() is None: p.terminate()
    for p in children:
        try: p.wait(timeout=10)
        except subprocess.TimeoutExpired: p.kill()
raise SystemExit(exit_code)
