# Lab 01 - Build a Service Knowledge Graph in Neo4j

**Chapter:** 4 - Neo4j Fundamentals  
**Status:** Full lab files authored; offline Python tests executed during preparation; live database steps not executed in this authoring environment.  
**Data:** Fictional Northstar Labs services, teams, incidents and runbooks.  
**Cost:** No external LLM, paid embedding API or production Neo4j service is necessary.

## Learning outcomes

- Run one-node Neo4j locally with persistent development data.
- Use application-stable IDs and unique constraints.
- Write data via parameterized Cypher with the official Python driver.
- Traverse directed service dependencies.
- Query runbooks linked to affected services.
- Show source-level validation independent of database runtime.

## Prerequisites

1. Python 3.13, Docker with the Compose plugin, and sufficient resources for a local Neo4j container.
2. Ports 7474 and 7687 on localhost not already in use.
3. A local, disposable development environment. This is **not production configuration**.

The example uses the Docker image `neo4j:2026.09.0`, the explicitly documented version tag in the Neo4j official Docker guide accessed October 21, 2026. The newest 2026.10.0 server was announced October 20, but availability of its Docker tag has not been checked for this edition.

## Files

```text
.
|-- .env.example
|-- .gitignore
|-- docker-compose.yml
|-- requirements.txt
|-- README.md
|-- src
|   |-- dataset.py
|   |-- graph_queries.py
|   |-- seed.py
|   `-- explore.py
`-- tests
    |-- test_dataset.py
    `-- test_cypher_contract.py
```

## Step 1 - Configure lab-only credentials

```bash
cp .env.example .env
```

Edit `.env` and change **both** `NEO4J_AUTH=neo4j/<password>` and `NEO4J_PASSWORD=<password>` to use the same nontrivial password. `NEO4J_AUTH` is used by the container only when initializing the database volume, and `NEO4J_PASSWORD` is used by the Python scripts. Do not commit `.env`.

## Step 2 - Start the database

```bash
docker compose up -d
docker compose ps
docker compose logs neo4j
```

Wait until Neo4j is accepting connections. Open `http://localhost:7474` and authenticate with the account configured in `.env`. By binding published ports to `127.0.0.1`, the Compose file avoids directly publishing Neo4j on all host interfaces; host firewall/VPN rules should still be reviewed in real environments.

## Step 3 - Create the Python environment

macOS/Linux:

```bash
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Windows PowerShell (after installing Python 3.13):

```powershell
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The ranges in `requirements.txt` are deliberately bounded by the official GraphRAG driver dependency range, but this initial lab does not yet ship a hash-locked production dependency file. Do not mistake installation success for a supply-chain review.

## Step 4 - Create constraints, nodes and relationships

```bash
python src/seed.py
```

Successful output resembles:

```text
INFO Seed successful; node counts in tenant northstar-demo: {'Incident': 2, 'Runbook': 2, 'Service': 6, 'Team': 3}
```

The seed operation is repeatable. Run it a second time; the number of nodes should remain the same for this untouched lab because it uses `MERGE` on stable IDs. It does not erase other data.

## Step 5 - Query dependency impact

```bash
python src/explore.py payments
```

**Expected result for the included synthetic dataset:**

```text
Potential upstream consumers of payments (max 3 hops):
  - api-gateway: API Gateway
  - checkout: Checkout
  - notification: Notification
Linked incident runbooks:
  - RB-001: Recover payments latency (incident INC-001)
```

These are *potentially impacted* consumers based on graph edges, not proof of a live outage. For the second incident, try `python src/explore.py auth` and inspect the different upstream paths and runbook.

## Step 6 - Inspect the graph in Neo4j Browser

Run each of these in Neo4j Browser:

```cypher
SHOW CONSTRAINTS;
SHOW INDEXES;
MATCH (s:Service) RETURN s ORDER BY s.id;
MATCH (a:Service)-[:DEPENDS_ON]->(b:Service)
RETURN a.name AS consumer, b.name AS provider ORDER BY consumer, provider;
EXPLAIN MATCH (s:Service {id: 'payments'}) RETURN s.name;
```

Read queries are safe for this training corpus. Avoid copy/pasting unrestricted destructive queries into databases containing non-demo data.

## Step 7 - Run offline tests

```bash
python -m pytest -q
```

The included tests validate schema relationships, source IDs, the expected 3-hop answer, and query parameterization/bounds. They run without a database connection, but `requirements.txt` includes the required `pytest` dependency.

## Troubleshooting

| Failure | Checks |
| --- | --- |
| Cannot connect to database | Confirm Compose container state; inspect Neo4j logs; verify port binding |
| Authentication error | Compare `.env` values; `NEO4J_AUTH` does not reset an existing persisted database's password |
| No rows from impact query | Check `python src/seed.py`, service ID and tenant scope |
| `ModuleNotFoundError: neo4j` | Activate virtual environment and install `requirements.txt` |
| Syntax error in Cypher | Verify Neo4j server version; run queries in the official Browser |
| Unexpected second seed result | Inspect ID uniqueness constraints and external/manual changes |

## Tear down

```bash
docker compose down
```

This leaves the named volume intact. If and only if the database is a disposable lab and you intend to erase it:

```bash
docker compose down -v
```

## Security and production notes

- The built-in `neo4j` account is only a convenience for this isolated lab. A production service needs a least-privilege account with a distinct write role for ingestion and read role for retrieval.
- The `tenant_id` property plus path filters are useful educational examples, but they are **not** an authorization boundary for real enterprise tenancy. The service-to-principal mapping and database-enforced restrictions must be designed and tested.
- No public network port exposure, secret in source code, unbounded traversal or unreviewed generated Cypher is required for this lab.
- There are no vector embeddings yet. Vector indexes and LLM generation are introduced after the foundation and architecture chapters.

## Authoritative references

- [Neo4j Docker image guide](https://neo4j.com/docs/operations-manual/current/docker/introduction/)
- [Neo4j Python driver](https://neo4j.com/docs/python-manual/current/query-simple/)
- [Neo4j constraints](https://neo4j.com/docs/cypher-manual/current/schema/constraints/create-constraints/)
- [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/current/)
