from engine import DBConnector

def run_retail_analysis():
    db = DBConnector()
    if not db.connect(): return
    
    # Fetch data
    campaigns = db.query_records("retail_media", {})
    
    print("📈 RETAIL MEDIA: Campaign Performance Matrix")
    print("-" * 60)
    
    for c in campaigns:
        # Business Logic: ROAS = Total Revenue Lift / Ad Spend
        # Assuming checkout lift translates to revenue at a scale factor
        roas = (c["in_store_checkout_lift"] * 100000) / c["digital_ad_spend"]
        
        status = "✅ OPTIMIZED" if roas > 2.0 else "⚠️ UNDERPERFORMING"
        
        print(f"Campaign {c['campaign_id']} ({c['channel']}) | ROAS: ${roas:.2f} | Status: {status}")
        
    db.close()

if __name__ == "__main__":
    run_retail_analysis()