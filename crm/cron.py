import requests
from datetime import datetime

def log_crm_heartbeat():
    """
    Logs heartbeat every 5 minutes.
    Optionally verifies GraphQL endpoint /hello field.
    """
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive"

    # Optional: verify GraphQL hello endpoint
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.status_code == 200 and "hello" in response.json().get("data", {}):
            message += " (GraphQL OK)"
        else:
            message += " (GraphQL FAIL)"
    except Exception:
        message += " (GraphQL ERROR)"

    # Append log to /tmp
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(message + "\n")