from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    """
    Logs heartbeat every 5 minutes.
    Also queries GraphQL hello field to verify endpoint responsiveness.
    """
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive"

    # Optional: check GraphQL endpoint with gql
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        query = gql("{ hello }")
        result = client.execute(query)

        if "hello" in result:
            message += f" (GraphQL OK: {result['hello']})"
        else:
            message += " (GraphQL FAIL)"
    except Exception as e:
        message += f" (GraphQL ERROR: {e})"

    # Append log to /tmp
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(message + "\n")
