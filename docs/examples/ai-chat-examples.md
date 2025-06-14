# AI Chat Examples

## 🎯 Overview

This document provides practical examples of using the OneFlow AI Chat Assistant to create various types of workflows. Each example includes the user prompt, expected AI response, and the resulting workflow.

## 🖼️ Image Processing Examples

### Basic Image Loading and Display

**User Prompt**: `"Load an image and display it"`

**AI Response**: 
```
I've created a simple workflow for you! This loads an image from file and displays it in a preview.

NODES: 2
STEPS: 2
```

**Generated Workflow**:
- LoadImage node
- PreviewImage node
- Connection: LoadImage.IMAGE → PreviewImage.images

**Use Case**: Basic image viewing and verification

---

### Image Enhancement

**User Prompt**: `"Make this image brighter and more colorful"`

**AI Response**:
```
I've generated a workflow that enhances your image! This takes the loaded image, applies brightness and saturation adjustments, and shows the result.

NODES: 2  
STEPS: 3
```

**Generated Workflow**:
- References existing LoadImage node (ID: 10)
- OpenAIImageEditing node with brightness/saturation parameters
- PreviewImage node for output
- Connections: LoadImage → OpenAIImageEditing → PreviewImage

**Use Case**: Quick image enhancement and color correction

---

### Image Upscaling

**User Prompt**: `"Upscale this image to make it higher resolution"`

**AI Response**:
```
I've created an upscaling workflow! This takes your image and increases its resolution using AI upscaling.

NODES: 3
STEPS: 4
```

**Generated Workflow**:
- LoadImage node
- Load Upscale Model node
- ImageUpscaleWithModel node
- SaveImage node
- Connections: LoadImage + UpscaleModel → ImageUpscaleWithModel → SaveImage

**Use Case**: Improving image resolution for printing or display

## 🎨 Image Generation Examples

### Text-to-Image Generation

**User Prompt**: `"Generate an image of a sunset over mountains"`

**AI Response**:
```
I've created an image generation workflow! This generates a beautiful sunset over mountains using AI image generation.

NODES: 4
STEPS: 5
```

**Generated Workflow**:
- OpenAITextToImage node with prompt "sunset over mountains"
- Load Checkpoint node (for model)
- KSampler node for generation
- PreviewImage node for display
- Connections: Checkpoint + Prompt → KSampler → PreviewImage

**Use Case**: Creating original artwork from text descriptions

---

### Style Transfer

**User Prompt**: `"Apply an artistic style to my image"`

**AI Response**:
```
I've generated a style transfer workflow! This applies artistic styling to your existing image while preserving the content.

NODES: 3
STEPS: 4
```

**Generated Workflow**:
- References existing LoadImage node
- OpenAIImageEditing node with style transfer parameters
- SaveImage node
- Connections: LoadImage → StyleTransfer → SaveImage

**Use Case**: Converting photos to artistic styles (painting, sketch, etc.)

## 📝 Text Processing Examples

### Text Generation

**User Prompt**: `"Generate a creative story about space exploration"`

**AI Response**:
```
I've created a text generation workflow! This generates an engaging story about space exploration using AI.

NODES: 1
STEPS: 1
```

**Generated Workflow**:
- OpenAITextGeneration node with space exploration prompt
- Output displayed in text preview

**Use Case**: Creative writing, content generation, brainstorming

---

### Image Description

**User Prompt**: `"Describe what's in this image"`

**AI Response**:
```
I've generated an image analysis workflow! This analyzes your image and provides a detailed description of its contents.

NODES: 2
STEPS: 3
```

**Generated Workflow**:
- References existing LoadImage node
- OpenAIImageAnalysis node
- Text output display
- Connections: LoadImage → ImageAnalysis → TextDisplay

**Use Case**: Accessibility, content cataloging, image understanding

## 🔄 Complex Workflow Examples

### Image-to-Image-to-Text Pipeline

**User Prompt**: `"Load an image, generate a description, then create a new image based on that description"`

**AI Response**:
```
I've created a complex multi-step workflow! This creates an image interpretation and regeneration pipeline.

NODES: 5
STEPS: 7
```

**Generated Workflow**:
1. LoadImage node (original image)
2. OpenAIImageAnalysis node (describe image)
3. OpenAITextToImage node (generate new image from description)
4. PreviewImage node (show original)
5. PreviewImage node (show generated)
6. Connections: LoadImage → Analysis → TextToImage → Preview

**Use Case**: Image interpretation, style transfer, creative reimagining

---

### Batch Image Processing

**User Prompt**: `"Process multiple images with the same enhancement settings"`

**AI Response**:
```
I've created a batch processing workflow! This applies the same enhancements to multiple images efficiently.

NODES: 4
STEPS: 6
```

**Generated Workflow**:
- LoadImageBatch node
- OpenAIImageEditing node (shared settings)
- SaveImageBatch node
- Progress monitoring
- Connections: BatchLoad → Enhancement → BatchSave

**Use Case**: Bulk photo editing, consistent processing across image sets

## 🔧 Integration Examples

### Working with Existing Workflows

**Scenario**: User has a LoadImage node (ID: 10) and wants to add processing

**User Prompt**: `"Connect to the LoadImage node and add noise reduction"`

**AI Response**:
```
I've enhanced your existing workflow! This connects to your LoadImage node (ID 10) and adds noise reduction processing.

NODES: 2
STEPS: 3
```

**Generated Workflow**:
- References existing LoadImage node (ID: 10)
- OpenAIImageEditing node with noise reduction
- PreviewImage node
- Connections: ExistingLoadImage(10) → NoiseReduction → Preview

