from engine import DBConnector

def run_hub_analysis():
    # 1. Connect to the Engine
    db = DBConnector()
    if not db.connect():
        print("❌ Error: Could not connect to the Engine.")
        return
    
    # 2. Fetch the "messy" data from the database
    # We query the 'flights' collection we created earlier
    flights = db.query_records("flights", {})
    
    if not flights:
        print("⚠️ No flight records found. Run aviation_generator.py first!")
        db.close()
        return

    print("🔍 Starting Aviation Network Friction Analysis...")
    print("-" * 50)
    
    # 3. Business Logic: The Friction Index
    # Logic: Friction = (Delay * 0.7) + (Tight Connections * 0.3)
    high_friction_count = 0
    
    for f in flights:
        delay = f["operational_metrics"]["delay_minutes"]
        connections = f["passenger_impact"]["tight_connections"]
        
        # Calculate Index
        friction = (delay * 0.7) + (connections * 0.3)
        
        # Display individual flight status
        print(f"Flight {f['flight_id']} | Origin: {f['origin']} | Friction: {friction:.2f}")
        
        # Trigger Priority Alert for high-friction scenarios
        if friction > 30:
            print(f"   ⚠️ PRIORITY ALERT: High friction detected! Divert resources.")
            high_friction_count += 1

    print("-" * 50)
    print(f"🎯 ANALYSIS SUMMARY:")
    print(f"• Total Flights Analyzed: {len(flights)}")
    print(f"• High-Friction Alerts  : {high_friction_count}")
    
    db.close()

if __name__ == "__main__":
    run_hub_analysis()