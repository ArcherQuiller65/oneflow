import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv("/workspace/.env")

class OpenAITextGeneration:
    """
    A node for text generation using OpenAI API
    """
    
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "Write a story",
                }),
                "model": (["gpt-4.1", "gpt-4", "gpt-3.5-turbo"], {
                    "default": "gpt-4.1"
                }),
                "max_tokens": ("INT", {
                    "default": 1000,
                    "min": 1,
                    "max": 4096,
                    "step": 1,
                    "display": "number"
                }),
                "temperature": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                    "display": "number"
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("generated_text",)
    FUNCTION = "generate_text"
    CATEGORY = "OpenAI"

    def generate_text(self, prompt, model, max_tokens, temperature):
        try:
            response = self.client.chat.completions.create(
                model=model,
                stream=False,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                        ]
                    }
                ]
            )
            
            generated_text = response.choices[0].message.content
            return (generated_text,)
            
        except Exception as e:
            error_msg = f"Error generating text: {str(e)}"
            print(error_msg)
            return (error_msg,)

NODE_CLASS_MAPPINGS = {
    "OpenAITextGeneration": OpenAITextGeneration
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OpenAITextGeneration": "OpenAI Text Generation"
}