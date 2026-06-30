# Import JSON serialization utility
import json
# Import datetime manipulation helpers
from datetime import datetime, timedelta
# Import singleton monitor instance
from src.retention_monitor import retention_monitor

# Define verification runner function
def test_retention():
    # Print execution header
    print("=== REALATES AI SYSTEMS: CLIENT RETENTION & WIN-BACK ENGINE ===")
    
    # Capture current reference timestamp
    now = datetime.now()
    # Construct mock client account database array
    mock_clients = [
        {
            "id": "acc_01",
            "company": "Cairo Tech Solutions",
            "last_active_iso": (now - timedelta(days=3)).strftime("%Y-%m-%d"),
            "retainer": 3000
        },
        {
            "id": "acc_02",
            "company": "Riyadh Commercial Agency",
            "last_active_iso": (now - timedelta(days=18)).strftime("%Y-%m-%d"),
            "retainer": 4500
        },
        {
            "id": "acc_03",
            "company": "Dubai Law Partners",
            "last_active_iso": (now - timedelta(days=45)).strftime("%Y-%m-%d"),
            "retainer": 5000
        }
    ]

    # Print trace auditing portfolio
    print("\n--- Auditing Retainer Portfolio Health ---")
    # Execute account health audit
    results = retention_monitor.evaluate_account_health(mock_clients)
    # Iterate through audit reports
    for r in results:
        # Print formatted health summary
        print(f"[{r.health_status}] {r.company_name} ({r.days_since_last_active} days inactive) -> Action: {r.winback_trigger}")

# Execute runner if script invoked directly
if __name__ == "__main__":
    # Run test retention audit
    test_retention()
