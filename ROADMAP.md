# Implementation roadmap

The core delivery sequence is a local batch pipeline followed by an incremental lakehouse pipeline. CDC is a proposed extension. All milestones below are pending.

## 1. NYC TLC batch analytics

| Milestone | Deliverable | Acceptance criteria |
| --- | --- | --- |
| Ingestion | Python command accepting a year and month; Parquet download and source manifest | Invalid input and failed downloads produce actionable errors; a rerun handles the existing file consistently |
| Analytical model | Typed staging, trip fact, zone dimension, and daily or hourly metrics | Grain and key policy are documented; aggregates reconcile with source counts after explicit exclusions |
| Data quality | Automated checks and a small invalid fixture | Checks identify the intended defect and pass for the documented valid input |
| Reprocessing | Two-month run, single-month backfill, and repeatable checks | Reprocessing unchanged input leaves counts and aggregates unchanged |
| Delivery | Setup instructions, architecture, runtime measurements, and limitations | A clean environment can reproduce the documented results |

The initial implementation uses Python and DuckDB SQL. dbt is a possible addition once there are enough models and dependencies to benefit from its build and testing workflow.

## 2. Operational database to lakehouse

| Milestone | Deliverable | Acceptance criteria |
| --- | --- | --- |
| Source simulation | Deterministic SQLite transactions and an append-only change table | Inserts, updates, and deletes are reproducible and have an explicit event ordering |
| Extraction | Bounded Python exports and a durable checkpoint | Interrupted extraction can restart without losing committed source events |
| Delta processing | Bronze events, silver current state, and gold metrics | Replays preserve the logical target state; updates and deletes produce the expected metrics |
| Operation | Databricks Job and reconciliation queries | A failed batch can be rerun safely; final source and target state agree |
| Delivery | Setup instructions, run evidence, and documented platform limits | Another engineer can reproduce the synthetic scenario and its final state |

The source change table is an application-level simulation. Log-based CDC is reserved for the separate extension below.

## 3. Proposed CDC extension

PostgreSQL, Debezium, Kafka, and a small consumer will extend the change-processing work to database logs. The scope includes an initial snapshot, subsequent changes, consumer restart, replay, and measured source-to-sink lag. Implementation follows completion of the core pipelines.
