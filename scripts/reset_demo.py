"""Explicitly reset only the default local demo database; never runs automatically."""
from pathlib import Path
import argparse
from backend.db import ROOT
parser=argparse.ArgumentParser(description='Stop local servers before resetting demo data.')
parser.add_argument('--confirm', action='store_true')
args=parser.parse_args()
if not args.confirm: raise SystemExit('This removes demo decisions and audit history. Rerun with --confirm only after stopping servers.')
for suffix in ['', '-wal', '-shm']:
    path=ROOT / f'data/runtime/decisionos.db{suffix}'
    if path.exists(): path.unlink()
print('Default local demo database removed. It will be seeded on the next API start. Custom DATABASE_URL databases are untouched.')
