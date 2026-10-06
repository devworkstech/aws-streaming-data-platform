import base64
import json
from src.contracts import partition_key, validate
from src.processor import handler

EVENT = {"tenant_id":"bank-demo-01","account_id":"acct-1","event_type":"payment","amount":"12.50","event_time":"2026-10-01T12:00:00Z"}


def kinesis_record(payload, event_id="1"):
    return {"eventID": event_id, "kinesis": {"data": base64.b64encode(json.dumps(payload).encode()).decode()}}


def test_partition_key_preserves_account_ordering():
    assert partition_key(EVENT) == "bank-demo-01:acct-1"


def test_valid_batch_is_processed():
    result = handler({"Records": [kinesis_record(EVENT)]})
    assert result["batchItemFailures"] == []
    assert result["processed"][0]["amount"] == "12.50"


def test_invalid_record_is_reported_for_retry():
    bad = dict(EVENT, amount="-2")
    result = handler({"Records": [kinesis_record(bad, "bad-1")]})
    assert result["batchItemFailures"] == [{"itemIdentifier": "bad-1"}]
