import json
import os

PROCESSED_IDS_FILE = "storage/processed_ids.json"

def load_processed_ids():
    if not os.path.exists(PROCESSED_IDS_FILE):
        return set()
    with open(PROCESSED_IDS_FILE, "r") as f:
        return set(json.load(f))

def save_processed_ids(processed_ids):
    with open(PROCESSED_IDS_FILE, "w") as f:
        json.dump(list(processed_ids), f)