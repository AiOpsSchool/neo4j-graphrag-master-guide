"""Offline contract checks: SQL/Cypher is not executed in this test suite."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from graph_queries import (
    CONSTRAINTS,
    LINK_DEPENDS,
    LINK_MITIGATES,
    QUERY_IMPACT,
    QUERY_RUNBOOKS,
    UPSERT_SERVICE,
)


def test_constraints_have_guard_and_unique_ids():
    assert len(CONSTRAINTS) == 4
    assert all("IF NOT EXISTS" in q and "IS UNIQUE" in q for q in CONSTRAINTS)


def test_upsert_uses_parameters_and_stable_id():
    assert "MERGE" in UPSERT_SERVICE
    for param in ("$id", "$tenant_id", "$name", "$environment"):
        assert param in UPSERT_SERVICE


def test_dependency_edge_has_explicit_semantics():
    assert "[:DEPENDS_ON]" in LINK_DEPENDS
    assert "MERGE (consumer)-[:DEPENDS_ON]->(provider)" in LINK_DEPENDS
    assert "$tenant_id" in LINK_DEPENDS


def test_impact_query_is_bounded_and_all_path_nodes_tenant_checked():
    assert "*1..3" in QUERY_IMPACT
    assert "ALL(n IN nodes(path) WHERE n.tenant_id = $tenant_id)" in QUERY_IMPACT
    assert "$service_id" in QUERY_IMPACT
    assert "RETURN DISTINCT" in QUERY_IMPACT


def test_runbooks_are_scoped_and_ordered():
    assert "[:MITIGATES]" in QUERY_RUNBOOKS
    assert "$service_id" in QUERY_RUNBOOKS
    assert "runbook.tenant_id = $tenant_id" in QUERY_RUNBOOKS
    assert "incident.tenant_id = $tenant_id" in QUERY_RUNBOOKS
    assert "service.tenant_id = $tenant_id" in QUERY_RUNBOOKS
    assert "MERGE" in LINK_MITIGATES
