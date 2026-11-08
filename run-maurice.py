#!/usr/bin/env python3
"""Start the local Maurice gateway with its dedicated Hermes profile."""

import os
import shutil
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    local_hermes = root / ".venv/bin/hermes"
    hermes = str(local_hermes) if os.access(local_hermes, os.X_OK) else shutil.which("hermes")
    if not hermes:
        raise SystemExit("Install Hermes Agent before starting Maurice.")

    profile = root / "work/maurice-home"
    if not (profile / "SOUL.md").is_file():
        raise SystemExit("Set up the Maurice profile first. See README.md.")

    secret = root / ".secrets.env"
    try:
        key = secret.read_text(encoding="utf-8-sig").strip()
    except (OSError, UnicodeError):
        raise SystemExit("Put the WhatsApp agent key in .secrets.env.") from None

    variable = "WHATSAPP_AGENT_PLATFORM_API_KEY"
    key = key.removeprefix(f"{variable}=")
    if not key or any(not 33 <= ord(char) <= 126 for char in key):
        raise SystemExit(".secrets.env must contain one WhatsApp API key.")

    env = dict(os.environ, HERMES_HOME=str(profile))
    env[variable] = key
    os.execve(hermes, [hermes, "gateway", "run"], env)


if __name__ == "__main__":
    main()