**Use Case**: Extending existing workflows, incremental development

---

### Model-Specific Workflows

**User Prompt**: `"Create a workflow using Stable Diffusion for portrait generation"`

**AI Response**:
```
I've created a Stable Diffusion portrait workflow! This uses SD models optimized for portrait generation.

NODES: 6
STEPS: 8
```

**Generated Workflow**:
- Load Checkpoint node (Stable Diffusion model)
- CLIP Text Encode nodes (positive/negative prompts)
- KSampler node (portrait-optimized settings)
- VAE Decode node
- SaveImage node
- Connections: Model + Prompts → Sampler → VAE → Save

**Use Case**: Model-specific optimizations, professional portrait generation

## 🎛️ Parameter Customization Examples

### Advanced Sampling Settings

**User Prompt**: `"Generate an image with high quality settings and specific sampling parameters"`

**AI Response**:
```
I've created a high-quality generation workflow! This uses advanced sampling settings for superior image quality.

NODES: 5
STEPS: 7
```

**Generated Workflow**:
- Load Checkpoint node
- CLIP Text Encode nodes
- KSampler node (steps: 50, cfg: 7.5, sampler: DPM++ 2M Karras)
- VAE Decode node
- SaveImage node (high quality settings)

**Use Case**: Professional image generation, fine-tuned control

---

### Custom Resolution and Aspect Ratios

**User Prompt**: `"Create a landscape image in 16:9 aspect ratio at 1920x1080"`

**AI Response**:
```
I've created a landscape workflow with custom dimensions! This generates images in 16:9 format at 1920x1080 resolution.

NODES: 4
STEPS: 6
```

**Generated Workflow**:
- EmptyLatentImage node (1920x1080 dimensions)
- Load Checkpoint node
- KSampler node
- VAE Decode node
- Connections optimized for landscape generation

**Use Case**: Specific output requirements, display optimization

## 🔍 Troubleshooting Examples

### Connection Issues

**User Prompt**: `"The nodes aren't connecting properly"`

**AI Response**:
```
I'll help you fix the connection issues! Let me create a simple workflow that demonstrates proper node connections.

NODES: 3
STEPS: 4
```

**Generated Workflow**:
- Clear, simple node chain
- Explicit connection documentation
- Data type compatibility verification

**Use Case**: Learning proper node connections, debugging workflows

---

### Performance Optimization

**User Prompt**: `"Make this workflow run faster"`

**AI Response**:
```
I've optimized your workflow for better performance! This reduces processing time while maintaining quality.

NODES: 4 (reduced from 6)
STEPS: 5 (optimized)
```

**Generated Workflow**:
- Removed redundant nodes
- Optimized sampling settings
- Efficient data flow
- Memory usage optimization

**Use Case**: Performance tuning, resource optimization

## 📚 Learning Examples

### Beginner Workflows

**User Prompt**: `"I'm new to this, show me a simple workflow"`

**AI Response**:
```
Welcome! I've created a beginner-friendly workflow that demonstrates the basics of image processing.

NODES: 2
STEPS: 2
```

**Generated Workflow**:
- LoadImage node (with helpful parameter descriptions)
- PreviewImage node
- Clear documentation of each step

**Use Case**: Learning the system, understanding basic concepts

---

### Advanced Techniques

**User Prompt**: `"Show me advanced techniques for image generation"`

**AI Response**:
```
I've created an advanced workflow showcasing professional techniques! This demonstrates ControlNet, LoRA, and advanced sampling.

NODES: 8
STEPS: 12
```

**Generated Workflow**:
- Multiple model loading (base + LoRA)
- ControlNet integration
- Advanced sampling techniques
- Multi-stage processing

**Use Case**: Skill development, professional techniques

## 🎨 Creative Examples

### Artistic Workflows

**User Prompt**: `"Create something artistic and experimental"`

**AI Response**:
```
I've designed an experimental artistic workflow! This combines multiple AI techniques for unique creative results.

NODES: 6
STEPS: 9
```

**Generated Workflow**:
- Multi-stage generation
- Style mixing
- Creative parameter combinations
- Unexpected artistic effects

**Use Case**: Creative exploration, artistic experimentation

---

### Animation Preparation

**User Prompt**: `"Prepare images for animation"`

**AI Response**:
```
I've created an animation preparation workflow! This generates consistent frames suitable for animation.

NODES: 5
STEPS: 8
```

**Generated Workflow**:
- Consistent style settings
- Frame sequence generation
- Temporal coherence optimization
- Export formatting for animation tools

**Use Case**: Animation production, video content creation

## 💡 Tips for Effective Prompts

### Best Practices

1. **Be Specific**: "Make image brighter" vs "Increase brightness by 20%"
2. **Include Context**: "Using the existing LoadImage node..."
3. **Specify Output**: "...and save the result"
4. **Break Down Complex Tasks**: Split multi-step processes

### Common Patterns

- **"Load [type] and [action]"**: Basic processing workflows
- **"Connect to [node] and add [feature]"**: Extending existing workflows
- **"Create a workflow that [description]"**: Complete workflow generation
- **"Optimize this for [goal]"**: Performance and quality tuning

### Advanced Prompting

- **Conditional Logic**: "If the image is dark, brighten it, otherwise enhance contrast"
- **Parameter Specifications**: "Use 50 sampling steps with CFG scale 7.5"
- **Style References**: "In the style of [artist/technique]"
- **Quality Requirements**: "High quality suitable for printing"

These examples demonstrate the versatility and power of the OneFlow AI Chat Assistant. Start with simple examples and gradually explore more complex workflows as you become comfortable with the system.