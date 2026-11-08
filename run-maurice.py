#!/usr/bin/env python3
"""Start the local Maurice gateway with its dedicated Hermes profile."""

import os
import sys
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    hermes = Path(sys.executable).with_name("hermes")
    if not os.access(hermes, os.X_OK):
        raise SystemExit("Start Maurice with 'pixi run maurice'. See README.md.")

    profile = root / ".maurice"
    if not (profile / "SOUL.md").is_file():
        raise SystemExit("Set up the Maurice profile first. See README.md.")

    plugin = profile / "plugins/whatsapp-agent-platform"
    bundled_plugin = root / "plugins/whatsapp-agent-platform"
    if not plugin.is_dir() or plugin.resolve() != bundled_plugin:
        raise SystemExit("Link the bundled WhatsApp plugin first. See README.md.")

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
