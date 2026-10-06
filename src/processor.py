"""Lambda-style Kinesis batch processor with partial batch failure response."""
import base64
import json
from src.contracts import idempotency_key, validate


def decode_record(record: dict) -> dict:
    payload = base64.b64decode(record["kinesis"]["data"])
    return json.loads(payload)


def process(event: dict) -> dict:
    record = validate(event)
    return {
        "idempotency_key": idempotency_key(record),
        "tenant_id": record["tenant_id"],
        "account_id": record["account_id"],
        "event_type": record["event_type"],
        "amount": record["amount"],
        "event_time": record["event_time"],
    }


def handler(event, context=None):
    failures = []
    processed = []
    for item in event.get("Records", []):
        try:
            processed.append(process(decode_record(item)))
        except (ValueError, KeyError, json.JSONDecodeError):
            failures.append({"itemIdentifier": item.get("eventID", "unknown")})
    return {"batchItemFailures": failures, "processed": processed}
