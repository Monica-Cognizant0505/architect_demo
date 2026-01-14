import os
import base64
from openai import AzureOpenAI

class VisionAgent:
    def __init__(self):
        # We use os.getenv to read the keys you put in Streamlit Secrets
        # Make sure the string inside getenv matches exactly what you wrote in Secrets
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_API_KEY"), 
            api_version=os.getenv("API_VERSION", "2024-12-01-preview"),
            azure_endpoint=os.getenv("AZURE_ENDPOINT")
        )
        self.deployment_name = os.getenv("DEPLOYMENT_NAME", "gpt-4o")

    def analyze(self, image_bytes, prompt):
        if not image_bytes:
            return "No image provided."

        # Convert image bytes to base64 string
        base64_image = base64.b64encode(image_bytes).decode('utf-8')

        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=800
        )
        
        return response.choices[0].message.content
