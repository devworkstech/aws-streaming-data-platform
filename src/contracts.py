from __future__ import annotations
import hashlib
from datetime import datetime
from decimal import Decimal, InvalidOperation

EVENT_TYPES = {"authorization", "payment", "deposit", "withdrawal", "transfer"}


def validate(event: dict) -> dict:
    required = {"tenant_id", "account_id", "event_type", "amount", "event_time"}
    missing = required - event.keys()
    if missing:
        raise ValueError(f"missing fields: {sorted(missing)}")
    if event["event_type"] not in EVENT_TYPES:
        raise ValueError("invalid event_type")
    try:
        amount = Decimal(str(event["amount"]))
    except InvalidOperation as exc:
        raise ValueError("invalid amount") from exc
    if amount <= 0:
        raise ValueError("amount must be positive")
    timestamp = datetime.fromisoformat(event["event_time"].replace("Z", "+00:00"))
    if timestamp.tzinfo is None:
        raise ValueError("event_time must be timezone-aware")
    normalized = dict(event)
    normalized["amount"] = str(amount.quantize(Decimal("0.01")))
    return normalized


def partition_key(event: dict) -> str:
    return f"{event['tenant_id']}:{event['account_id']}"


def idempotency_key(event: dict) -> str:
    material = "|".join(str(event[k]) for k in sorted(event))
    return hashlib.sha256(material.encode()).hexdigest()
