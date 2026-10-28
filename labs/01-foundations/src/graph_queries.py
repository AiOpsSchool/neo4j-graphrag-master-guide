"""Constant, parameterized Cypher queries used by the foundational lab.

No query contains interpolated user input. Schema operations are admin-only.
Access checks here are didactic, not a substitute for database privileges.
"""

CONSTRAINTS = (
    "CREATE CONSTRAINT service_id IF NOT EXISTS FOR (s:Service) REQUIRE s.id IS UNIQUE",
    "CREATE CONSTRAINT team_id IF NOT EXISTS FOR (t:Team) REQUIRE t.id IS UNIQUE",
    "CREATE CONSTRAINT incident_id IF NOT EXISTS FOR (i:Incident) REQUIRE i.id IS UNIQUE",
    "CREATE CONSTRAINT runbook_id IF NOT EXISTS FOR (r:Runbook) REQUIRE r.id IS UNIQUE",
)

UPSERT_SERVICE = """
MERGE (s:Service {id: $id})
SET s.name = $name, s.tenant_id = $tenant_id, s.environment = $environment
"""

UPSERT_TEAM = """
MERGE (t:Team {id: $id})
SET t.name = $name, t.tenant_id = $tenant_id
"""

UPSERT_INCIDENT = """
MERGE (i:Incident {id: $id})
SET i.title = $title, i.severity = $severity, i.tenant_id = $tenant_id
"""

UPSERT_RUNBOOK = """
MERGE (r:Runbook {id: $id})
SET r.title = $title, r.tenant_id = $tenant_id
"""

LINK_DEPENDS = """
MATCH (consumer:Service {id: $consumer_id, tenant_id: $tenant_id})
MATCH (provider:Service {id: $provider_id, tenant_id: $tenant_id})
MERGE (consumer)-[:DEPENDS_ON]->(provider)
"""

LINK_OWNED = """
MATCH (team:Team {id: $team_id, tenant_id: $tenant_id})
MATCH (service:Service {id: $service_id, tenant_id: $tenant_id})
MERGE (team)-[:OWNS]->(service)
"""

LINK_AFFECTED = """
MATCH (incident:Incident {id: $incident_id, tenant_id: $tenant_id})
MATCH (service:Service {id: $service_id, tenant_id: $tenant_id})
MERGE (incident)-[:AFFECTED]->(service)
"""

LINK_MITIGATES = """
MATCH (runbook:Runbook {id: $runbook_id, tenant_id: $tenant_id})
MATCH (incident:Incident {id: $incident_id, tenant_id: $tenant_id})
MERGE (runbook)-[:MITIGATES]->(incident)
"""

# Explicit path bound and check ALL nodes, not only the endpoints.
QUERY_IMPACT = """
MATCH path = (consumer:Service)-[:DEPENDS_ON*1..3]->(target:Service {id: $service_id})
WHERE ALL(n IN nodes(path) WHERE n.tenant_id = $tenant_id)
RETURN DISTINCT consumer.id AS id, consumer.name AS name
ORDER BY id
"""

QUERY_RUNBOOKS = """
MATCH (runbook:Runbook)-[:MITIGATES]->(incident:Incident)-[:AFFECTED]->
      (service:Service {id: $service_id})
WHERE runbook.tenant_id = $tenant_id
  AND incident.tenant_id = $tenant_id
  AND service.tenant_id = $tenant_id
RETURN DISTINCT runbook.id AS id, runbook.title AS title,
                incident.id AS incident_id
ORDER BY id
"""

QUERY_COUNTS = """
MATCH (n)
WHERE n.tenant_id = $tenant_id
RETURN labels(n)[0] AS label, count(n) AS count
ORDER BY label
"""
