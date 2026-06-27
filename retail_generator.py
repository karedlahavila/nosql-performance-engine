from engine import DBConnector, DataGenerator

def seed_retail_data():
    db = DBConnector()
    gen = DataGenerator()
    if not db.connect(): return
    
    db.drop_collection("retail_media")
    
    # Seeding 20 campaigns
    batch = [gen.generate_retail_media_record(f"CMP-{500+i}") for i in range(20)]
    
    db.insert_many_records("retail_media", batch)
    print(f"✅ Retail Media: {len(batch)} records seeded.")
    db.close()

if __name__ == "__main__":
    seed_retail_data()