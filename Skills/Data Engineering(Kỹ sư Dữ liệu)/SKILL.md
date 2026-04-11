# Data Engineering (Kỹ sư Dữ liệu)

> **"Models are temporary; data pipelines are forever."**

Before there is Artificial Intelligence, there must be Data Integrity. Data Engineering is the backbone capability required to safely ingest, clean, store, and serve massive datasets. If you cannot process a terabyte of messy logs into actionable JSON in real-time, your AI models will fail. This skill provides the bedrock for "10x Delivery".

## Command Center
- **Core Mission**: Build reliable, high-throughput data pipelines that never drop events.
- **Stack Focus**: Apache Kafka (Streaming), Airflow/Prefect (Orchestration), Snowflake/BigQuery (Warehousing), Vector Databases (RAG).
- **Standard**: Elite 2026 (Real-time analytics, Data Mesh architecture).

## Mastery Chapters
1. [The Streaming Revolution](chapters/01_streaming_kafka.md) - Moving from Batch processing to Event-Driven streaming.
2. [Modern Data Warehousing](chapters/02_warehousing_dbt.md) - Using dbt (data build tool) to transform data inside the warehouse.
3. [The AI Vector Layer](chapters/03_vector_databases.md) - Architecting Pinecone/Qdrant schemas to feed LLMs with perfect context (RAG).

## Roadmap 2026
See [roadmap-2026.md](references/roadmap-2026.md) for the shift from centralized pipelines to decentralized Data Meshes.

## Core Tenets
- **Idempotency**: A data pipeline must be able to run 1,000 times and produce the exact same final state.
- **Observability**: If data is malformed at the source, the pipeline alerts the engineer before it reaches the data lake.
