# AWS Streaming Data Platform

A portfolio-grade event streaming reference architecture for ingesting and processing financial events with Amazon Kinesis, Python and AWS Lambda patterns. It emphasizes schema validation, deterministic partitioning, event-time handling, idempotency and operational observability.

> Uses synthetic events only. No employer or customer source code/data is included.

## Architecture

```text
Synthetic event producer
        |
        v
 Amazon Kinesis Data Streams
        |
        v
 Lambda stream processor
   |                 |
   v                 v
S3 replay/archive   CloudWatch metrics / DLQ pattern
   |
   v
Athena / Glue / downstream analytics
```

A Kafka/MSK deployment can use the same event contract and partition-key strategy; `tenant_id:account_id` keeps account-level event ordering deterministic while distributing tenants across partitions.

## What this demonstrates

- Python producer with a stable JSON event contract.
- Kinesis partition-key strategy for multi-tenant financial workloads.
- Lambda batch processing with per-record failure reporting.
- Idempotency keys derived from business fields.
- Event-time parsing and validation rather than relying on processing time.
- Terraform for Kinesis, S3 archive storage and IAM.
- Unit tests that run without AWS credentials.

## Layout

```text
src/contracts.py             Shared event validation/idempotency
src/producer.py              Kinesis producer example
src/processor.py             Lambda stream processor
terraform/main.tf            Streaming infrastructure
tests/test_streaming.py      Contract/processor tests
sample_data/events.jsonl     Synthetic events
```

## Run tests

```bash
python -m pip install -r requirements-dev.txt
pytest -q
```

## Production extensions

For a production platform, add enhanced fan-out where required, KMS CMKs, VPC endpoints, alarms on iterator age and throttling, a dead-letter/replay workflow, schema registry compatibility rules, autoscaling/capacity planning, centralized tracing, and cross-account data governance.
