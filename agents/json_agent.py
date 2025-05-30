import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from redis_memory import RedisMemory
from typing import Dict,Any
import datetime

REQUIRED_FIELDS = ["invoice_id", "date", "amount", "customer"]

class JsonAgent:
    def __init__(self, redis_client: RedisMemory):
        self.redis = redis_client
    
    def validate_and_reformat(self, data: Dict[str,Any]) -> Dict[str,Any]:
        missing_fields = [f for f in REQUIRED_FIELDS if f not in data]
        is_valid = len(missing_fields) == 0

        reformatted = {
            "invoice_id": data.get("invoice_id", ""),
            "date": data.get("date", ""),
            "amount": data.get("amount", ""),
            "customer": data.get("customer", ""),
            "status": "valid" if is_valid else "invalid",
            "missing_fields": missing_fields,
        }

        self.redis.push_to_list("json_agent_log",{
            "timestamp": datetime.datetime.now().isoformat(),
            "input": data,
            "output": reformatted,
        })

        self.redis.set_value("last_processed_json",reformatted)
        return reformatted