from engine import DBConnector, DataGenerator

def seed_aviation_data():
    # 1. Initialize the tools from engine.py
    db = DBConnector()
    gen = DataGenerator()
    
    # 2. Connect to Database
    if not db.connect():
        print("❌ Could not connect to MongoDB.")
        return
    
    # 3. Clean the board (Drop old records)
    db.drop_collection("flights")
    
    # 4. Use the Factory to build 15 flight records
    batch = [gen.generate_flight_record(f"FL-{100+i}") for i in range(15)]
    
    # 5. Inject into Database
    success = db.insert_many_records("flights", batch)
    
    if success:
        print(f"✅ Successfully seeded {len(batch)} flight records into the 'flights' collection.")
    else:
        print("❌ Failed to seed data.")
        
    db.close()

if __name__ == "__main__":
    seed_aviation_data()