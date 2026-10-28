"""Idempotently seed the synthetic foundational Neo4j graph.

Use: python src/seed.py
Requires a running Neo4j container, .env, and requirements.txt installed.
The seed job is administrative and creates database uniqueness constraints.
"""

import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

from dataset import (
    AFFECTED,
    DEPENDENCIES,
    INCIDENTS,
    MITIGATIONS,
    OWNERSHIPS,
    RUNBOOKS,
    SERVICES,
    TEAMS,
    TENANT_ID,
)
from graph_queries import (
    CONSTRAINTS,
    LINK_AFFECTED,
    LINK_DEPENDS,
    LINK_MITIGATES,
    LINK_OWNED,
    QUERY_COUNTS,
    UPSERT_INCIDENT,
    UPSERT_RUNBOOK,
    UPSERT_SERVICE,
    UPSERT_TEAM,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def environment() -> tuple[str, str, str, str]:
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
    required = ("NEO4J_URI", "NEO4J_USER", "NEO4J_PASSWORD", "NEO4J_DATABASE")
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    return tuple(os.environ[key] for key in required)  # type: ignore[return-value]


def write_graph(driver, database: str) -> None:
    for statement in CONSTRAINTS:
        driver.execute_query(statement, database_=database)
    for rows, statement in (
        (SERVICES, UPSERT_SERVICE),
        (TEAMS, UPSERT_TEAM),
        (INCIDENTS, UPSERT_INCIDENT),
        (RUNBOOKS, UPSERT_RUNBOOK),
    ):
        for row in rows:
            driver.execute_query(statement, parameters_=row, database_=database)

    for consumer_id, provider_id in DEPENDENCIES:
        driver.execute_query(
            LINK_DEPENDS,
            parameters_={
                "consumer_id": consumer_id, "provider_id": provider_id,
                "tenant_id": TENANT_ID,
            },
            database_=database,
        )
    for team_id, service_id in OWNERSHIPS:
        driver.execute_query(
            LINK_OWNED,
            parameters_={"team_id": team_id, "service_id": service_id, "tenant_id": TENANT_ID},
            database_=database,
        )
    for incident_id, service_id in AFFECTED:
        driver.execute_query(
            LINK_AFFECTED,
            parameters_={"incident_id": incident_id, "service_id": service_id, "tenant_id": TENANT_ID},
            database_=database,
        )
    for runbook_id, incident_id in MITIGATIONS:
        driver.execute_query(
            LINK_MITIGATES,
            parameters_={"runbook_id": runbook_id, "incident_id": incident_id, "tenant_id": TENANT_ID},
            database_=database,
        )

    records, _, _ = driver.execute_query(
        QUERY_COUNTS, parameters_={"tenant_id": TENANT_ID}, database_=database
    )
    counts = {row["label"]: row["count"] for row in records}
    expected = {"Service": 6, "Team": 3, "Incident": 2, "Runbook": 2}
    for label, minimum in expected.items():
        if counts.get(label, 0) < minimum:
            raise RuntimeError(f"Seed incomplete: expected at least {minimum} {label} nodes, got {counts.get(label, 0)}")
    logger.info("Seed successful; node counts in tenant %s: %s", TENANT_ID, counts)


def main() -> int:
    try:
        uri, user, password, database = environment()
        with GraphDatabase.driver(uri, auth=(user, password)) as driver:
            driver.verify_connectivity()
            write_graph(driver, database)
        return 0
    except (ValueError, Neo4jError, OSError, RuntimeError) as exc:
        # Do not echo a connection string, password or provider credentials.
        logger.error("Unable to seed graph (%s). Check container, auth, schema and logs.", type(exc).__name__)
        return 1


if __name__ == "__main__":
    sys.exit(main())
