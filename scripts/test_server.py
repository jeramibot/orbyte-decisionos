"""Fresh disposable database for browser tests; never resets the interactive demo."""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import os
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ['DATABASE_URL'] = 'sqlite://'
os.environ['MIROFISH_ALLOW_EXTERNAL'] = 'false'
import uvicorn
from backend.api.app import create_app
with TemporaryDirectory(prefix='decisionos-e2e-') as tmp:
    uvicorn.run(create_app(f'sqlite:///{tmp}/e2e.db'), host='127.0.0.1', port=8001)
