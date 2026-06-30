# Import datetime objects to calculate inactivity intervals
from datetime import datetime
# Import typing primitives
from typing import List, Dict, Any
# Import Pydantic v2 core primitives
from pydantic import BaseModel, Field, ConfigDict

# Define Pydantic schema representing client account health status
class ClientAccountHealth(BaseModel):
    # Enable Pydantic v2 serialization options
    model_config = ConfigDict(populate_by_name=True)
    
    # Client account ID string
    client_id: str
    # Client company name
    company_name: str
    # Elapsed inactive days count
    days_since_last_active: int
    # Monthly retainer billing value in USD
    monthly_retainer_usd: int
    # Health status classification string
    health_status: str = Field(..., description="HEALTHY, AT_RISK, or CHURNED")
    # Boolean flag indicating if intervention sequence must fire
    intervention_required: bool
    # Automated routing trigger string
    winback_trigger: str

# Define retention engine class scanning account telemetry
class ClientRetentionMonitor:
    # Initialize engine with inactivity warning threshold
    def __init__(self, churn_threshold_days: int = 14):
        # Store threshold days count
        self.churn_threshold = churn_threshold_days

    # Define evaluation method auditing client record list
    def evaluate_account_health(self, client_records: List[Dict[str, Any]]) -> List[ClientAccountHealth]:
        # Capture current reference datetime
        now = datetime.now()
        # Initialize empty list to accumulate audit reports
        reports = []

        # Iterate through active retainer client accounts
        for client in client_records:
            # Parse ISO date string into datetime object
            last_active_dt = datetime.strptime(client["last_active_iso"], "%Y-%m-%d")
            # Calculate elapsed delta in days
            delta_days = (now - last_active_dt).days
            
            # If client inactive for 30 days or more mark as churned
            if delta_days >= 30:
                status = "CHURNED"
                intervention = True
                trigger = "DISPATCH_FOUNDER_WINBACK_CALL"
            # If inactive between 14 and 29 days mark as at risk
            elif delta_days >= self.churn_threshold:
                status = "AT_RISK"
                intervention = True
                trigger = "TRIGGER_AUTOMATED_SYSTEM_CHECKIN"
            # Otherwise account is healthy
            else:
                status = "HEALTHY"
                intervention = False
                trigger = "NONE"

            # Append validated Pydantic health report
            reports.append(ClientAccountHealth(
                client_id=client["id"],
                company_name=client["company"],
                days_since_last_active=delta_days,
                monthly_retainer_usd=client.get("retainer", 2500),
                health_status=status,
                intervention_required=intervention,
                winback_trigger=trigger
            ))
        # Return complete audit list
        return reports

# Instantiate singleton monitor instance
retention_monitor = ClientRetentionMonitor()
