import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from redis_memory import RedisMemory
from typing import Dict, Any
import datetime

class EmailAgent:
    def __init__(self, redis_client: RedisMemory):
        self.redis = redis_client

    def analyze_email(self, email_data: Dict[str,Any],intent: str)->Dict[str,Any]:
        sender_name, sender_email = email_data.get("sender",(","))
        subject =email_data.get("subject","")
        body= email_data.get("body","")

        urgency =self.detect_urgency(subject+" "+body)

        formatted_email = {
            "sender_name": sender_name,
            "sender_email": sender_email,
            "subject": subject,
            "body": body,
            "intent": intent,
            "urgency": urgency
        }

        self.redis.push_to_list("email_agent_log", {
            "timestamp": datetime.datetime.now().isoformat(),
            "input": email_data,
            "output": formatted_email
        })

        self.redis.set_value("last_processed_email",formatted_email)
        return formatted_email
    
    def detect_urgency(self, text: str)->str:
        lowered = text.lower()
        if any(keyword in lowered for keyword in ["urgent","asap","immediately","priority"]):
            return "High"
        else:
            return "Normal"