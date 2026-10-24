# Five-minute demonstration script

Target: approximately **5:15**, within the reviewed preliminary **5–7 minute** video requirement. Rehearse with the actual running build. Do not use mocked simulation results.

Before recording, install/build via README, start both servers and confirm the local URL. For a clean initial state, deliberately reset the default synthetic database only after stopping servers. Start again and choose Purchasing manager. Close any private tabs/notifications. Prepare slides and genuine submission links separately.

| Time | Show | Narration / evidence |
|---|---|---|
| 0:00–0:35 | Brief problem slide and overview | A small café owner repeatedly checks stock, compares quotes and approves purchases. We focus on one workflow and preserve human control. All data is synthetic. |
| 0:35–1:15 | Operations inventory and supplier records | Milk: 18 litres, usage 12/day, threshold 3 days, purchase 60 litres. These inputs are visible; the mock hub is our own interface, not official Orbyte API access. |
| 1:15–2:05 | Run inventory check; decision workspace | Trigger → connected data → rule evaluation. Coverage is 1.5 days. A costs RM570 but arrives in 4 days; B costs RM660 and arrives in 1 day. RM90 is the premium, not proven savings. Delivery and consumption are estimates. |
| 2:05–2:55 | Manager's disabled approval, then switch to owner | Explain simulated roles and backend checks. Select B; enter “Pay RM90 more for estimated delivery before stock runs out.” Approve and show the draft. No external supplier transaction occurs. |
| 2:55–3:30 | Reload and audit log | Show persisted approval and PO events, actor, time, reason, and before/after values. Approval, order draft and audit commit together. Stock stays unchanged until a future receiving workflow. |
| 3:30–4:10 | Simulation Lab | Explain optional delivery-delay perspectives. Check availability: current result is Unavailable, no report, tokens not reported. This honestly demonstrates graceful failure; we have not completed a live MiroFish run. Show strategic menu-price configuration only if time permits. |
| 4:10–4:45 | Architecture / validation slide | Deterministic calculations, optional isolated simulation, reusable business-scoped connector. Mention 33 backend, three component and four Replit browser tests passed; GitHub CI and the public synthetic Replit demo were also verified. |
| 4:45–5:15 | Impact and next steps | SDG 8.2/8.3: intended reduction in repetitive administrative work and better traceable decisions. No measured productivity gain yet. Plan a timed usability comparison and a small synthetic simulation run after valid provider setup. |

Fallback: if the browser/server fails, restart the local launcher and use a truthful backup recording of an actual working run. A recording does not replace the required functioning prototype/access instructions. Keep the final presentation consistent with the precise repository version submitted.
