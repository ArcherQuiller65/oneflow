import os
import requests
import numpy as np
from PIL import Image
from io import BytesIO
from openai import OpenAI
from dotenv import load_dotenv
import torch

# Load environment variables
load_dotenv("/workspace/.env")

class OpenAITextToImage:
    """
    A node for text-to-image generation using OpenAI API (Flux models)
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
                    "default": "A children's book drawing of a veterinarian using a stethoscope to listen to the heartbeat of a baby otter.",
                }),
                "model": ([
                    "flux-dev", 
                    "flux.1.1-pro", 
                    "flux-pro-max", 
                    "flux", 
                    "flux-pro", 
                    "flux-pro-1.1-ultra"
                ], {
                    "default": "flux-dev"
                }),
                "width": ("INT", {
                    "default": 1024,
                    "min": 256,
                    "max": 2048,
                    "step": 64,
                    "display": "number"
                }),
                "height": ("INT", {
                    "default": 1024,
                    "min": 256,
                    "max": 2048,
                    "step": 64,
                    "display": "number"
                }),
            },
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "image_url")
    FUNCTION = "generate_image"
    CATEGORY = "OpenAI"

    def generate_image(self, prompt, model, width, height):
        try:
            # Generate image using OpenAI API
            result = self.client.images.generate(
                model=model,
                prompt=prompt,
                size=f"{width}x{height}" if model in ["dall-e-3", "dall-e-2"] else None,
                n=1
            )
            
            image_url = result.data[0].url
            
            # Download the image
            response = requests.get(image_url)
            response.raise_for_status()
            
            # Convert to PIL Image
            pil_image = Image.open(BytesIO(response.content))
            
            # Convert to RGB if necessary
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            # Resize if needed (for non-DALL-E models that don't support size parameter)
            if pil_image.size != (width, height):
                pil_image = pil_image.resize((width, height), Image.Resampling.LANCZOS)
            
            # Convert PIL image to tensor format expected by ComfyUI
            image_np = np.array(pil_image).astype(np.float32) / 255.0
            image_tensor = torch.from_numpy(image_np)[None,]  # Add batch dimension
            
            return (image_tensor, image_url)
            
        except Exception as e:
            error_msg = f"Error generating image: {str(e)}"
            print(error_msg)
            
            # Return a black image as fallback
            black_image = np.zeros((height, width, 3), dtype=np.float32)
            black_tensor = torch.from_numpy(black_image)[None,]
            return (black_tensor, error_msg)

NODE_CLASS_MAPPINGS = {
    "OpenAITextToImage": OpenAITextToImage
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OpenAITextToImage": "OpenAI Text to Image"
}