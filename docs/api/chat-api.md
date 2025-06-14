# Chat API Reference

## 🌐 Overview

The OneFlow Chat API provides programmatic access to the AI-powered workflow generation system. This API allows developers to integrate AI workflow creation into their own applications or build custom interfaces.

## 🔗 Base URL

```
http://localhost:12000/api/chat
```

## 🔐 Authentication

Currently, the Chat API uses the same authentication as the main OneFlow application. Ensure you have proper session authentication or API keys configured.

## 📡 Endpoints

### Generate Workflow

Generate a new workflow based on natural language input.

**Endpoint**: `POST /api/chat/generate-workflow`

**Request Headers**:
```http
Content-Type: application/json
```

**Request Body**:
```json
{
  "message": "string",
  "current_workflow": {
    "nodes": "object",
    "links": "array"
  },
  "options": {
    "preserve_existing": "boolean",
    "max_nodes": "number",
    "preferred_style": "string"
  }
}
```

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `message` | string | Yes | Natural language description of desired workflow |
| `current_workflow` | object | No | Current workflow state for context |
| `current_workflow.nodes` | object | No | Existing nodes on the canvas |
| `current_workflow.links` | array | No | Existing connections between nodes |
| `options.preserve_existing` | boolean | No | Whether to preserve existing workflow (default: true) |
| `options.max_nodes` | number | No | Maximum number of new nodes to create (default: 10) |
| `options.preferred_style` | string | No | Preferred workflow style: "simple", "advanced", "creative" |

**Response**:

**Success (200)**:
```json
{
  "success": true,
  "workflow": {
    "operations": [
      {
        "type": "create_node",
        "node_type": "LoadImage",
        "node_id": "new_node_1",
        "position": [100, 100],
        "parameters": {
          "image": "example.png"
        }
      },
      {
        "type": "link_node",
        "source_node_id": "10",
        "target_node_id": "new_node_1",
        "source_slot": "IMAGE",
        "target_slot": "image"
      }
    ],
    "metadata": {
      "node_count": 2,
      "operation_count": 4,
      "estimated_execution_time": "5-10 seconds"
    }
  },
  "description": "This workflow loads an image and connects it to the existing node for processing.",
  "suggestions": [
    "You can adjust the image parameters in the LoadImage node",
    "Consider adding a preview node to see the results"
  ]
}
```

**Error (400)**:
```json
{
  "success": false,
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Message cannot be empty",
    "details": {
      "field": "message",
      "expected": "non-empty string"
    }
  }
}
```

**Error (500)**:
```json
{
  "success": false,
  "error": {
    "code": "AI_SERVICE_ERROR",
    "message": "Failed to generate workflow",
    "details": {
      "ai_error": "OpenAI API rate limit exceeded"
    }
  }
}
```

### Get Available Nodes

Retrieve information about available nodes for workflow generation.

**Endpoint**: `GET /api/chat/nodes`

**Query Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `category` | string | No | Filter by node category (e.g., "image", "text", "loaders") |
| `search` | string | No | Search nodes by name or description |
| `include_custom` | boolean | No | Include custom nodes (default: true) |

**Response**:

**Success (200)**:
```json
{
  "success": true,
  "nodes": [
    {
      "name": "LoadImage",
      "category": "image",
      "description": "Load an image from file",
      "inputs": [
        {
          "name": "image",
          "type": "STRING",
          "required": true,
          "description": "Path to image file"
        }
      ],
      "outputs": [
        {
          "name": "IMAGE",
          "type": "IMAGE",
          "description": "Loaded image data"
        }
      ],
      "is_custom": false
    }
  ],
  "total_count": 150,
  "categories": ["image", "text", "loaders", "conditioning", "sampling"]
}
```

### Validate Workflow

Validate a workflow before execution.

**Endpoint**: `POST /api/chat/validate-workflow`

**Request Body**:
```json
{
  "workflow": {
    "operations": [...]
  }
}
```

**Response**:

**Success (200)**:
```json
{
  "success": true,
  "valid": true,
  "warnings": [
    "Node 'new_node_1' has no output connections"
  ],
  "estimated_execution_time": "5-10 seconds"
}
```

**Validation Error (200)**:
```json
{
  "success": true,
  "valid": false,
  "errors": [
    {
      "type": "MISSING_CONNECTION",
      "message": "Node 'KSampler' requires a 'model' input",
      "node_id": "new_node_2",
      "field": "model"
    }
  ]
}
```

## 📝 Operation Types

### create_node

Creates a new node on the canvas.

```json
{
  "type": "create_node",
  "node_type": "LoadImage",
  "node_id": "unique_node_id",
  "position": [x, y],
  "parameters": {
    "param_name": "param_value"
  }
}
```

### link_node

Creates a connection between two nodes.

```json
{
  "type": "link_node",
  "source_node_id": "source_id",
  "target_node_id": "target_id",
  "source_slot": "output_name",
  "target_slot": "input_name"
}
```

### update_node

Updates parameters of an existing node.

```json
{
  "type": "update_node",
  "node_id": "existing_node_id",
  "parameters": {
    "param_name": "new_value"
  }
}
```

