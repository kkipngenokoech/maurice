# Maurice

Maurice is an open-source personal assistant project for WhatsApp. The goal is to turn text and voice notes into Notion notes and tasks, schedule tasks in Google Calendar on request, and send a brief covering connected Gmail inboxes, calendar events, and tasks. Granola captures live meetings separately so Maurice can use the resulting notes.

## Status

Early prototype. This repository contains an example agent profile. Account connections and end-to-end delivery are still being tested.

## Setup

1. Install [Hermes Agent](https://hermes-agent.nousresearch.com/docs/getting-started/installation) and create a dedicated profile.
2. Copy `SOUL.example.md` to `SOUL.md` in the profile's data directory. Replace the example timezone and choose your own Notion databases and calendar.
3. Set up the [WhatsApp Agent Platform plugin](https://hermes-agent.nousresearch.com/marketplace/whatsapp-agent-platform). Keep your API key in your local profile. Enable speech-to-text for voice notes.
4. Connect your chosen model provider, then authorize Notion, Google, and Granola separately. Start with one test note and verify the saved item before using real data.

Use a separate profile for each person. Keep account credentials, local configuration, recordings, transcripts, and logs outside version control.
