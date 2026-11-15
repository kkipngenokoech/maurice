"""Fresh calendar replies for the WhatsApp owner."""

import logging
import re
from datetime import datetime
from time import monotonic

from . import TIMEZONE, _calendar_today, _read
from .whatsapp_auth import _owner_chat

logger = logging.getLogger(__name__)
_TODAY_REQUEST = re.compile(
    r"(?:(?:show|check|list|get|fetch)(?: me)? )?"
    r"(?:what(?:'s| is) on (?:my )?(?:google )?calendar today"
    r"|what(?:'s| is) on my schedule today|what do i have (?:on my calendar )?today"
    r"|(?:my )?(?:today's )?(?:google calendar|calendar|agenda|schedule|events)"
    r"(?: (?:for )?today)?|today's (?:calendar )?events)"
    r"(?: please|[.?] use google calendar)?"
)


def is_today_request(text):
    return _TODAY_REQUEST.fullmatch(text) is not None


def fresh_agenda(raw_args, *, platform="", source=None):
    if not _owner_chat(platform, source):
        return "Google Calendar is available in the owner's private WhatsApp chat."
    if raw_args and raw_args.strip().lower() != "today":
        return "Use /calendar to see today's events."
    started = monotonic()
    result = _read(_calendar_today)
    if "error" in result:
        return result["error"]
    logger.info("Fresh WhatsApp calendar fetched: %d events in %.2fs",
                len(result["events"]), monotonic() - started)

    lines = [f"Google Calendar · {result['date']} (Kigali time)"]
    for event in result["events"]:
        start = event.get("start", {})
        end = event.get("end", {})
        when = "All day"
        if start.get("dateTime") and end.get("dateTime"):
            begins = datetime.fromisoformat(start["dateTime"]).astimezone(TIMEZONE)
            ends = datetime.fromisoformat(end["dateTime"]).astimezone(TIMEZONE)
            when = f"{begins:%H:%M}–{ends:%H:%M}"
            if begins.date() != ends.date():
                when = f"{begins:%b %d %H:%M}–{ends:%b %d %H:%M}"
        title = " ".join((event.get("summary") or "(Untitled event)").split())
        lines.append(f"• {when} — {title[:160]}")
    if not result["events"]:
        lines.append("No events today.")
    if result["more"]:
        lines.append("More events are available in Google Calendar.")
    return "\n".join(lines)