### delete_node

Removes a node from the canvas.

```json
{
  "type": "delete_node",
  "node_id": "node_to_delete"
}
```

## 🔧 Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| `INVALID_REQUEST` | Request format is incorrect | Check request body format and required fields |
| `EMPTY_MESSAGE` | Message field is empty | Provide a non-empty message |
| `AI_SERVICE_ERROR` | AI service is unavailable | Check OpenAI API configuration and connectivity |
| `RATE_LIMIT_EXCEEDED` | Too many requests | Wait before making additional requests |
| `WORKFLOW_VALIDATION_ERROR` | Generated workflow is invalid | Review workflow structure and node compatibility |
| `NODE_NOT_FOUND` | Referenced node doesn't exist | Verify node IDs and types |
| `CONNECTION_ERROR` | Cannot create node connection | Check data type compatibility |

## 📊 Rate Limits

| Endpoint | Limit | Window |
|----------|-------|--------|
| `/generate-workflow` | 30 requests | 1 minute |
| `/nodes` | 100 requests | 1 minute |
| `/validate-workflow` | 60 requests | 1 minute |

## 🔍 Examples

### Basic Workflow Generation

```javascript
const response = await fetch('/api/chat/generate-workflow', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: "Create a simple image generation workflow",
    options: {
      preferred_style: "simple"
    }
  })
});

const result = await response.json();
console.log(result.workflow.operations);
```

### Working with Existing Workflow

```javascript
const currentWorkflow = {
  nodes: {
    "10": {
      type: "LoadImage",
      inputs: { image: "example.png" }
    }
  },
  links: []
};

const response = await fetch('/api/chat/generate-workflow', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: "Add image editing to brighten the loaded image",
    current_workflow: currentWorkflow
  })
});
```

### Node Discovery

```javascript
const response = await fetch('/api/chat/nodes?category=image&search=edit');
const nodes = await response.json();

nodes.nodes.forEach(node => {
  console.log(`${node.name}: ${node.description}`);
});
```

## 🛠️ SDK Examples

### Python SDK

```python
import requests

class OneFlowChatAPI:
    def __init__(self, base_url="http://localhost:12000"):
        self.base_url = base_url
    
    def generate_workflow(self, message, current_workflow=None, options=None):
        payload = {"message": message}
        if current_workflow:
            payload["current_workflow"] = current_workflow
        if options:
            payload["options"] = options
        
        response = requests.post(
            f"{self.base_url}/api/chat/generate-workflow",
            json=payload
        )
        return response.json()
    
    def get_nodes(self, category=None, search=None):
        params = {}
        if category:
            params["category"] = category
        if search:
            params["search"] = search
        
        response = requests.get(
            f"{self.base_url}/api/chat/nodes",
            params=params
        )
        return response.json()

# Usage
api = OneFlowChatAPI()
result = api.generate_workflow("Create an image upscaling workflow")
print(result["description"])
```

### JavaScript SDK

```javascript
class OneFlowChatAPI {
  constructor(baseUrl = 'http://localhost:12000') {
    this.baseUrl = baseUrl;
  }
  
  async generateWorkflow(message, currentWorkflow = null, options = null) {
    const payload = { message };
    if (currentWorkflow) payload.current_workflow = currentWorkflow;
    if (options) payload.options = options;
    
    const response = await fetch(`${this.baseUrl}/api/chat/generate-workflow`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    
    return await response.json();
  }
  
  async getNodes(category = null, search = null) {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (search) params.append('search', search);
    
    const response = await fetch(`${this.baseUrl}/api/chat/nodes?${params}`);
    return await response.json();
  }
}

// Usage
const api = new OneFlowChatAPI();
const result = await api.generateWorkflow('Add text generation to my workflow');
console.log(result.workflow.operations);
```

## 🔄 Webhooks

### Workflow Completion

Register a webhook to receive notifications when workflows complete execution.

**Endpoint**: `POST /api/chat/webhooks`

**Request Body**:
```json
{
  "url": "https://your-app.com/webhook",
  "events": ["workflow.completed", "workflow.failed"],
  "secret": "your_webhook_secret"
}
```

**Webhook Payload**:
```json
{
  "event": "workflow.completed",
  "timestamp": "2024-01-15T10:30:00Z",
  "workflow_id": "workflow_123",
  "execution_time": 8.5,
  "outputs": {
    "images": ["output1.png", "output2.png"],
    "text": "Generated content..."
  }
}
```

## 📚 Best Practices

### Request Optimization
- **Batch Operations**: Combine multiple operations in a single request
- **Caching**: Cache node information to reduce API calls
- **Error Handling**: Implement retry logic with exponential backoff

### Workflow Design
- **Incremental Building**: Start with simple workflows and add complexity
- **Validation**: Always validate workflows before execution
- **Testing**: Test workflows with sample data before production use

### Performance
- **Async Processing**: Use async/await for non-blocking operations
- **Rate Limiting**: Respect API rate limits to avoid throttling
- **Monitoring**: Track API usage and performance metrics

This API reference provides comprehensive documentation for integrating with the OneFlow Chat system programmatically.