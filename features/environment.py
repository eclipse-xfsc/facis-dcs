"""Behave environment hooks for DCS BDD tests."""

import os
import sys
from pathlib import Path


def before_all(context):
    # Behave auto-discovers steps/ at project root; add to sys.path for direct imports
    steps_dir = Path(__file__).resolve().parent.parent / "steps"
    steps_dir_str = str(steps_dir)
    if steps_dir_str not in sys.path:
        sys.path.insert(0, steps_dir_str)

    # Shared request defaults for step definitions.
    context.base_url = os.getenv("BDD_DCS_BASE_URL", "http://127.0.0.1:8991").rstrip("/")
    context.http_timeout_seconds = float(os.getenv("BDD_HTTP_TIMEOUT_SECONDS", "20"))
    context.aliases = {}
