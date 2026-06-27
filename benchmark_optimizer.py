import time
from engine import DBConnector, DataGenerator

def run_performance_benchmark():
    db_helper = DBConnector(host="localhost", port=27017, db_name="portfolio_engine")
    generator = DataGenerator()
    collection_name = "patient_records"
    target_record_id = 99998  
    
    print("=============================================================")
    print("🔌 Step 1: Establishing connection to MongoDB...")
    if not db_helper.connect():
        print("❌ Connection Failed. Check if MongoDB is running on port 27017!")
        return
    print("✅ Connection Established Successfully!")
    print("=============================================================")

    try:
        print(f"🧹 Step 2: Purging historical collections to guarantee clean test metrics...")
        db_helper.drop_collection(collection_name)
        print("✅ Environment wiped clean.")
        print("=============================================================")

        num_records = 100000
        print(f"📦 Step 3: Generating {num_records:,} highly randomized patient documents...")
        start_gen = time.time()
        records = [generator.generate_healthcare_record(i) for i in range(1, num_records + 1)]
        gen_duration = time.time() - start_gen
        print(f"✅ Generated in {gen_duration:.2f} seconds.")
        
        print(f"🚀 Batch-inserting records into MongoDB...")
        start_insert = time.time()
        success = db_helper.insert_many_records(collection_name, records)
        insert_duration = time.time() - start_insert
        
        if not success:
            print("❌ Batch insertion failed.")
            return
        print(f"✅ Batch Insertion completed in {insert_duration:.2f} seconds!")
        print("=============================================================")

        print(f"🔍 Step 4: Measuring unindexed lookup (COLLSCAN) for Record ID: {target_record_id}...")
        query_filter = {"record_id": target_record_id}
        iterations = 5
        unindexed_times = []
        result = None
        
        for _ in range(iterations):
            start_query = time.time()
            result = db_helper.query_records(collection_name, query_filter)
            unindexed_times.append(time.time() - start_query)
            
        avg_unindexed_ms = (sum(unindexed_times) / len(unindexed_times)) * 1000
        print(f"📋 Query Record Selected: {result[0]['patient_metadata']['name'] if result else 'None'}")
        print(f"⏱️ Unindexed Query Time (COLLSCAN): {avg_unindexed_ms:.3f} ms (Avg of {iterations} runs)")
        print("=============================================================")

        print(f"⚡ Step 5: Optimization Action - Compiling B-Tree index on field 'record_id'...")
        start_index = time.time()
        index_name = db_helper.create_collection_index(collection_name, "record_id")
        index_duration = (time.time() - start_index) * 1000
        print(f"✅ Index created: '{index_name}' in {index_duration:.2f} ms")
        print("=============================================================")

        print(f"🚀 Step 6: Measuring indexed lookup (IXSCAN) for Record ID: {target_record_id}...")
        indexed_times = []
        
        for _ in range(iterations):
            start_query = time.time()
            result = db_helper.query_records(collection_name, query_filter)
            indexed_times.append(time.time() - start_query)
            
        avg_indexed_ms = (sum(indexed_times) / len(indexed_times)) * 1000
        print(f"⏱️ Indexed Query Time (IXSCAN): {avg_indexed_ms:.3f} ms (Avg of {iterations} runs)")
        print("=============================================================")

        speedup = ((avg_unindexed_ms - avg_indexed_ms) / avg_unindexed_ms) * 100
        print("📊 PERFORMANCE OPTIMIZATION METRICS REPORT:")
        print(f"  • Raw Table Lookup (COLLSCAN) : {avg_unindexed_ms:.3f} ms")
        print(f"  • Optimized Lookup (IXSCAN)   : {avg_indexed_ms:.3f} ms")
        print(f"  • Latency Reduction           : {speedup:.2f}% faster query speed")
        print("=============================================================")

    finally:
        db_helper.close()
        print("🔌 Connection closed safely.")

if __name__ == "__main__":
    run_performance_benchmark()
