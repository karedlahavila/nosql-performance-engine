"""
Cloud FinOps Multi-Factor Optimizer (Day 4)
-------------------------------------------
This script cross-references Metadata (Production Tag) with 
Actual Telemetry (CPU Usage) to identify 'Zombie' cloud waste.
"""

from engine import DBConnector, DataGenerator

def inject_test_anomalies(db_helper):
    """
    Helper to inject a 'Zombie' record so the auditor always has something to find.
    """
    zombie = {
        "resource_metadata": {"instance_id": "ZOMBIE-999", "service_category": "Production-Critical"},
        "operational_metrics": {"cpu_utilization_pct": 1.2},
        "financial_layer": {"daily_cost_usd": 650.0}
    }
    db_helper.insert_many_records("cloud_assets", [zombie])
    print("✅ Injected 1 Zombie asset (High Cost/Low CPU) for audit testing.")

def run_multi_factor_analysis():
    # 1. Connect to the engine
    db_helper = DBConnector()
    if not db_helper.connect():
        print("❌ Error: Could not connect to MongoDB.")
        return

    # 2. Setup: Ensure we have data to analyze
    # Clear old audit data and inject a test case
    db_helper.drop_collection("cloud_assets")
    inject_test_anomalies(db_helper)

    print("🔍 Starting Multi-Factor Cloud FinOps Audit...")
    
    # 3. Define the Multi-Factor Logic
    # We are looking for: CPU < 5% AND Daily Cost > $500
    pipeline = [
        {
            "$match": {
                "operational_metrics.cpu_utilization_pct": {"$lt": 5.0},
                "financial_layer.daily_cost_usd": {"$gt": 500.0}
            }
        }
    ]

    # Run the query
    results = db_helper.query_records("cloud_assets", {}) # Note: Adjust if you need pipeline support
    
    # Simple manual filtering for this logic since we're using the base helper
    # (If you want to use the $match pipeline, use the collection directly)
    collection = db_helper.db["cloud_assets"]
    zombies = list(collection.aggregate([{"$match": {"operational_metrics.cpu_utilization_pct": {"$lt": 5.0}, "financial_layer.daily_cost_usd": {"$gt": 500.0}}}]))

    total_waste = 0
    for asset in zombies:
        waste = asset["financial_layer"]["daily_cost_usd"]
        total_waste += waste
        print(f"⚠️ FLAG: Asset {asset['resource_metadata']['instance_id']} is IDLE but High-Cost (${waste})")

    print("=======================================================")
    print(f"🎯 FINOPS AUDIT SUMMARY:")
    print(f"• Total Zombie Assets Identified: {len(zombies)}")
    print(f"• Daily Cost Leakage Identified : ${total_waste:,.2f}")
    print(f"• Annualized Potential Savings  : ${total_waste * 365:,.2f}")
    print("=======================================================")
    
    db_helper.close()

if __name__ == "__main__":
    run_multi_factor_analysis()