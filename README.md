# Maurice

Maurice is an open-source personal assistant project for WhatsApp. The goal is to turn text and voice notes into Notion notes and tasks, schedule tasks in Google Calendar on request, and send a brief covering connected Gmail inboxes, calendar events, and tasks. Granola captures live meetings separately so Maurice can use the resulting notes.

## Status

Early prototype. The repository contains the Maurice profile template and a launcher for the Hermes gateway. WhatsApp authentication and end-to-end replies are still being tested.

## Repository layout

- `SOUL.example.md` is the template for Maurice's Hermes profile.
- `run-maurice.py` starts the local gateway.
- `work/` holds the private Hermes profile and local development files. Hermes and its WhatsApp plugin are upstream dependencies.

## Setup

1. Install [Hermes Agent](https://hermes-agent.nousresearch.com/docs/getting-started/installation) and open a terminal at the repository root.
2. Create the local profile and copy the template without overwriting an existing profile:

   ```sh
   export HERMES_HOME="$PWD/work/maurice-home"
   mkdir -p "$HERMES_HOME"
   cp -n SOUL.example.md "$HERMES_HOME/SOUL.md"
   ```

3. Run `hermes plugins install whatsapp-agent-platform --enable` and use `hermes model` to configure a model provider for this profile. See the [WhatsApp plugin setup](https://hermes-agent.nousresearch.com/marketplace/whatsapp-agent-platform).
4. Copy `.env.example` to `.secrets.env` and fill in your WhatsApp agent key without quotes. A file containing only the raw key also works.
5. Run `python3 run-maurice.py`. Once the gateway reports that WhatsApp authenticated, send Maurice a plain text test message.

After the text test works, enable speech-to-text for voice notes and authorize Notion, Google, and Granola separately.

Use a separate profile for each person. Keep account credentials, local configuration, recordings, transcripts, and logs outside version control.
