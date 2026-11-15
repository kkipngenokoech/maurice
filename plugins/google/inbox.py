"""Fast, fresh inbox replies for the WhatsApp owner."""

import json
import logging
import re
from time import monotonic

from . import gmail_unread
from .agenda import is_today_request
from .whatsapp_auth import _owner_chat

logger = logging.getLogger(__name__)
_INBOX_REQUEST = re.compile(
    r"(?:(?:show|tell|get|fetch|check|summarize|read)(?: me)?(?: (?:a summary of|a list of))? "
    r"|what(?:'s| is)(?: new)? in |do i have )?"
    r"(?:my |any )?(?:latest |new |recent )?(?:unread )?"
    r"(?:gmail(?: inbox| messages)?|emails?|inbox)(?: (?:now|please|again|as well))?"
)


def route_google_request(*, event, **kwargs):
    if event.media_urls:
        return None
    text = (event.text or "").lower().replace("’", "'").strip(" .?!")
    command = "/calendar" if is_today_request(text) else "/inbox" if _INBOX_REQUEST.fullmatch(text) else None
    source = event.source
    if command and source is not None and _owner_chat(source.platform.value, source):
        return {"action": "rewrite", "text": command}
    return None


def fresh_inbox(raw_args, *, platform="", source=None):
    if not _owner_chat(platform, source):
        return "Gmail is available in the owner's private WhatsApp chat."
    started = monotonic()
    result = json.loads(gmail_unread({}))
    if "error" in result:
        return result["error"]

    lines = ["Recent unread Gmail · last 3 days"]
    available = 0
    for label, inbox in result["inboxes"].items():
        if "error" in inbox:
            lines.append(f"\n{label}: {inbox['error']}")
            continue
        available += 1
        lines.append(f"\n{label} · {inbox['email']}")
        for message in inbox["unread_inbox_last_3_days"]:
            sender = " ".join((message["from"] or "Unknown sender").split())
            subject = " ".join((message["subject"] or "(No subject)").split())
            lines.append(f"• {sender[:100]} — {subject[:160]}")
        if not inbox["unread_inbox_last_3_days"]:
            lines.append("No recent unread messages.")
        if inbox["more"]:
            lines.append("More results are available in Gmail.")
    logger.info("Fresh WhatsApp inbox fetched: %d/%d inboxes available in %.2fs",
                available, len(result["inboxes"]), monotonic() - started)
    return "\n".join(lines)
