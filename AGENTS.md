# DecisionOS engineering rules
Use synthetic data only. Keep paid external calls disabled by default. Never deploy or push without user approval.
Money uses integer sen; quantities use Decimal. Every consequential action requires a backend owner-role check.
Approval, PO and audit must commit atomically. Never bypass stale-snapshot checks or idempotency.
Run backend pytest, frontend unit tests/typecheck/build and Playwright for critical workflow changes.
Do not present fixture data as genuine MiroFish results. Do not copy AGPL source into this Apache application.
Keep docs/STATUS.md factual and up to date. Workstreams are modules, not permission to exceed the five-member event limit.
