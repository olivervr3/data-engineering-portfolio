# Roadmap and review gates

This is a sequence of deliverables, not a list of courses to finish before applying. Existing production SQL/PL/SQL experience is useful; the evidence still needed is Python, ingestion, analytical modeling, data quality, incremental processing, and operation on a modern platform.

At an initial pace of **6–8 hours a week**, use this as a provisional 12-week plan: weeks 1–2 for the first local pipeline, weeks 3–6 for modeling and reliable reruns, weeks 7–11 for the incremental lakehouse, and week 12 for documentation, interview stories, and an Associate exam decision. The review gates below control progress; a calendar date never turns incomplete work into a finished project.

## Gate 1 — A working local batch pipeline

Finish milestones 1 and 2 of [project 1](01-tlc-batch-analytics/README.md): ingest a real public dataset with Python, query it with DuckDB, model useful tables in SQL, and show checks for broken input. Keep the first end-to-end run small. Learn Python through the code you need: files, functions, dates, exceptions, CLI arguments, and tests.

## Gate 2 — A portfolio project worth discussing in an interview

Finish project 1, including a second month, rerun without duplicate results, backfill, tests, and a clear README. Add dbt **after** the plain SQL model works if its build and testing workflow improves the project. Start applying to Data Engineer I, Junior Data Engineer, Data Engineering Analyst, Analytics Engineer, and SQL-heavy ETL/ELT roles at this gate. Do not describe the projects as professional employment.

## Gate 3 — A second system with incremental behavior

Finish [project 2](02-operational-to-lakehouse/README.md): prove what happens to inserts, updates, deletes, failures, and replays. Use Databricks Free Edition for Spark, Delta, and a scheduled or manually triggered Job. Explain the source-to-target reconciliation and platform limits. This is the strongest preparation for a Databricks exam.

## Gate 4 — Specialize only when it serves a target role

[Project 3](03-cdc-streaming-optional/README.md) is optional. Build it if vacancies you want repeatedly ask for Kafka, streaming, or log-based CDC. Otherwise spend the time on applications, interviews, and improvements to projects 1 and 2.

## Certification decision

1. Use the free [Databricks Fundamentals accreditation](https://www.databricks.com/resources/learn/training/databricks-fundamentals) for a short, structured introduction.
2. Follow the free [Get Started with Databricks for Data Engineering](https://customer-academy.databricks.com/learn/courses/2469/get-started-with-databricks-for-data-engineering/lessons) lessons while building project 2.
3. Consider the paid [Data Engineer Associate](https://www.databricks.com/learn/certification/data-engineer-associate) exam after project 2 is operational and the current exam guide's domains are covered in practice. The badge supports a portfolio; it does not replace one. Leave Professional for experience running real data systems.

The [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) is a useful reference for selected modules. There is no requirement to complete it linearly before the first project. In particular, infrastructure setup is not a prerequisite for learning to ingest and validate data.

## Review protocol

For each milestone, submit the relevant commit plus: the exact run command, a sample result, the check output, what failed or was difficult, and one decision you want reviewed. The next milestone is selected after reviewing that evidence. A useful review can reject a working pipeline if it cannot be rerun or if its output cannot be reconciled with its source.
