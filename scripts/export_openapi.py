from pathlib import Path
import json
from backend.api.app import app
Path('docs/openapi.json').write_text(json.dumps(app.openapi(), indent=2)+'\n')
