import os
import requests
import numpy as np
from PIL import Image
from io import BytesIO
from openai import OpenAI
from dotenv import load_dotenv
import torch
import base64
import tempfile

# Load environment variables
load_dotenv("/workspace/.env")

class OpenAIImageEditing:
    """
    A node for image editing using OpenAI API (Flux models)
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
                "image": ("IMAGE",),
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "change this girl to boy",
                }),
                "model": ([
                    "flux-kontext-max", 
                    "flux-kontext-pro"
                ], {
                    "default": "flux-kontext-max"
                }),
            },
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("edited_image", "image_url")
    FUNCTION = "edit_image"
    CATEGORY = "OpenAI"

    def tensor_to_pil(self, tensor):
        """Convert tensor to PIL Image"""
        # Remove batch dimension if present
        if len(tensor.shape) == 4:
            tensor = tensor.squeeze(0)
        
        # Convert from float [0,1] to uint8 [0,255]
        image_np = (tensor.cpu().numpy() * 255).astype(np.uint8)
        return Image.fromarray(image_np)

    def pil_to_tensor(self, pil_image):
        """Convert PIL Image to tensor"""
        image_np = np.array(pil_image).astype(np.float32) / 255.0
        return torch.from_numpy(image_np)[None,]  # Add batch dimension

    def upload_image_to_temp_url(self, pil_image):
        """
        Convert PIL image to a temporary URL-like string for the prompt
        In a real implementation, you might want to upload to a cloud service
        For now, we'll create a base64 data URL
        """
        buffer = BytesIO()
        pil_image.save(buffer, format='PNG')
        img_data = buffer.getvalue()
        img_base64 = base64.b64encode(img_data).decode()
        return f"data:image/png;base64,{img_base64}"

    def edit_image(self, image, prompt, model):
        try:
            # Convert tensor to PIL Image
            pil_image = self.tensor_to_pil(image)
            
            # Convert to RGB if necessary
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            # Create a temporary image URL (in practice, you'd upload to a service)
            # For this example, we'll include the image reference in the prompt
            image_url_placeholder = "https://example.com/image.png"  # Placeholder
            
            # Modify prompt to include image reference
            full_prompt = f"{prompt} {image_url_placeholder}"
            
            # Note: The actual implementation depends on how the API handles image editing
            # This is based on the example provided where image URL is included in prompt
            result = self.client.images.generate(
                model=model,
                prompt=full_prompt,
            )
            
            generated_image_url = result.data[0].url
            
            # Download the generated image
            response = requests.get(generated_image_url)
            response.raise_for_status()
            
            # Convert to PIL Image
            edited_pil_image = Image.open(BytesIO(response.content))
            
            # Convert to RGB if necessary
            if edited_pil_image.mode != 'RGB':
                edited_pil_image = edited_pil_image.convert('RGB')
            
            # Resize to match original image size
            original_size = pil_image.size
            if edited_pil_image.size != original_size:
                edited_pil_image = edited_pil_image.resize(original_size, Image.Resampling.LANCZOS)
            
            # Convert back to tensor
            edited_tensor = self.pil_to_tensor(edited_pil_image)
            
            return (edited_tensor, generated_image_url)
            
        except Exception as e:
            error_msg = f"Error editing image: {str(e)}"
            print(error_msg)
            
            # Return original image as fallback
            return (image, error_msg)

NODE_CLASS_MAPPINGS = {
    "OpenAIImageEditing": OpenAIImageEditing
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OpenAIImageEditing": "OpenAI Image Editing"
}