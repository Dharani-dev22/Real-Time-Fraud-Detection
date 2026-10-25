import time
import json
import random
import os
import uuid
from datetime import datetime

os.makedirs("live_transactions", exist_ok=True)
users = [f"USER_{i}" for i in range(1, 100)]
merchants = ["Retail", "Online", "Travel", "Dining", "Crypto", "Gaming"]
locations = ["Mumbai", "Delhi", "Bangalore", "New York", "London", "Dubai"]

while True:
    transaction = {
        "tx_id": uuid.uuid4().hex,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": random.choice(users),
        "amount": round(random.uniform(5.0, 8000.0), 2),
        "merchant": random.choice(merchants),
        "location": random.choice(locations)
    }
    filename = f"live_transactions/tx_{transaction['tx_id']}.json"
    with open(filename, "w") as f:
        json.dump(transaction, f)
    time.sleep(0.1) # Generates 10 transactions per second