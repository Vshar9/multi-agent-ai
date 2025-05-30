import os
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import joblib
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from data.intent_examples import INTENT_EXAMPLES

texts, labels = [],[]
for intent, examples in INTENT_EXAMPLES.items():
    for sentence in examples:
        texts.append(sentence)
        labels.append(intent)

label_encoder = LabelEncoder()
y= label_encoder.fit_transform(labels)

model_name = "all-MiniLM-L6-v2"
sentence_model = SentenceTransformer(model_name)
X= sentence_model.encode(texts,show_progress_bar=True)

classifier =LogisticRegression(max_iter=1000)
classifier.fit(X,y)

os.makedirs("models/intent_classifier",exist_ok=True)
joblib.dump(classifier, "models/intent_classifier/classifier.joblib")
joblib.dump(label_encoder, "models/intent_classifier/label_encoder.joblib")
sentence_model.save("models/intent_classifier/sentence_model")

print("Done")
