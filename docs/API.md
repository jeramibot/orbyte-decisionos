# API contract v0.1

REST under `/api`. `X-Demo-User` is **simulated identity**, resolved to a seeded database user. Missing identity selects the read-only observer. Never deploy this as real authentication. Default actors: `owner-demo`, `manager-demo`, `viewer-demo`. Business ownership is checked server-side. All data are fictional; money is integer sen.

| Route | Method | Permission / contract |
|---|---|---|
| `/health` | GET | Local health status |
| `/bootstrap` | GET | Business, users, inventory, offers, decisions, recent audit, simulation availability |
| `/monitor` | POST | Owner/manager; `{item_id}`; deduplicates an active decision; returns FAILED with audit if evaluation lacks inputs |
| `/decisions/{id}` | GET | Same-business decision, immutable input snapshot, options, approval, PO and audit |
| `/decisions/{id}/resolve` | POST | Owner; `Idempotency-Key` 8–100 chars; `{action: approve/reject/cancel, option_id?, reason, acknowledge_risk}` |
| `/decisions/{id}/refresh` | POST | Owner/manager; supersedes pending decision and creates a fresh evaluation atomically |
| `/inventory/{id}` | PATCH | Owner; quantity, daily_usage, threshold_days, purchase_quantity, expected_version, reason |
| `/offers/{id}` | PATCH | Owner; unit_price_sen, lead_days, expected_version, reason |
| `/simulations` | POST | Owner; template (`delivery_delay`/`price_change`), item_id, delay_days, price_change_percent, rounds 1–3 |
| `/simulations/{id}` | GET | Same-business persistent run and genuine report if completed |
| `/simulations/{id}/cancel` | POST | Owner; cancellation request, terminal only after queue/worker handling |

Errors: 401 unknown actor; 403 permission denied; 404 absent/other-business resource; 409 state conflict, stale input or already sufficient coverage; 422 validation or unacknowledged stockout risk; 503 database failure. API errors are visible in the UI. No mutation is made by GET.

Approval must select an option owned by that decision. Before approving, compare current inventory/offer fingerprint with stored snapshot. On conflict, re-evaluate. Identical idempotency retries return the original result; different payload with the same key returns 409. Parallel approvals can return 409 or transient SQLite 503 to the losing request but cannot create a second PO. PO, approval, audit and final status commit together.

`docs/openapi.json` is generated from Pydantic/FastAPI and is the detailed request contract. Local interactive docs: http://127.0.0.1:8000/docs . Snapshots retain evidence; approved drafts do not increase inventory or claim delivery.
