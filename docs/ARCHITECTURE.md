# Architecture
Local synthetic-data MVP: Next.js UI → same-origin /api proxy → FastAPI → SQLAlchemy → SQLite.
Business-keyed inventory, supplier offers and users feed a documented MockOrbyteConnector.
Money uses integer sen and Decimal rounding; no LLM participates in procurement arithmetic.

Decision state machine: DETECTED → EVALUATED → PENDING_APPROVAL → APPROVED / REJECTED / CANCELLED.
Evaluation failures become FAILED. Each transition appends an audit record. Approval claims the pending row conditionally and writes approval, PO draft and audit in one transaction. A unique decision constraint and request idempotency protect against duplicate orders. Input snapshots are checked against current inventory/offers before approval; changed inputs require reevaluation.

Simulated identity: X-Demo-User selects a seeded user; database roles enforce permissions. This is intentionally not production authentication. Listen on loopback only. No payments, external orders, real customer data or public deployment.

MiroFish is a separate optional service with a pinned HTTP contract. Persistent jobs are processed by a separate local worker; timeouts/errors are visible and never fabricate reports. External execution defaults off. Production needs real identity, migrations, a durable distributed queue and tenant/security review.

See API.md, MIROFISH.md, WORKSTREAMS.md and STATUS.md. OpenAPI is generated at /docs and exported in docs/openapi.json.
