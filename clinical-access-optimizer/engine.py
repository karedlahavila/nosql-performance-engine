import random
import time
from typing import Dict, List, Any, Optional
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError

class DBConnector:
    """
    Manages connections and basic CRUD operations with MongoDB.
    """
    def __init__(self, host: str = "localhost", port: int = 27017, db_name: str = "portfolio_engine"):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self) -> bool:
        try:
            connection_url = f"mongodb://{self.host}:{self.port}/"
            self.client = MongoClient(connection_url, serverSelectionTimeoutMS=3000)
            self.client.admin.command("ping")
            self.db = self.client[self.db_name]
            return True
        except ConnectionFailure:
            return False

    def insert_many_records(self, collection_name: str, dataset: List[Dict[str, Any]]) -> bool:
        if self.db is None: raise RuntimeError("Not connected.")
        try:
            self.db[collection_name].insert_many(dataset)
            return True
        except PyMongoError: return False

    def query_records(self, collection_name: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Queries database for documents matching filter criteria."""
        if self.db is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        try:
            return list(self.db[collection_name].find(query))
        except PyMongoError as e:
            print(f"❌ MongoDB Query Error: {e}")
            return []

    def drop_collection(self, collection_name: str):
        if self.db is not None: self.db[collection_name].drop()

    def close(self):
        if self.client: self.client.close()

class DataGenerator:
    """
    Enterprise Data Printing Press.
    """
    def __init__(self):
        self.patient_first_names = ["Sarah", "Michael", "Elena", "Marcus", "David", "Aaliyah"]
        self.patient_last_names = ["Smith", "Chen", "Rodriguez", "Johnson", "Patel"]
        self.low_intensity_symptoms = ["minor dry cough", "mild seasonal allergies", "minor paper cut"]
        self.high_intensity_symptoms = ["acute substernal chest pain", "severe compound bone fracture"]
        self.cloud_providers = ["AWS", "GoogleCloud", "Azure"]
        self.instance_types = ["t3.medium", "m5.large", "r5.2xlarge"]
        self.departments = ["Engineering", "FinTech-Core", "AI-Inference-Layer"]
        self.cloud_services = ["EC2", "RDS", "S3", "KubernetesPod"]
        self.saas_industries = ["Retail", "FinTech", "Healthcare", "EdTech"]
        self.churn_indicators = ["System is too slow.", "Pricing increased.", "UI is confusing."]

    def generate_payment_integrity_record(self, record_id: int) -> Dict[str, Any]:
        return {
            "record_id": record_id,
            "patient_metadata": {"name": f"{random.choice(self.patient_first_names)} {random.choice(self.patient_last_names)}"},
            "ehr_clinical_document": {"unstructured_chart_note": "Routine visit.", "semantic_vector_embedding": [0.1, -0.2, 0.5]},
            "billing_claim_submitted": {"billed_cpt_code": "99215", "charged_amount": 1200.0}
        }

    def generate_finops_log(self, record_id: int) -> Dict[str, Any]:
        return {
            "record_id": record_id,
            "cloud_provider": random.choice(self.cloud_providers),
            "resource_metadata": {"instance_id": f"i-{random.randint(1000, 9999)}", "service_category": random.choice(self.cloud_services)},
            "operational_metrics": {"cpu_utilization_pct": random.uniform(1.0, 95.0)},
            "financial_layer": {"daily_cost_usd": random.uniform(0.12, 500.0)}
        }

    def generate_commercial_due_diligence_record(self, record_id: int) -> Dict[str, Any]:
        return {
            "record_id": record_id,
            "customer_company_name": f"{random.choice(self.patient_last_names)} Global",
            "saas_financial_metrics": {"monthly_recurring_revenue_mrr": random.uniform(1500, 25000)},
            "support_and_sentiment_analysis": {"raw_ticket_text": random.choice(self.churn_indicators)}
        }

    # NEW: Aviation Project Method
    def generate_flight_record(self, flight_id: str) -> Dict[str, Any]:
        """Generates a synthetic flight record for the Aviation Network."""
        hubs = ["JFK", "ATL", "ORD", "DFW"]
        return {
            "flight_id": flight_id,
            "origin": random.choice(hubs),
            "operational_metrics": {"delay_minutes": random.choice([0, 15, 45, 120])},
            "passenger_impact": {"tight_connections": random.randint(0, 50)}
        }
    def generate_retail_media_record(self, campaign_id: str) -> Dict[str, Any]:
        """Generates cross-channel retail media attribution data."""
        return {
            "campaign_id": campaign_id,
            "digital_ad_spend": round(random.uniform(500.0, 5000.0), 2),
            "in_store_checkout_lift": round(random.uniform(0.01, 0.15), 4),
            "channel": random.choice(["Social", "Search", "Display"]),
            "omnichannel_cac": round(random.uniform(10.0, 50.0), 2)
        }

    def generate_due_diligence_record(self, customer_id: str) -> Dict[str, Any]:
        """Generates SaaS revenue metrics and support ticket sentiment."""
        mrr = round(random.uniform(2000.0, 30000.0), 2)
        return {
            "customer_id": customer_id,
            "financials": {"mrr": mrr, "dso": random.randint(15, 60)},
            "support_log": random.choice(self.churn_indicators),
            "risk_score": random.randint(10, 90)
        }
        