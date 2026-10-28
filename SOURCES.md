# Primary Source Ledger

**Verification/access date: 2026-10-21**

Sources below were checked against publicly accessible authoritative pages during the research phase. A document citation is evidence of a source's published guidance, **not** evidence that every local example was executed. Future editions should retain the precise package version and date for each example.

| ID | Source | Verified facts and usage | Stability/qualification |
| --- | --- | --- | --- |
| S01 | [Neo4j release notes](https://neo4j.com/release-notes/) | Release notes list Neo4j 2026.10.0 on 2026-10-20 as newest at research time | Product release changes monthly |
| S02 | [neo4j-graphrag on PyPI](https://pypi.org/project/neo4j-graphrag/) | v1.22.0 released 2026-10-01; `>=3.10,<3.15` Python compatibility; extras and history | Use fixed release page for future verification |
| S03 | [Neo4j GraphRAG source pyproject.toml](https://github.com/neo4j/neo4j-graphrag-python/blob/main/pyproject.toml) | At research time lists package 1.22.0, Python >=3.10,<3.15, Neo4j Python driver >=6.3.1,<7 | Main branch moves; verify pinned tag before final release |
| S04 | [Python 3.15.0 release](https://www.python.org/downloads/release/python-3150/) | Python 3.15.0 stable release dated 2026-10-09 | Latest Python does not imply package support |
| S05 | [Neo4j GraphRAG Python docs](https://neo4j.com/docs/neo4j-graphrag-python/current/) | Official package; older `neo4j-genai` deprecated; documented Neo4j server and Python support | Current docs can change |
| S06 | [Neo4j GraphRAG API docs](https://neo4j.com/docs/neo4j-graphrag-python/current/api.html) | `VectorRetriever`, `VectorCypherRetriever`, `HybridRetriever`, `HybridCypherRetriever`, `Text2CypherRetriever`, `GraphRAG`, `OpenAILLM` and `OpenAIEmbeddings` | API should be checked against pinned 1.22.0 code |
| S07 | [Neo4j GraphRAG RAG guide](https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_rag.html) | Official component flow, quickstart and retrieval behavior | Current guide may update imports |
| S08 | [Neo4j KG Builder guide](https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_kg_builder.html) | KG building marked experimental; `SimpleKGPipeline` under experimental path; configurable stages | Do not claim stable API/behavior |
| S09 | [Neo4j Cypher vector indexes](https://neo4j.com/docs/cypher-manual/current/indexes/search-indexes/vector-indexes/) | `CREATE VECTOR INDEX` syntax; index state; `SEARCH` preferred from 2026.01; old query procedures deprecated 2026.04 | Cypher 25 and version conditions |
| S10 | [Neo4j Cypher SEARCH](https://neo4j.com/docs/cypher-manual/current/clauses/search/) | SEARCH vector syntax, ANN behavior and version-specific filtering | Only on supported Cypher language/server versions |
| S11 | [Neo4j full-text indexes](https://neo4j.com/docs/cypher-manual/current/indexes/search-indexes/full-text-indexes/) | Full-text index creation; `SEARCH` preferred as of 2026.09 with Cypher 25 | Index scores not interchangeable with vector scores |
| S12 | [Neo4j Python driver manual](https://neo4j.com/docs/python-manual/current/query-simple/) | `Driver.execute_query`, parameters, database_, transient failure retry | Use driver v6.x validated in final implementation |
| S13 | [Neo4j Docker guide](https://neo4j.com/docs/operations-manual/current/docker/introduction/) | Versioned image `neo4j:2026.09.0`, env `NEO4J_AUTH`, volume `/data`, default Browser/Bolt ports | Lab pins documented image; 2026.10.0 image not independently verified |
| S14 | [Neo4j constraints](https://neo4j.com/docs/cypher-manual/current/schema/constraints/create-constraints/) | Unique node properties, `IF NOT EXISTS`; edition-dependent key/existence constraints | Production edition check required |
| S15 | [Neo4j backup/restore](https://neo4j.com/docs/operations-manual/current/backup-restore/restore-backup/) | Enterprise-specific restore capabilities and operational requirements | Licensing/tier dependent |
| S16 | [Neo4j developer guide](https://neo4j.com/developer/genai-ecosystem/graphrag-python/) | End-to-end library orientation and supported retrieval families | Secondary to specific API docs |

## Verified imports scheduled for Part III (not yet runtime-tested)

The official GraphRAG user guide includes imports such as:

```python
from neo4j import GraphDatabase
from neo4j_graphrag.retrievers import VectorRetriever
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.embeddings import OpenAIEmbeddings
from neo4j_graphrag.generation import GraphRAG
```

`SimpleKGPipeline` is marked experimental in the official guide:

```python
from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline
```

The baseline is to wrap experimental components behind internal interfaces and require executable integration tests before publication of chapters that depend on them.

## Open questions for subsequent research

- Confirm exact `neo4j-graphrag==1.22.0` interfaces by running against an isolated Python 3.13 environment and released source distribution, including retrieval configuration, response metadata, and async variants.
- Record the exact LLM/embedder model names, token prices, dimension configurations, provider rate-limit semantics and model version availability at the time Part III is authored.
- Confirm supported tenancy strategies and database privileges for the intended Enterprise or Aura tier, especially how document ACLs influence vector candidates.
- Confirm deployment chart, backup/restore tooling, TLS settings and upgrade strategy on a chosen production tier.
- Verify the full-text and vector `SEARCH` query mode under the chosen Neo4j 2026.x pin.
