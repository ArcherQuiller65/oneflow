import os
import oss2
import numpy as np
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import torch
import uuid
from datetime import datetime

# Load environment variables
load_dotenv("/workspace/.env")

class OSSImageUpload:
    """
    A node for uploading images to Alibaba Cloud OSS
    """
    
    def __init__(self):
        # Initialize OSS client
        access_key_id = os.getenv("ACCESS_KEY_ID")
        access_key_secret = os.getenv("ACCESS_KEY_SECRET")
        endpoint = os.getenv("ENDPOINT")
        bucket_name = os.getenv("BUCKET_NAME")
        
        auth = oss2.Auth(access_key_id, access_key_secret)
        self.bucket = oss2.Bucket(auth, endpoint, bucket_name)
        self.bucket_name = bucket_name
        self.endpoint = endpoint

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "filename_prefix": ("STRING", {
                    "default": "oneflow_image",
                }),
                "folder_path": ("STRING", {
                    "default": "images/",
                }),
                "image_format": (["PNG", "JPEG", "WEBP"], {
                    "default": "PNG"
                }),
                "quality": ("INT", {
                    "default": 95,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "display": "number"
                }),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "IMAGE")
    RETURN_NAMES = ("upload_url", "filename", "image")
    FUNCTION = "upload_image"
    CATEGORY = "OSS"
    OUTPUT_NODE = True

    def tensor_to_pil(self, tensor):
        """Convert tensor to PIL Image"""
        # Remove batch dimension if present
        if len(tensor.shape) == 4:
            tensor = tensor.squeeze(0)
        
        # Convert from float [0,1] to uint8 [0,255]
        image_np = (tensor.cpu().numpy() * 255).astype(np.uint8)
        return Image.fromarray(image_np)

    def upload_image(self, image, filename_prefix, folder_path, image_format, quality):
        try:
            # Convert tensor to PIL Image
            pil_image = self.tensor_to_pil(image)
            
            # Convert to RGB if saving as JPEG
            if image_format == "JPEG" and pil_image.mode in ("RGBA", "LA", "P"):
                pil_image = pil_image.convert("RGB")
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            extension = image_format.lower()
            if extension == "jpeg":
                extension = "jpg"
            
            filename = f"{filename_prefix}_{timestamp}_{unique_id}.{extension}"
            
            # Ensure folder path ends with /
            if folder_path and not folder_path.endswith('/'):
                folder_path += '/'
            
            # Full object key (path in OSS)
            object_key = f"{folder_path}{filename}"
            
            # Convert PIL image to bytes
            buffer = BytesIO()
            save_kwargs = {}
            if image_format == "JPEG":
                save_kwargs["quality"] = quality
                save_kwargs["optimize"] = True
            elif image_format == "PNG":
                save_kwargs["optimize"] = True
            elif image_format == "WEBP":
                save_kwargs["quality"] = quality
                save_kwargs["optimize"] = True
            
            pil_image.save(buffer, format=image_format, **save_kwargs)
            image_data = buffer.getvalue()
            
            # Upload to OSS
            result = self.bucket.put_object(object_key, image_data)
            
            if result.status == 200:
                # Construct the public URL
                # Remove protocol from endpoint for URL construction
                endpoint_domain = self.endpoint.replace('https://', '').replace('http://', '')
                upload_url = f"https://{self.bucket_name}.{endpoint_domain}/{object_key}"
                
                success_msg = f"Successfully uploaded to OSS: {upload_url}"
                print(success_msg)
                
                return (upload_url, filename, image)
            else:
                error_msg = f"Upload failed with status: {result.status}"
                print(error_msg)
                return (error_msg, filename, image)
                
        except Exception as e:
            error_msg = f"Error uploading image to OSS: {str(e)}"
            print(error_msg)
            return (error_msg, "upload_failed", image)

NODE_CLASS_MAPPINGS = {
    "OSSImageUpload": OSSImageUpload
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OSSImageUpload": "OSS Image Upload"
}