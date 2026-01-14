# context_engineering.py
import json

class ContextEngineer:
    def __init__(self):
        pass

    def construct_prompt(self, retrieved_data):
        """
        Combines the retrieved building codes with a STRICT visual analysis prompt.
        """
        
        # Extract the text from the Vector DB result
        rules_text = retrieved_data.get("definition", "No specific rules found.")
        source = retrieved_data.get("source", "Unknown")

        # --- THE FIX IS HERE ---
        # We engineer the prompt to force the AI to identify the object BEFORE grading it.
        prompt = f"""
        You are a strict building code inspector.
        
        Reference Standards ({source}):
        {rules_text}

        YOUR TASK:
        1. IDENTIFY: Look at the image. Is there a window explicitly visible on an exterior wall? 
           - Do NOT confuse glass doors (like sauna doors), interior doors, or mirrors with windows.
           - If there is NO window, state that clearly.
        
        2. MEASURE (Visual Estimate): 
           - If a window exists, estimate the sill height (distance from floor to bottom of glass).
           - Estimate the opening width and height.

        3. EVALUATE:
           - Compare your findings against the Reference Standards above.

        OUTPUT FORMAT (JSON ONLY):
        {{
            "object_detected": "window" or "sauna_door" or "interior_door" or "none",
            "safety_verdict": "Safe for Escape" or "Safety risk violated",
            "reasoning": "Explain why based on the image features."
        }}
        """
        return prompt