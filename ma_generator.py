from engine import DBConnector, DataGenerator

def seed_ma_data():
    db = DBConnector()
    gen = DataGenerator()
    if not db.connect(): return
    
    db.drop_collection("ma_deals")
    
    # Seeding 20 customer accounts
    batch = [gen.generate_due_diligence_record(f"CUST-{1000+i}") for i in range(20)]
    
    db.insert_many_records("ma_deals", batch)
    print(f"✅ M&A Deal Room: {len(batch)} records seeded.")
    db.close()

if __name__ == "__main__":
    seed_ma_data()