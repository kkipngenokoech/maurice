"""Media helpers for Maurice's bundled Hermes engine."""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Iterable

from gateway import rich_sent_store
from gateway.platforms.base import (
    cache_audio_from_bytes_async,
    cache_document_from_bytes_async,
    cache_image_from_bytes_async,
    cache_image_from_url,
    cache_video_from_bytes_async,
    get_inbound_media_max_bytes,
    transcode_to_ogg_opus,
)

logger = logging.getLogger(__name__)

__all__ = [
    "cache_audio_from_bytes_async",
    "cache_document_from_bytes_async",
    "cache_image_from_bytes_async",
    "cache_image_from_url",
    "cache_video_from_bytes_async",
    "inbound_media_max_bytes",
    "lookup_media",
    "record_media",
    "transcode_to_ogg_opus",
]

def inbound_media_max_bytes() -> int:
    """Hermes's ``gateway.max_inbound_media_bytes``; ``0`` means Hermes applies no cap."""
    try:
        return max(0, int(get_inbound_media_max_bytes()))
    except Exception:  # unreadable config must not break inbound handling
        return 0


async def record_media(chat_id: str, message_id: str, media: Iterable[tuple[str, str]]) -> None:
    """Remember ``(path, mime)`` attachments of a message so a later quote can re-attach them. Never raises."""
    pairs = [(str(path), str(mime or "")) for path, mime in media if path]
    if not pairs or not chat_id or not message_id:
        return
    try:
        await rich_sent_store.record_media_async(chat_id, message_id, pairs)
    except Exception as exc:
        logger.debug("rich_sent_store.record_media failed (%s)", type(exc).__name__)


async def lookup_media(chat_id: str, message_id: str) -> list[tuple[str, str]]:
    """Attachments recorded for a quoted message whose files still exist; ``[]`` on any failure."""
    if not chat_id or not message_id:
        return []
    try:
        return await asyncio.to_thread(rich_sent_store.lookup_media, chat_id, message_id)
    except Exception as exc:
        logger.debug("rich_sent_store.lookup_media failed (%s)", type(exc).__name__)
        return []
