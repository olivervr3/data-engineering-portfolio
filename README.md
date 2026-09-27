# Data Engineering Portfolio

Data pipeline projects covering batch analytics, incremental processing, and change data capture. The designs focus on reproducible runs, data quality, and recovery from failures.

**Current status:** project specifications are available; pipeline implementation has not started.

## Projects

| Project | Engineering problem | Planned stack | Status |
| --- | --- | --- | --- |
| [NYC TLC batch analytics](01-tlc-batch-analytics/README.md) | Build consistent trip metrics from monthly public records, with repeatable loads and backfills | Python, DuckDB, SQL, Parquet | Specification |
| [Operational database to lakehouse](02-operational-to-lakehouse/README.md) | Keep analytical tables consistent with transactional inserts, updates, and deletes | SQLite, Python, Spark, Delta Lake, Databricks | Specification |
| [Log-based CDC and streaming](03-cdc-streaming-optional/README.md) | Process database changes with defined ordering, replay behavior, and measured latency | PostgreSQL, Debezium, Kafka | Proposed extension |

## Implementation focus

The first implementation will be the NYC TLC batch pipeline. Its initial scope is a parameterized monthly ingestion command, a source manifest, and SQL queries over the downloaded data. Subsequent milestones add analytical models, quality checks, and safe reprocessing.

Each project specification describes its proposed architecture, design decisions, and acceptance criteria. Run instructions and measured results will be added alongside the implementation. The [technical roadmap](ROADMAP.md) tracks the delivery sequence.

## Data sources

The batch project uses public [NYC TLC trip records](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). The operational and CDC projects use synthetic transactions so that their input data and failure scenarios can be reproduced.
