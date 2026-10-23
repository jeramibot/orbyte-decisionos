"""Store provider settings locally without printing secrets or enabling execution."""
import argparse
import getpass
import json
import os
from pathlib import Path
from urllib.parse import urlparse
p=argparse.ArgumentParser(description='Configure the separate pinned MiroFish checkout; paid execution stays disabled in DecisionOS.')
p.add_argument('--service-dir',type=Path,required=True)
a=p.parse_args();root=a.service_dir.resolve()
if not (root/'backend/run.py').is_file():raise SystemExit('Expected the inspected MiroFish source checkout.')
target=root/'.env'
if target.exists():raise SystemExit('A service .env already exists. Edit it locally instead of overwriting it.')
url=input('Approved OpenAI-compatible provider base URL: ').strip()
if urlparse(url).scheme not in {'http','https'}:raise SystemExit('A valid provider URL is required.')
model=input('Approved model ID: ').strip()
llm=getpass.getpass('LLM API key (hidden): ').strip()
zep=getpass.getpass('Zep API key (hidden): ').strip()
if not all([model,llm,zep]):raise SystemExit('Missing setting; no file written.')
values={'LLM_BASE_URL':url,'LLM_MODEL_NAME':model,'LLM_API_KEY':llm,'ZEP_API_KEY':zep,'FLASK_HOST':'127.0.0.1','FLASK_PORT':'5001','FLASK_DEBUG':'false'}
fd=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
with os.fdopen(fd,'w') as f:
 for k,v in values.items():f.write(f'{k}={json.dumps(v)}\n')
print('Saved restricted service .env. No credentials printed. DecisionOS external execution remains disabled.')
print('Review provider budget and approvals before starting the service, worker or a live simulation.')
