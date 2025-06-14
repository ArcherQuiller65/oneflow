# OneFlow AI Chat Assistant

## 🌊 Overview

The OneFlow AI Chat Assistant is an intelligent workflow creation tool that allows you to build complex ComfyUI workflows using natural language. Simply describe what you want to accomplish, and the AI will generate the appropriate nodes and connections for you.

## 🚀 Getting Started

### Accessing the AI Chat

1. **Open OneFlow**: Navigate to your OneFlow instance in your web browser
2. **Find the Chat Widget**: Look for the 🤖 icon in the bottom-right corner
3. **Click to Open**: Click the icon to open the AI chat interface

### Basic Usage

The AI chat widget appears as a floating panel with:
- **Chat History**: Previous conversations and generated workflows
- **Input Field**: Where you type your requests
- **Send Button**: Click ➤ or press Enter to send your message

## 💬 How to Communicate with the AI

### Natural Language Commands

The AI understands natural language descriptions of what you want to create:

```
"Generate an image of a sunset and display it"
"Create a workflow that loads an image and makes it brighter"
"Add text generation to my current workflow"
"Connect the LoadImage node to an image editing node"
```

### Workflow Integration

The AI can work with your existing workflow:
- **Analyze Current Nodes**: The AI sees what nodes you already have
- **Smart Connections**: It will connect new nodes to existing ones when appropriate
- **Preserve Your Work**: Existing nodes and connections remain intact

## 🎯 Supported Operations

### Image Processing
- **Load Images**: `"Load an image from file"`
- **Image Editing**: `"Edit this image to make it brighter/darker/more colorful"`
- **Image Generation**: `"Generate an image of [description]"`
- **Save Images**: `"Save the result as an image"`

### Text Operations
- **Text Generation**: `"Generate text about [topic]"`
- **Text Processing**: `"Create a story about cats"`
- **Prompts**: `"Create a prompt for image generation"`

### Workflow Management
- **Node Creation**: `"Add a [node type] node"`
- **Node Connections**: `"Connect [node A] to [node B]"`
- **Workflow Building**: `"Create a complete workflow for [task]"`

## 🔧 Advanced Features

### Context Awareness

The AI maintains context about your current workflow:
- **Existing Nodes**: Knows what nodes are already on your canvas
- **Available Connections**: Understands which nodes can connect to each other
- **Data Types**: Respects data type compatibility (images, text, models, etc.)

### Smart Linking

When you have existing nodes, the AI will:
- **Reference by ID**: Use existing node IDs for connections
- **Validate Compatibility**: Only suggest valid connections
- **Preserve Workflow**: Keep your existing setup intact

### Error Handling

If something goes wrong:
- **Clear Messages**: The AI explains what went wrong
- **Suggestions**: Provides alternative approaches
- **Debugging**: Detailed logs help troubleshoot issues

## 📝 Example Conversations

### Basic Image Generation
```
You: "Generate an image of a beautiful landscape"

AI: I've created a workflow for you! This generates an image of a beautiful landscape using text-to-image generation.
[Apply to Canvas] [View Details]
```

### Working with Existing Nodes
```
You: "Connect to the LoadImage node and make the image brighter"

AI: I've generated a workflow that takes the image from your existing LoadImage node (ID 10), edits it to make it brighter using OpenAI Image Editing, and previews the result.
[Apply to Canvas] [View Details]
```

### Complex Workflows
```
You: "Create a workflow that loads an image, generates a description of it, and then creates a new image based on that description"

AI: I've created a multi-step workflow that:
1. Loads an image from file
2. Analyzes it to generate a text description
3. Uses that description to generate a new image
4. Displays both the original and generated images
[Apply to Canvas] [View Details]
```

## 🎨 Workflow Application

### Applying Generated Workflows

When the AI generates a workflow:

1. **Review the Description**: Read what the AI created
2. **Check Node Count**: See how many nodes will be added
3. **Apply to Canvas**: Click "Apply to Canvas" to add the nodes
4. **Modify if Needed**: Adjust parameters or connections as desired

### Workflow Details

Click "View Details" to see:
- **Complete Node List**: All nodes that will be created
- **Connection Map**: How nodes will be linked together
- **Parameter Settings**: Default values for each node
- **Execution Order**: The sequence of operations

## 🔍 Troubleshooting

### Common Issues

**AI doesn't understand my request**
- Be more specific about what you want to accomplish
- Use clear, descriptive language
- Break complex requests into smaller steps

**Nodes aren't connecting properly**
- Check data type compatibility
- Verify node IDs in existing workflows
- Look at browser console for detailed error messages

**Workflow doesn't execute**
- Ensure all required inputs are connected
- Check that model files are available
- Verify node parameters are set correctly

### Getting Help

- **Browser Console**: Press F12 to see detailed debugging information
- **Error Messages**: The AI will explain what went wrong
- **Documentation**: Refer to node-specific documentation for details

## 🌟 Tips for Best Results

### Writing Effective Prompts

1. **Be Specific**: "Make the image brighter" vs "Adjust the image"
2. **Include Context**: "Using the existing LoadImage node, add..."
3. **Specify Output**: "...and display the result"
4. **Break Down Complex Tasks**: Split multi-step processes into parts

### Working with Existing Workflows

- **Describe Current State**: "I have a LoadImage node, now I want to..."
- **Reference Specific Nodes**: "Connect to node 10" or "Use the existing checkpoint loader"
- **Preserve Important Connections**: "Keep the current image processing chain intact"

### Iterative Development

- **Start Simple**: Begin with basic workflows
- **Add Gradually**: Build complexity step by step
- **Test Frequently**: Apply and test workflows as you build them
- **Refine**: Ask the AI to modify or improve existing workflows

## 🔗 Integration with ComfyUI

The AI Chat Assistant seamlessly integrates with ComfyUI:

- **Native Node Support**: Works with all standard ComfyUI nodes
- **Custom Node Compatibility**: Supports custom nodes like OpenAI integrations
- **Workflow Preservation**: Maintains your existing workflow structure
- **Real-time Updates**: Changes appear immediately on the canvas

## 📚 Next Steps

- **Explore Examples**: Try the example prompts provided
- **Experiment**: Test different types of requests
- **Combine Features**: Use AI chat with manual node editing
- **Share Workflows**: Export and share your AI-generated workflows

The OneFlow AI Chat Assistant makes workflow creation accessible to everyone, from beginners to advanced users. Start with simple requests and gradually explore more complex workflow generation as you become comfortable with the system.