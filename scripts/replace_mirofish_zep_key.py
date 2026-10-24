"""Replace only the local MiroFish Zep key using hidden input."""

import argparse
import getpass
import json
import os
import tempfile
from pathlib import Path


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--service-dir", type=Path, required=True)
args = parser.parse_args()
target = args.service_dir.resolve() / ".env"
if not target.is_file():
    raise SystemExit("MiroFish .env is missing; run configure_mirofish.py first.")

lines = target.read_text().splitlines()
if sum(line.startswith("ZEP_API_KEY=") for line in lines) != 1:
    raise SystemExit("Expected exactly one ZEP_API_KEY setting; no change made.")

key = getpass.getpass("New full Zep API key (hidden; paste once): ").strip()
if len(key) % 2 == 0 and key[: len(key) // 2] == key[len(key) // 2 :]:
    key = key[: len(key) // 2]
if not key.startswith("z_") or "*" in key or any(char.isspace() for char in key) or len(key) < 20:
    raise SystemExit("That looks like a masked or incomplete Zep key; no change made.")

replacement = [
    "ZEP_API_KEY=" + json.dumps(key) if line.startswith("ZEP_API_KEY=") else line
    for line in lines
]
fd, temporary = tempfile.mkstemp(prefix=".env.", dir=target.parent)
try:
    os.fchmod(fd, 0o600)
    with os.fdopen(fd, "w") as output:
        output.write("\n".join(replacement) + "\n")
        output.flush()
        os.fsync(output.fileno())
    os.replace(temporary, target)
finally:
    if os.path.exists(temporary):
        os.unlink(temporary)
print("Saved new Zep key locally; key not printed. External execution remains disabled.")
