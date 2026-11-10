# Maurice

Maurice is an open-source personal assistant project for WhatsApp. The goal is to turn text and voice notes into Notion notes and tasks, schedule tasks in Google Calendar on request, and send a brief covering connected Gmail inboxes, calendar events, and tasks. Granola captures live meetings separately so Maurice can use the resulting notes.

## Status

Early prototype. WhatsApp text replies have been tested with OpenAI Codex.

## Repository layout

- `SOUL.example.md` is the template for Maurice's Hermes profile.
- `run-maurice.py` starts the local gateway.
- `engine/` contains the Hermes source. Edit it here to change the agent or gateway.
- `plugins/whatsapp/` contains the WhatsApp adapter source.
- `.maurice/` holds the private profile and runtime data.

## Setup

1. On Apple Silicon with macOS 14 or newer, use [Pixi](https://pixi.sh/) to install the bundled Hermes source and local Whisper from the repository root.

   ```sh
   pixi install
   ```

2. Set up the local profile and link the bundled WhatsApp adapter:

   ```sh
   export HERMES_HOME="$PWD/.maurice"
   mkdir -p "$HERMES_HOME/plugins"
   cp -n SOUL.example.md "$HERMES_HOME/SOUL.md"
   ln -sfn ../../plugins/whatsapp "$HERMES_HOME/plugins/whatsapp-agent-platform"
   pixi run hermes plugins enable whatsapp-agent-platform
   ```

3. Run `pixi run hermes model` to configure a model provider for this profile. See the [bundled WhatsApp adapter guide](plugins/whatsapp/README.md) for how to get the WhatsApp agent key.
4. Copy `.env.example` to `.secrets.env` and fill in your WhatsApp agent key without quotes. A file containing only the raw key also works.
5. Run `pixi run maurice`. Once the gateway reports that WhatsApp authenticated, send Maurice a plain text test message.

Send a short voice note after the text test. Local transcription downloads the Whisper model on first use. Authorize Notion, Google, and Granola separately.

Use a separate profile for each person. Keep account credentials, local configuration, recordings, transcripts, and logs outside version control.

The bundled sources retain their upstream licenses. Hermes comes from the local snapshot used for the first successful WhatsApp test. The WhatsApp adapter comes from upstream commit `3a57b1da04499279d1af6c7d979c9c2d8b658ce0`.

## Connect Google Calendar and Gmail

1. In the [Google Cloud Console](https://console.cloud.google.com/), enable the Google Calendar API and Gmail API in one project. Set up the OAuth consent screen, add each account as a test user if applicable, and download a **Desktop app** OAuth client JSON. Keep it outside this repository.
2. Add `maurice-google` to the `plugins.enabled` list in `.maurice/config.yaml`. Then run these commands from the repository root, replacing the client JSON path with your downloaded file.

   ```sh
   export HERMES_HOME="$PWD/.maurice"
   mkdir -p "$HERMES_HOME/plugins"
   ln -s ../../plugins/google "$HERMES_HOME/plugins/maurice-google"
   pixi run python plugins/google/connect.py /path/to/client.json
   ```

3. Open the consent link printed by the command and approve the two read-only scopes. Restart Maurice with `pixi run maurice` and ask “What's on my calendar today?” or “Which unread emails need my attention?”

The first sign-in connects the primary account's calendar and Gmail. For another inbox, reuse the same client JSON and choose a different Google account at the consent screen:

```sh
HERMES_HOME="$PWD/.maurice" pixi run python plugins/google/connect.py /path/to/client.json --account work
```

Use a unique label for each extra inbox. These accounts grant read-only Gmail access. Maurice checks recent unread messages across all connected inboxes, identifies any unavailable account, and stores each token separately in the private profile.

### Connect from WhatsApp

On the machine running Maurice, set up a public HTTPS route for `/google/callback` that forwards only that path to `http://127.0.0.1:8766/google/callback`. Disable callback query-string logging in the proxy. Maurice starts the local listener when it issues its first sign-in link.

Create a **Web application** OAuth client in your Google Cloud project and register the full public callback URL as an authorized redirect URI. Save its downloaded JSON as `.maurice/credentials/google-web-client.json` with file permissions `0600`. Set `MAURICE_GOOGLE_REDIRECT_URI` to that same HTTPS URL in the environment that starts `pixi run maurice`, then restart Maurice.

In the owner's private WhatsApp chat, send `/connect-google` for Calendar and Gmail or `/connect-google work` for an additional Gmail inbox. Open the link and pick the account in Google. If WhatsApp's in-app browser is rejected by Google, open the link in your phone's browser. The confirmation page tells you when the account is ready.
