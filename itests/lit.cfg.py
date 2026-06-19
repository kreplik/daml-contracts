import os
import sys

import lit.formats

# Integration tests run against the live Canton node that `dpm trace test
# --integration` boots. Connection details arrive via DPM_TRACE_IT_* env vars.
config.name = "asset-integration"
config.test_format = lit.formats.ShTest(execute_external=True)  # real /bin/sh: $(...) etc.
config.suffixes = [".test"]
config.test_source_root = os.path.dirname(__file__)
config.test_exec_root = os.path.join(config.test_source_root, ".lit")

# The runner exports DPM_TRACE_IT_* before invoking lit. If they are missing the
# suite was started without a live Canton (e.g. plain `lit itests/`); fail loudly
# rather than skip, so a mis-wired runner can never go green with zero tests run.
ledger = os.environ.get("DPM_TRACE_IT_LEDGER")
if not ledger:
    lit_config.fatal(
        "integration tests need a live Canton; run them with "
        "`dpm trace test --integration <dir>` (DPM_TRACE_IT_LEDGER is not set)."
    )

python = os.environ.get("DPM_TRACE_IT_PYTHON", sys.executable)
src = os.environ.get("DPM_TRACE_IT_SRC", "")
config.environment["PYTHONPATH"] = src

config.substitutions.append(("%dpm", f"{python} -m dpm_trace.cli"))
config.substitutions.append(("%ledger", ledger))
config.substitutions.append(("%alice", os.environ.get("DPM_TRACE_IT_ALICE", "")))
config.substitutions.append(("%bob", os.environ.get("DPM_TRACE_IT_BOB", "")))
config.substitutions.append(("%dar", os.environ.get("DPM_TRACE_IT_DAR", "")))
