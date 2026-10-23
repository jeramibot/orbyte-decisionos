"""Keep test collection independent of host-provided service credentials."""
import os

# Importing the ASGI module creates a default app before per-test factories run.
# Replit may inject a PostgreSQL DATABASE_URL; tests must never use that service.
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["MIROFISH_ALLOW_EXTERNAL"] = "false"
