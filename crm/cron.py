import datetime
import requests

def log_crm_heartbeat():
    # Timestamp in DD/MM/YYYY-HH:MM:SS format
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    # Optional: Query GraphQL hello field
    graphql_status = ""
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.ok and "hello" in response.text:
            graphql_status = " (GraphQL OK)"
        else:
            graphql_status = " (GraphQL FAIL)"
    except Exception as e:
        graphql_status = f" (GraphQL ERROR: {str(e)})"

    # Log message
    log_message = f"{timestamp} CRM is alive{graphql_status}\n"

    with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
        log_file.write(log_message)

# ["from gql.transport.requests import RequestsHTTPTransport", "from gql import", "gql", "Client"]
import datetime
import requests

def update_low_stock():
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_path = "/tmp/low_stock_updates_log.txt"

    query = """
    mutation {
        updateLowStockProducts {
            updatedProducts {
                name
                stock
            }
            message
        }
    }
    """

    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": query},
            timeout=10
        )
        data = response.json()

        if response.ok and "data" in data:
            updates = data["data"]["updateLowStockProducts"]["updatedProducts"]
            message = data["data"]["updateLowStockProducts"]["message"]

            with open(log_path, "a") as log_file:
                log_file.write(f"{timestamp} - {message}\n")
                for product in updates:
                    log_file.write(f"    - {product['name']} now has stock: {product['stock']}\n")
        else:
            with open(log_path, "a") as log_file:
                log_file.write(f"{timestamp} - Failed to update low stock: {data}\n")

    except Exception as e:
        with open(log_path, "a") as log_file:
            log_file.write(f"{timestamp} - ERROR: {str(e)}\n")

# updatelowstock and logs to /tmp/lowstockupdates_log.txt
# Checks for a mutation that Queries products with stock < 10
