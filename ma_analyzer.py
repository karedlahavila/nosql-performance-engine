from engine import DBConnector

def run_ma_analysis():
    db = DBConnector()
    if not db.connect(): return
    
    deals = db.query_records("ma_deals", {})
    
    print("💼 M&A DUE DILIGENCE: Revenue Attrition Report")
    print("-" * 60)
    
    risk_exposure = 0
    for d in deals:
        mrr = d["financials"]["mrr"]
        risk = d["risk_score"]
        
        if risk > 60:
            print(f"🚨 FLAG: {d['customer_id']} | MRR: ${mrr:,.2f} | Risk Score: {risk}/100")
            print(f"   Reason: {d['support_log']}")
            risk_exposure += mrr
            
    print("-" * 60)
    print(f"💰 Total Revenue at Risk: ${risk_exposure:,.2f}")
    db.close()

if __name__ == "__main__":
    run_ma_analysis()
