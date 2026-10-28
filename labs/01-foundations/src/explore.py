"""Explore possible upstream dependency impact and linked incident runbooks.

Use: python src/explore.py payments
"""

import argparse
import logging
import sys

from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

from dataset import TENANT_ID
from graph_queries import QUERY_IMPACT, QUERY_RUNBOOKS
from seed import environment

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main() -> int:
    parser = argparse.ArgumentParser(description="Query a synthetic service dependency graph")
    parser.add_argument("service_id", nargs="?", default="payments")
    args = parser.parse_args()
    try:
        uri, user, password, database = environment()
        with GraphDatabase.driver(uri, auth=(user, password)) as driver:
            driver.verify_connectivity()
            records, _, _ = driver.execute_query(
                QUERY_IMPACT,
                parameters_={"service_id": args.service_id, "tenant_id": TENANT_ID},
                database_=database,
            )
            runbooks, _, _ = driver.execute_query(
                QUERY_RUNBOOKS,
                parameters_={"service_id": args.service_id, "tenant_id": TENANT_ID},
                database_=database,
            )
        print(f"Potential upstream consumers of {args.service_id} (max 3 hops):")
        if records:
            for row in records:
                print(f"  - {row['id']}: {row['name']}")
        else:
            print("  (none recorded or service not found)")
        print("Linked incident runbooks:")
        if runbooks:
            for row in runbooks:
                print(f"  - {row['id']}: {row['title']} (incident {row['incident_id']})")
        else:
            print("  (none linked)")
        return 0
    except (ValueError, Neo4jError, OSError) as exc:
        logger.error("Query failed (%s). Check database connectivity and permissions.", type(exc).__name__)
        return 1


if __name__ == "__main__":
    sys.exit(main())
