# vision_execution.py
import base64
from openai import AzureOpenAI
import streamlit as st 

class VisionAgent:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=config.AZURE_API_KEY,
            api_version=config.API_VERSION,
            azure_endpoint=config.AZURE_ENDPOINT
        )

    def analyze(self, image_bytes, engineered_prompt):
        # Encode image to Base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        try:
            response = self.client.chat.completions.create(
                model=config.DEPLOYMENT_NAME,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a safety compliance AI."
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": engineered_prompt},
                            {
                                "type": "image_url", 
                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error contacting Azure OpenAI: {str(e)}"
