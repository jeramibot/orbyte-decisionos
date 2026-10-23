# Local upstream setup record

Upstream commit `7657031ac01184afe2cb220f5ee3545573b5e843` was checked out separately in the task's `work/mirofish-service` directory. Source/setup scripts were inspected before installation. `uv sync --frozen --no-dev` used upstream `backend/uv.lock` and Python 3.12.14; **133 packages installed successfully**. The application repository does not contain that checkout or its virtual environment.

The unmodified upstream `backend/run.py` was executed. It exited with configuration errors for missing **LLM_API_KEY** and **ZEP_API_KEY** before starting the server. This verifies that the installed entrypoint reaches configuration validation. It is not a live simulation test, service-health result or provider authentication check. No model inference or paid provider call was executed.

To enter approved credentials locally, run from the application root:

```bash
.venv/bin/python scripts/configure_mirofish.py --service-dir /absolute/path/to/work/mirofish-service
```

The helper prompts for the provider base URL/model and hides API-key input. It creates an ignored service `.env` with mode 0600, binds upstream to loopback and refuses to overwrite an existing file. It does not enable DecisionOS external execution. Do not paste keys in chat or commit the file.

Next required input: approved provider/model, Zep account and maximum spend. After configuration, start the separate upstream service, explicitly enable the DecisionOS external flag, start the worker and perform one small run with actual provenance/runtime/usage capture. No live-run or proof PDF will be created from fixture data.
