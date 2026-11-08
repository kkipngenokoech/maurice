# WhatsApp

This adapter connects Maurice to Meta’s WhatsApp Agents API. It receives messages by long polling and sends replies through the same API.

## Setup

1. In WhatsApp, open **Settings → Agents** and create an agent. Open its chat and copy the key from **Chat info → API key**.
2. Follow the [Maurice setup instructions](../../README.md) to link the adapter and save the key in `.secrets.env`.
3. Run `pixi run maurice`. Once the gateway logs `authenticated; long polling started`, send the agent a message.

## Messages and media

By default, Maurice accepts messages from the account that created the WhatsApp agent. It handles text, voice notes, images, and supported attachments. Voice transcription and image analysis depend on the providers configured in Hermes.

Media is enabled by default. To run in text-only mode, set `WHATSAPP_AGENT_PLATFORM_MEDIA_ENABLED=false` in the environment before starting Maurice.

Agent chats pass through Meta and lack end-to-end encryption. Received attachments can be cached locally and processed by your configured providers. See [WhatsApp’s Third-Party Agents Terms](https://www.whatsapp.com/legal/third-party-agents-terms).

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| API key rejected | Copy the current key from the agent’s chat info and update `.secrets.env`. |
| `poll_conflict` (HTTP 409) | Stop any other gateway polling with the same key. |
| Connected but no reply | Message the agent from its creator account and check `.maurice/logs/gateway.log` for model or delivery errors. |

## Development

`adapter.py` connects Hermes to WhatsApp, `client.py` handles API requests, and `state.py` stores polling progress.

With `pytest` and `pytest-asyncio` available in the Pixi environment, run `pixi run python -m pytest plugins/whatsapp/tests` from the repo root. The suite uses a fake Meta API.

The adapter is MIT-licensed. See [LICENSE](LICENSE).
