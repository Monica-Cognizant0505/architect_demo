# vector_retrieval.py
import json

class VectorDB:
    def __init__(self):
        # Simulated knowledge base
        self.knowledge_base = {
            "egress_window": {
                "keywords": ["window", "bedroom", "sleeping", "basement", "escape"],
                "data": {
                    "source": "IRC (International Residential Code)",
                    "constraints": {
                        "EGRESS_MIN_WIDTH": "20 inches",
                        "EGRESS_MIN_HEIGHT": "24 inches",
                        "MAX_SILL_HEIGHT": "44 inches",
                        "EMERGENCY_EXIT_REQ": "True"
                    },
                    "definition": "The bottom ledge of the window opening."
                }
            }
        }

    def query(self, user_text):
        user_text = user_text.lower()
        keywords = self.knowledge_base["egress_window"]["keywords"]
        
        # Simple keyword matching
        for word in keywords:
            if word in user_text:
                return self.knowledge_base["egress_window"]["data"]
        return None