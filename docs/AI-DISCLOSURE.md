# AI-assisted development disclosure draft

The team supplied the product/build prompt and scenario requirements. OpenAI Codex assisted extensively with architecture refinement, application code, synthetic seed records, tests, debugging, upstream source inspection and documentation. Deterministic backend rules perform procurement arithmetic. The running operational demo does not call an LLM.

Codex executed backend and component tests, TypeScript checks, a production build and native-browser workflow checks. Playwright browser startup was blocked in the local macOS execution sandbox. These are development checks, not evidence of team review or real SME validation.

MiroFish is an optional separately licensed upstream project, source-pinned and inspected. Its HTTP integration was tested with clearly synthetic mocked responses. No live simulation, paid LLM call or Zep usage was performed during this build; no generated report is being passed off as a genuine run.

Before official submission, the registered team must review, adapt, test and understand the substantial AI-assisted work, and ensure the idea/design ownership and actual assistance disclosure meet organiser rules. Do not state that team review, workshop attendance or platform usage is complete until it actually is. Record the actual assistant/model details available in the team's tool history, versions, extent of assistance and resulting human changes in the official declaration.

For the earlier rules review, Whisper `base.en` through faster-whisper produced local CPU transcripts of the supplied workshop videos. Transcripts plus sampled frames were reviewed; this is not team workshop attendance or a claim of frame-by-frame viewing. ReportLab/PyPDF and the Codex presentation artifact runtime were used to prepare submission files. The pinned MiroFish backend environment is installed separately, but its configuration preflight stops without provider keys.
