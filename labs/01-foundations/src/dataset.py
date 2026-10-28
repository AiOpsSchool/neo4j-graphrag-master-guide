"""Synthetic dataset for the Northstar Labs training knowledge graph.

No API keys, user records, company credentials, or external data are included.
Dependencies use (consumer_service_id, provider_service_id) ordering.
"""

TENANT_ID = "northstar-demo"

SERVICES = (
    {"id": "api-gateway", "name": "API Gateway", "environment": "lab", "tenant_id": TENANT_ID},
    {"id": "checkout", "name": "Checkout", "environment": "lab", "tenant_id": TENANT_ID},
    {"id": "payments", "name": "Payments", "environment": "lab", "tenant_id": TENANT_ID},
    {"id": "inventory", "name": "Inventory", "environment": "lab", "tenant_id": TENANT_ID},
    {"id": "notification", "name": "Notification", "environment": "lab", "tenant_id": TENANT_ID},
    {"id": "auth", "name": "Authentication", "environment": "lab", "tenant_id": TENANT_ID},
)

TEAMS = (
    {"id": "platform", "name": "Platform", "tenant_id": TENANT_ID},
    {"id": "commerce", "name": "Commerce", "tenant_id": TENANT_ID},
    {"id": "supply", "name": "Supply", "tenant_id": TENANT_ID},
)

INCIDENTS = (
    {"id": "INC-001", "title": "Payments API latency", "severity": "SEV2", "tenant_id": TENANT_ID},
    {"id": "INC-002", "title": "Authentication token failures", "severity": "SEV2", "tenant_id": TENANT_ID},
)

RUNBOOKS = (
    {"id": "RB-001", "title": "Recover payments latency", "tenant_id": TENANT_ID},
    {"id": "RB-002", "title": "Restore authentication", "tenant_id": TENANT_ID},
)

# "Consumer depends on provider". Cycles are not forbidden by graph theory,
# but our training corpus is intentionally acyclic and simple to reason about.
DEPENDENCIES = (
    ("api-gateway", "checkout"),
    ("api-gateway", "auth"),
    ("checkout", "payments"),
    ("checkout", "inventory"),
    ("checkout", "auth"),
    ("payments", "auth"),
    ("notification", "payments"),
)

# (team_id, service_id)
OWNERSHIPS = (
    ("platform", "api-gateway"),
    ("platform", "auth"),
    ("platform", "notification"),
    ("commerce", "checkout"),
    ("commerce", "payments"),
    ("supply", "inventory"),
)

# (incident_id, service_id)
AFFECTED = (
    ("INC-001", "payments"),
    ("INC-002", "auth"),
)

# (runbook_id, incident_id)
MITIGATIONS = (
    ("RB-001", "INC-001"),
    ("RB-002", "INC-002"),
)
