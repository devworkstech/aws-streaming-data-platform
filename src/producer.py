"""Kinesis producer. Requires boto3 and AWS credentials only when executed."""
import json
import os
from src.contracts import partition_key, validate


def publish(client, stream_name: str, event: dict):
    record = validate(event)
    return client.put_record(
        StreamName=stream_name,
        Data=json.dumps(record).encode("utf-8"),
        PartitionKey=partition_key(record),
    )


def main():
    import boto3
    stream = os.environ["STREAM_NAME"]
    client = boto3.client("kinesis")
    demo = {
        "tenant_id": "bank-demo-01",
        "account_id": "acct-1001",
        "event_type": "authorization",
        "amount": "89.25",
        "event_time": "2026-10-01T12:00:00Z",
    }
    print(publish(client, stream, demo))


if __name__ == "__main__":
    main()
