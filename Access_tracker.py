"""
Specialty Drug Onboarding & Access Tracker (Project 2)
-----------------------------------------------------
Analyzes insurance denials and calculates time-to-treatment.
"""

from engine import DBConnector
import datetime

class AccessTracker:
    def __init__(self):
        self.db_helper = DBConnector()
        self.collection = "onboarding_funnel"

    def process_denial_letter(self, patient_id, denial_text):
        """
        AI Logic: Extract rejection reason from unstructured text.
        In a real app, this would use a library like SpaCy or an OpenAI API.
        """
        denial_text = denial_text.lower()
        if "missing clinical documentation" in denial_text:
            return "Documentation Incomplete"
        elif "prior authorization" in denial_text:
            return "Auth Required"
        return "Unknown Denial"

    def onboard_patient(self, patient_id, drug_name, status="Pending"):
        record = {
            "patient_id": patient_id,
            "drug_name": drug_name,
            "status": status,
            "start_date": datetime.datetime.now(),
            "denial_reason": None
        }
        self.db_helper.insert_record(self.collection, record)
        return record

# --- Demonstration Logic ---
if __name__ == "__main__":
    tracker = AccessTracker()
    tracker.db_helper.connect()
    tracker.db_helper.drop_collection("onboarding_funnel") # Start clean for demo

    # 1. Simulate Patient Onboarding
    patient = tracker.onboard_patient("PAT-001", "OncoLife-Biologic")
    
    # 2. Simulate Receiving a Denial Letter
    raw_denial = "Claim rejected due to Missing Clinical Documentation for authorization."
    reason = tracker.process_denial_letter("PAT-001", raw_denial)
    
    # 3. Update the record
    tracker.db_helper.db["onboarding_funnel"].update_one(
        {"patient_id": "PAT-001"},
        {"$set": {"status": "Denied", "denial_reason": reason}}
    )

    print(f"✅ Onboarding record created for {patient['drug_name']}")
    print(f"⚠️ Denial detected for PAT-001: {reason}")
    print("=======================================================")
    print("🎯 ONBOARDING KPI SUMMARY:")
    print(f"• Patient: {patient['patient_id']}")
    print(f"• Status : Denied (Action Required)")
    print(f"• Resolution Goal: < 24 Hours")
    print("=======================================================")