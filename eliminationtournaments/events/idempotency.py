from django.core.cache import cache

EVENT_TTL_SECONDS = 60 * 60 * 24  # 24 hours


def is_event_processed(event_id: str) -> bool:
    return cache.get(f"event:{event_id}") is not None


def mark_event_processed(event_id: str) -> None:
    cache.set(
        f"event:{event_id}",
        True,
        timeout=EVENT_TTL_SECONDS,
    )