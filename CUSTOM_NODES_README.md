# OneFlow Custom Nodes Documentation

## Overview
This document describes the custom nodes created for OneFlow integration with OpenAI API and Alibaba Cloud OSS.

## Custom Nodes Created

### 1. OpenAI Text Generation (`openai_text_generation.py`)
- **Category**: OpenAI
- **Purpose**: Generate text using OpenAI GPT models
- **Inputs**: 
  - `prompt` (STRING): Text prompt for generation
  - `model` (STRING): Model name (default: "gpt-4.1")
  - `max_tokens` (INT): Maximum tokens to generate
  - `temperature` (FLOAT): Sampling temperature
- **Outputs**: 
  - `text` (STRING): Generated text
- **Usage**: Connect to TextShow nodes to display results

### 2. OpenAI Text to Image (`openai_text_to_image.py`)
- **Category**: OpenAI
- **Purpose**: Generate images using Flux models
- **Inputs**:
  - `prompt` (STRING): Image description prompt
  - `model` (STRING): Flux model (flux-dev, flux-pro, etc.)
- **Outputs**:
  - `image` (IMAGE): Generated image
  - `url` (STRING): Image URL
- **Usage**: Generates images from text descriptions

### 3. OpenAI Image Editing (`openai_image_editing.py`)
- **Category**: OpenAI
- **Purpose**: Edit images using Flux-kontext models
- **Inputs**:
  - `prompt` (STRING): Editing instructions with image URL
  - `model` (STRING): Flux-kontext model
- **Outputs**:
  - `image` (IMAGE): Edited image
  - `url` (STRING): Image URL
- **Usage**: Modify existing images based on text instructions

### 4. OSS Image Upload (`oss_image_upload.py`)
- **Category**: OSS
- **Purpose**: Upload images to Alibaba Cloud OSS
- **Inputs**:
  - `image` (IMAGE): Image to upload
  - `filename` (STRING): Target filename
- **Outputs**:
  - `url` (STRING): Public URL of uploaded image
- **Usage**: Store images in cloud storage

### 5. Text Show (`text_show.py`)
- **Category**: Text
- **Purpose**: Display text in the web interface
- **Inputs**:
  - `text` (STRING): Text to display
- **Outputs**:
  - `text` (STRING): Pass-through text
- **Usage**: View generated text content

### 6. Text Show Advanced (`text_show.py`)
- **Category**: Text
- **Purpose**: Advanced text display with formatting
- **Inputs**:
  - `text` (STRING): Text to display
  - `title` (STRING): Display title
- **Outputs**:
  - `text` (STRING): Pass-through text
- **Usage**: Enhanced text viewing with titles

## Environment Configuration

### Required Environment Variables (.env file)
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=your_openai_base_url

# OSS Configuration  
OSS_ACCESS_KEY_ID=your_oss_access_key
OSS_ACCESS_KEY_SECRET=your_oss_secret_key
OSS_ENDPOINT=your_oss_endpoint
OSS_BUCKET_NAME=your_bucket_name
```

## Installation and Setup

### 1. Dependencies
The following packages are automatically installed:
- `openai` - OpenAI API client
- `oss2` - Alibaba Cloud OSS SDK
- `python-dotenv` - Environment variable loading
- `requests` - HTTP requests
- `torch` - PyTorch (for image processing)
- `PIL` - Python Imaging Library

### 2. Server Startup
```bash
cd /workspace/oneflow
python main.py --listen 0.0.0.0 --port 12000 --enable-cors-header "*" --cpu
```

### 3. Web Interface
Access the OneFlow interface at: https://work-1-kzrwfothdnzshqht.prod-runtime.all-hands.dev

## Usage Examples

### Text Generation Workflow
1. Add "OpenAI Text Generation" node
2. Set prompt: "Write a story about AI"
3. Connect to "Text Show" node
4. Run workflow to see generated text

### Image Generation Workflow
1. Add "OpenAI Text to Image" node
2. Set prompt: "A beautiful landscape"
3. Connect to image viewer or save node
4. Run workflow to generate image

### Image Upload Workflow
1. Load or generate an image
2. Add "OSS Image Upload" node
3. Set filename for the upload
4. Run workflow to upload to cloud storage

## API Integration

### OpenAI API Usage
```python
from openai import OpenAI

client = OpenAI(
    api_key=openai_api_key,  
    base_url=openai_base_url
)

# Text Generation
response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": [{"type": "text", "text": "write a story"}]}]
)

# Image Generation
result = client.images.generate(
    model="flux-dev",
    prompt="A children's book drawing of a veterinarian"
)

# Image Editing
result = client.images.generate(
    model="flux-kontext-max",
    prompt="change this girl to boy https://example.com/image.png"
)
```

## Troubleshooting

### Common Issues
1. **Missing API Keys**: Ensure all environment variables are set in `.env`
2. **Import Errors**: Check that all dependencies are installed
3. **Network Issues**: Verify API endpoints are accessible
4. **CSS 404 Errors**: Fixed by creating user.css files and API route

### Server Logs
Check `/workspace/oneflow/server.log` for detailed error messages and node loading status.

### Node Loading Status
All custom nodes should load in under 1 second:
```
Import times for custom nodes:
   0.0 seconds: /workspace/oneflow/custom_nodes/text_show.py
   0.0 seconds: /workspace/oneflow/custom_nodes/openai_text_generation.py
   0.0 seconds: /workspace/oneflow/custom_nodes/openai_image_editing.py
   0.1 seconds: /workspace/oneflow/custom_nodes/oss_image_upload.py
   0.5 seconds: /workspace/oneflow/custom_nodes/openai_text_to_image.py
```

## File Structure
```
/workspace/oneflow/
├── custom_nodes/
│   ├── openai_text_generation.py
│   ├── openai_text_to_image.py
│   ├── openai_image_editing.py
│   ├── oss_image_upload.py
│   └── text_show.py
├── .env
├── server.py (modified for CSS route)
└── CUSTOM_NODES_README.md
```

## Status
✅ All 6 custom nodes successfully created and loaded
✅ Web server running on port 12000
✅ CSS 404 errors resolved
✅ All nodes accessible via web interface
✅ Environment properly configured
✅ Dependencies installed