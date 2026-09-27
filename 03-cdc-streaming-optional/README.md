# Project 3 — Log-based CDC and streaming (optional)

**Status: optional and planned.** Build this only after projects 1 and 2 if target jobs repeatedly require Kafka, streaming, or CDC. It introduces substantially more infrastructure and should answer a real engineering question: how quickly and reliably can changes from a transactional database reach an analytical sink?

Use PostgreSQL, [Debezium](https://debezium.io/documentation/reference/stable/tutorial.html), Kafka, and a small consumer. Unlike project 2's synthetic change table, Debezium reads database changes through a connector. Use generated data only. Document the container setup and its Windows prerequisites before implementation.

## Required demonstrations

- An initial snapshot followed by inserts, updates, and deletes.
- A consumer restart and event replay without an incorrect final state.
- Defined message key, ordering boundary, offset/checkpoint strategy, and duplicate handling.
- Measured source-to-sink lag for a reproducible sample workload, plus a failure and recovery walkthrough.

**Done when:** the complete stack can be started from a clean machine, each event type has a check, and the reported latency includes the measurement method. A running Kafka container alone is not a finished data pipeline.
