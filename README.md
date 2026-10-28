# Neo4j GraphRAG Master Guide

**Gold Standard Edition | Research baseline: 2026-10-21**

**Subtitle:** From Graph Theory and Knowledge Graphs to Production-Grade GraphRAG Applications

This is a versioned, research-grounded technical book in progress. The book covers 26 chapters, four practical capstone projects, a tested-as-possible local lab, source-verification ledgers, and production engineering workflows.

## Start here

1. Read [Book plan, coverage matrix, and architecture](BOOK_PLAN.md).
2. Read [Part I - Foundations (Chapters 1-4)](PART_I_FOUNDATIONS.md).
3. Complete [Lab 01 - Foundational knowledge graph](labs/01-foundations/README.md).
4. Review [Source ledger](SOURCES.md), [verification report](VERIFICATION.md), and [progress ledger](PROGRESS.md).

## Status and claims

- Parts I, Chapters 1-4: authored in this edition.
- Parts II-VII, Chapters 5-26: designed and planned, **not represented as complete**.
- Projects 1-4: specified and dependent on later implementation chapters, **not represented as complete**.
- Lab 01: source files, constraints, parameterized Cypher and offline tests included. Its database integration cannot be verified here because this runtime has no Docker daemon or Neo4j Python driver installed. See [verification report](VERIFICATION.md).

## Baseline

- Neo4j current release at research time: 2026.10.0 (released 2026-10-20).
- Lab Docker image: 2026.09.0, whose versioned image is explicitly documented in the official Neo4j Docker manual. The newer 2026.10.0 image availability was **not** independently verified.
- Python baseline: 3.13. The latest Python 3.15.0 is not supported by the GraphRAG package release selected here.
- Official GraphRAG package: neo4j-graphrag 1.22.0; supports Python >=3.10 and <3.15; Neo4j Python driver >=6.3.1 and <7.0.0.
- KG Builder is experimental; do not assume stable APIs without re-verification.

## Principles

**Evidence before confidence.** Claims are tied to primary sources where possible.
**Retrieval before generation.** Graph construction quality and evidence provenance matter more than expressive output.
**Authorization before context.** Never let unauthorized evidence reach a prompt.
**Build the simplest design that measures well.** GraphRAG is not always superior to keyword or vector RAG.
**No simulated results advertised as measurements.** Output examples and unexecuted code are labeled accordingly.

## Book structure

- Part I - Foundations: Chapters 1-4 (authored)
- Part II - GraphRAG Architecture: Chapters 5-7 (planned)
- Part III - Development Environment and Implementation: Chapters 8-13 (planned)
- Part IV - Advanced Retrieval and Query Engineering: Chapters 14-16 (planned)
- Part V - Production Engineering: Chapters 17-22 (planned)
- Part VI - Real-World Projects: four projects (planned)
- Part VII - Reference and Mastery: Chapters 23-26 (planned)

## License and examples

Synthetic examples in this guide use fictional companies and services. Package and API names belong to their respective owners. External documentation is linked rather than reproduced.
