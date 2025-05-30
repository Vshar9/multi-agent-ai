import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import joblib
from sentence_transformers import SentenceTransformer
from redis_memory import RedisMemory


MODEL_PATH = "models/intent_classifier/classifier.joblib"
ENCODER_PATH = "models/intent_classifier/label_encoder.joblib"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

class ClassifierAgent:
    def __init__(self, redis_client: RedisMemory):
        self.redis = redis_client
        self.model = joblib.load(MODEL_PATH)
        self.label_encoder = joblib.load(ENCODER_PATH)
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    
    def classify_intent(self, text: str) -> str:
        embedding = self.embedding_model.encode([text])
        predicted_label_index = self.model.predict(embedding)[0]
        predicted_label = self.label_encoder.inverse_transform([predicted_label_index])[0]

        self.redis.set_value("last_intent", {"intent": predicted_label})

        self.redis.push_to_list("intent_log", {
            "input": text,
            "predicted_intent": predicted_label
        })

        return predicted_label
