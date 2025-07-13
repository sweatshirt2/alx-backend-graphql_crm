#!/usr/bin/env python3

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta
import logging

# Configure logging
log_file = "/tmp/order_reminders_log.txt"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - Order ID: %(message)s",
)

# GraphQL endpoint
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Calculate date 7 days ago
seven_days_ago = (datetime.now() - timedelta(days=7)).date().isoformat()

# Define the GraphQL query
query = gql("""
query GetRecentOrders($since: Date!) {
  orders(orderDate_Gte: $since) {
    id
    customer {
      email
    }
  }
}
""")

params = {"since": seven_days_ago}

try:
    result = client.execute(query, variable_values=params)
    for order in result.get("orders", []):
        order_id = order["id"]
        customer_email = order["customer"]["email"]
        logging.info(f"{order_id}, {customer_email}")
    print("Order reminders processed!")
except Exception as e:
    print("Error processing order reminders:", str(e))
