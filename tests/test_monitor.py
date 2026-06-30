# Import datetime helper
from datetime import datetime, timedelta
# Import pytest framework
import pytest
# Import singleton monitor instance
from src.retention_monitor import retention_monitor

# Define test function verifying account health classification deltas
def test_account_health_classification():
    now = datetime.now()
    sample = [
        {"id": "1", "company": "Healthy Corp", "last_active_iso": (now - timedelta(days=2)).strftime("%Y-%m-%d"), "retainer": 2000},
        {"id": "2", "company": "Risk Corp", "last_active_iso": (now - timedelta(days=15)).strftime("%Y-%m-%d"), "retainer": 3000},
        {"id": "3", "company": "Churn Corp", "last_active_iso": (now - timedelta(days=35)).strftime("%Y-%m-%d"), "retainer": 5000}
    ]
    res = retention_monitor.evaluate_account_health(sample)
    assert res[0].health_status == "HEALTHY"
    assert res[1].health_status == "AT_RISK"
    assert res[2].health_status == "CHURNED"
    assert res[2].winback_trigger == "DISPATCH_FOUNDER_WINBACK_CALL"
