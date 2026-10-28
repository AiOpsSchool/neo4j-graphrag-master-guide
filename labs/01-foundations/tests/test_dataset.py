"""Offline unit tests for synthetic training graph semantics."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

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


def ids(rows):
    return {row["id"] for row in rows}


def upstream_consumers(service_id: str, max_depth: int) -> set[str]:
    """Oracle for a small directed graph, independent from Neo4j/Cypher."""
    frontier = {service_id}
    found = set()
    for _ in range(max_depth):
        next_frontier = {a for a, b in DEPENDENCIES if b in frontier}
        found.update(next_frontier)
        frontier = next_frontier
        if not frontier:
            break
    return found - {service_id}


def test_stable_ids_are_unique():
    for collection in (SERVICES, TEAMS, INCIDENTS, RUNBOOKS):
        assert len(ids(collection)) == len(collection)
        assert all(row["tenant_id"] == TENANT_ID for row in collection)


def test_all_relationship_endpoints_exist():
    services, teams, incidents, runbooks = map(ids, (SERVICES, TEAMS, INCIDENTS, RUNBOOKS))
    assert all(a in services and b in services for a, b in DEPENDENCIES)
    assert all(t in teams and s in services for t, s in OWNERSHIPS)
    assert all(i in incidents and s in services for i, s in AFFECTED)
    assert all(r in runbooks and i in incidents for r, i in MITIGATIONS)


def test_expected_upstream_impact():
    assert upstream_consumers("payments", 3) == {"api-gateway", "checkout", "notification"}


def test_impact_requires_reverse_direction():
    assert "payments" not in upstream_consumers("payments", 3)
    assert "auth" not in upstream_consumers("payments", 3)


def test_linked_incident_and_runbook_are_consistent():
    linked_incidents = {incident for incident, service in AFFECTED if service == "payments"}
    linked_runbooks = {runbook for runbook, incident in MITIGATIONS if incident in linked_incidents}
    assert linked_runbooks == {"RB-001"}
