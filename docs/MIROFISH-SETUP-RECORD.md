# Local upstream setup record

Upstream commit `7657031ac01184afe2cb220f5ee3545573b5e843` was checked out separately in the task's `work/mirofish-service` directory. Source/setup scripts were inspected before installation. `uv sync --frozen --no-dev` used upstream `backend/uv.lock` and Python 3.12.14; **133 packages installed successfully**. The application repository does not contain that checkout or its virtual environment.

The unmodified upstream `backend/run.py` was executed. It exited with configuration errors for missing **LLM_API_KEY** and **ZEP_API_KEY** before starting the server. This verifies that the installed entrypoint reaches configuration validation. It is not a live simulation test, service-health result or provider authentication check. No model inference or paid provider call was executed.

To enter approved credentials locally, run from the application root:

```bash
.venv/bin/python scripts/configure_mirofish.py --service-dir /absolute/path/to/work/mirofish-service
```

The helper prompts for the provider base URL/model and hides API-key input. It creates an ignored service `.env` with mode 0600, binds upstream to loopback and refuses to overwrite an existing file. It does not enable DecisionOS external execution. Do not paste keys in chat or commit the file.

The selected LLM path is **Google AI Studio Gemini API Free tier**, using its OpenAI-compatible endpoint. The local ignored service `.env` now exists with mode 0600 and base URL `https://generativelanguage.googleapis.com/v1beta/openai/`. Its Gemini key authenticated to `models.list`, completed a three-token `countTokens` request, and completed a tiny native `generateContent` request. The initial `gemini-3.1-flash-lite` model timed out through Google's OpenAI-compatible endpoint. The local model was changed to `gemini-3.5-flash-lite`; a tiny chat completion through the pinned backend's OpenAI SDK returned `OK.`, and CAMEL's model factory created an `OpenAIModel` for it offline. This confirms a small provider call, **not** an end-to-end MiroFish simulation. The Google project's actual Free tier eligibility and quota have not been independently confirmed. Do not enable billing. Use synthetic scenario data only.

Zep's dashboard shows a Free-plan project, but the locally entered Zep value was a masked dashboard display pasted twice. The pinned Zep client returned HTTP 401; no valid Zep authentication has been established. Create a new Zep key and copy its **full value from the one-time creation screen**. Replace only that local setting with `scripts/replace_mirofish_zep_key.py --service-dir /absolute/path/to/work/mirofish-service`; this helper rejects masked text and hides input. Do not copy the masked key shown later in Zep's table.

Next: verify the replacement Zep key, agree a call/usage limit within available free quotas, then start the separate upstream service, explicitly enable the DecisionOS external flag, start the worker and perform one small run with actual provenance/runtime/usage capture. No live-run or proof PDF will be created from fixture data.
