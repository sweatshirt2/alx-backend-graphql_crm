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
