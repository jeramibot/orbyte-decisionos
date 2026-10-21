# Licensing and upstream boundaries

Original DecisionOS application code is offered under Apache License 2.0; see the root LICENSE. Dependency licences continue to apply. No MiroFish source has been copied, imported or vendored into this application's runtime.

MiroFish is a separately installed optional HTTP service, pinned to `7657031ac01184afe2cb220f5ee3545573b5e843`. Its source declares **AGPL-3.0**. Its licence text is preserved in `docs/licenses/MiroFish-AGPL-3.0.txt` for reference. Upstream: https://github.com/666ghj/MiroFish/tree/7657031ac01184afe2cb220f5ee3545573b5e843 . We have not relicensed it under Apache.

AGPL carries source-distribution obligations; section 13 requires a modified network-interactive version to offer its corresponding source to remote users. Service isolation is an engineering boundary, not a guarantee that every combined deployment avoids AGPL obligations. Before distributing a combined system, copying upstream code, modifying MiroFish or offering it over a network, review the actual combination and obtain organiser clarification about the Apache submission requirement. Keep upstream notices and make corresponding source available where required.

Authoritative licence: https://www.gnu.org/licenses/agpl-3.0.html . Original application licence: https://www.apache.org/licenses/LICENSE-2.0 . No public combined deployment has been made.

Key runtime dependencies: Next.js/React/Tailwind/lucide (MIT), FastAPI/SQLAlchemy (MIT), Pydantic (MIT), HTTPX (BSD-3-Clause), Uvicorn (BSD-3-Clause). Exact direct and transitive versions are recorded in the Python and frontend lockfiles; retain installed package notices when redistributing dependencies.
