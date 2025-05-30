import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from redis_memory import RedisMemory
from typing import Dict,Any
import datetime
import re
from collections import Counter

STOPWORDS = {
    "the", "and", "to", "of", "in", "a", "for", "on", "with", "as", "by", "at",
    "this", "that", "is", "are", "from", "be", "or", "an", "we", "it", "you"
}

class PdfAgent:
    def __init__(self,redis_client: RedisMemory):
        self.redis = redis_client
    
    def analyze_pdf(self,text: str, intent: str)->Dict[str,Any]:
        summary=text.strip().split("\n")[0][:500] if text else ""
        keywords = self.extract_keywords(text)

        result={
            "summary":summary,
            "keywords": keywords,
            "intent": intent
        }

        self.redis.push_to_list("pdf_agent_log",{
            "timestamp": datetime.datetime.now().isoformat(),
            "input_snippet": text[:200],
            "output": result
        })

        self.redis.set_value("last_processed_pdf",result)
        return result
    
    def extract_keywords(self,text: str,top_n:int =10)->list:
        words =re.findall(r'\b\w{4,}\b',text.lower())
        filtered_words = [word for word in words if word not in STOPWORDS]
        freq = Counter(filtered_words)
        return [word for word, _ in freq.most_common(top_n)]

