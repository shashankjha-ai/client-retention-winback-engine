# ARCHITECTURE DOCUMENTATION
**Service:** Client Retention & Win-Back Engine  

## Background Auditing Engine
Designed to run as a daily background cron worker, it audits account inactivity deltas.

```mermaid
sequenceDiagram
    autonumber
    participant Cron as Daily Background Worker
    participant Eng as RetentionMonitor Engine
    participant DB as Retainer Account DB
    participant Alert as Founder Slack / WhatsApp

    Cron->>Eng: Execute Daily Portfolio Audit
    Eng->>DB: Fetch Client Last Active Timestamps
    DB-->>Eng: Account Telemetry Array
    loop For Each Client Account
        Eng->>Eng: Calculate Delta Days (Now - Last Active)
        alt Delta < 14 Days
            Eng->>Eng: Mark Status: HEALTHY
        else 14 <= Delta < 30 Days (At Risk)
            Eng->>Alert: Dispatch Automated Check-in Trigger
        else Delta >= 30 Days (Churn Risk)
            Eng->>Alert: ESCALATION: High Retainer Churn Risk
        end
    end
```
