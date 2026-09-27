# Data Engineering Portfolio

**Status: planned.** This repository is a learning and evidence trail for a move from production SQL/PL/SQL development into data engineering. A folder describes work to be built; its presence does not mean the project is complete.

The route starts with a useful local pipeline, then adds incremental processing and a managed lakehouse. Streaming is optional. Each project must be reproducible, tested, and explain its design decisions before it is marked complete.

| Order | Project | What it proves | Status |
| --- | --- | --- | --- |
| 1 | [NYC TLC batch analytics](01-tlc-batch-analytics/README.md) | Python ingestion, Parquet, SQL models, data quality, repeatable loads | Planned |
| 2 | [Operational database to lakehouse](02-operational-to-lakehouse/README.md) | Incremental extraction, Spark/Delta, orchestration, reconciliation | Planned |
| 3, optional | [Log-based CDC and streaming](03-cdc-streaming-optional/README.md) | Debezium/Kafka, replay, ordering, measured lag | Planned |

The first two projects are the portfolio core. They use distinct data sources and solve distinct problems: public trip records for batch analytics, then a **synthetic** transactional system for change processing. No employer or client data belongs here.

## How to work through this repository

1. Start with [the first project's first milestone](01-tlc-batch-analytics/README.md). Deliver a small pipeline that runs on Windows without Docker, cloud accounts, or an orchestrator.
2. Add the next capability only after the current milestone has a command to reproduce it and a check that can fail when it is broken.
3. Update the project README with the actual commands, architecture, row counts, test results, and limitations. Replace its status only when the acceptance criteria are demonstrated.
4. Open a pull request or share a commit for review. The review will check correctness, reproducibility, data quality, failure handling, and whether the documentation matches the code. Then select the next milestone.

See [ROADMAP.md](ROADMAP.md) for the skill sequence, job-search gate, and certification plan.

## Evidence standard

For each finished project, provide a short architecture diagram, source and license, a clean-run command, automated checks, one rerun or recovery demonstration, and measured output. Screenshots or a certification badge alone are not evidence that a pipeline works. Never publish secrets, raw employer data, or unlicensed private datasets.

## Source notes

- NYC TLC publishes the [trip records](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). This project is about **TLC taxi data**, not Uber internal data.
- The [Databricks Free Edition](https://docs.databricks.com/aws/en/getting-started/free-edition) is intended for learning and has [usage and network limits](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations). The second project therefore uses synthetic data and a small local export.
