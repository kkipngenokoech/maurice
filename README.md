# Maurice

Maurice is an open-source personal assistant project for WhatsApp. The goal is to turn text and voice notes into Notion notes and tasks, schedule tasks in Google Calendar on request, and send a brief covering connected Gmail inboxes, calendar events, and tasks. Granola captures live meetings separately so Maurice can use the resulting notes.

## Status

Early prototype. WhatsApp text replies have been tested with OpenAI Codex.

## Repository layout

- `SOUL.example.md` is the template for Maurice's Hermes profile.
- `run-maurice.py` starts the local gateway.
- `vendor/hermes-agent/` contains the Hermes source. Edit it here to change the agent or gateway.
- `vendor/whatsapp-agent-platform/` contains the WhatsApp adapter source.
- `work/` holds the private profile and runtime data.

## Setup

1. From the repository root, use [uv](https://docs.astral.sh/uv/) to install the bundled source in editable mode. For an existing `.venv`, skip the first command.

   ```sh
   uv venv --python 3.14
   uv pip install --python .venv/bin/python --overrides vendor/hermes-overrides.txt -e vendor/hermes-agent
   ```

2. Set up the local profile and link the bundled WhatsApp adapter:

   ```sh
   export HERMES_HOME="$PWD/work/maurice-home"
   mkdir -p "$HERMES_HOME/plugins"
   cp -n SOUL.example.md "$HERMES_HOME/SOUL.md"
   ln -sfn "$PWD/vendor/whatsapp-agent-platform" "$HERMES_HOME/plugins/whatsapp-agent-platform"
   .venv/bin/hermes plugins enable whatsapp-agent-platform
   ```

3. Run `.venv/bin/hermes model` to configure a model provider for this profile. See the [bundled WhatsApp adapter guide](vendor/whatsapp-agent-platform/README.md) for how to get the WhatsApp agent key.
4. Copy `.env.example` to `.secrets.env` and fill in your WhatsApp agent key without quotes. A file containing only the raw key also works.
5. Run `python3 run-maurice.py`. Once the gateway reports that WhatsApp authenticated, send Maurice a plain text test message.

After the text test works, enable speech-to-text for voice notes and authorize Notion, Google, and Granola separately.

Use a separate profile for each person. Keep account credentials, local configuration, recordings, transcripts, and logs outside version control.

The bundled sources retain their upstream licenses. Hermes comes from the local snapshot used for the first successful WhatsApp test. The WhatsApp adapter comes from upstream commit `3a57b1da04499279d1af6c7d979c9c2d8b658ce0`.
