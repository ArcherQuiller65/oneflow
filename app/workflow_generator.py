"""
Workflow Generator Service
Uses GPT-4.1 to convert user requests into structured workflow instructions
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv
from .node_info_collector import NodeInfoCollector

# Load environment variables
load_dotenv("/workspace/.env")

class WorkflowAtom:
    """Atomic primitive for workflow operations"""
    
    def __init__(self, operation: str, **kwargs):
        self.operation = operation
        self.params = kwargs
    
    def to_dict(self):
        return {
            "operation": self.operation,
            "params": self.params
        }

class WorkflowGenerator:
    """Generates workflows using GPT-4.1 based on user requirements"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )
        self.node_collector = NodeInfoCollector()
        self.logger = logging.getLogger(__name__)
        
        # Cache node information
        self.nodes_info = self.node_collector.get_all_nodes_info()
        self.nodes_info_formatted = self.node_collector.format_for_gpt(self.nodes_info)
    
    def create_system_prompt(self) -> str:
        """Create the system prompt for GPT-4.1"""
        return f"""You are an AI workflow designer for OneFlow, a ComfyUI-based system. Your task is to convert user requirements into structured workflow instructions using available custom nodes.

{self.nodes_info_formatted}

## Workflow Generation Rules:

1. **Node Selection**: Only use nodes from the available custom nodes list above
2. **Data Flow**: Ensure correct connections between nodes (image->image, text->text, etc.)
3. **Parameter Passing**: Set reasonable default parameters for each node
4. **Workflow Logic**: Create logical sequences that fulfill user requirements
5. **Minimal Complexity**: Use only necessary nodes to achieve the goal
6. **Text Rendering**: If you want to render text, you MUST use "TextToImageDisplay" node followed by a "PreviewImage" node
7. **Image Editing**: For image modification requests, use "OpenAIImageEditing" node (which has built-in image upload) followed by "PreviewImage" node
8. **Context Awareness**: If current workflow context is provided, modify existing workflows instead of creating new ones when appropriate
9. **Existing Node Integration**: When current workflow contains relevant nodes, connect new nodes to existing ones instead of creating isolated workflows
10. **Node ID Preservation**: When referencing existing nodes from current workflow, use their exact node IDs (e.g., "1", "2", etc.)

## Output Format:

You must respond with a JSON object containing a "workflow" array of atomic operations. Each operation should be one of:

### add_node(node_id, node_params, position)
Adds a node to the workflow
- node_id: The ID of the node from the available nodes list
- node_params: Dictionary of parameters for the node (use defaults from node specs)
- position: {{x: number, y: number}} for UI positioning

### link_node(source_node_id, source_output, target_node_id, target_input)
Links two nodes together
- source_node_id: ID of the source node
- source_output: Name of the output from source node
- target_node_id: ID of the target node  
- target_input: Name of the input on target node

### set_param(node_id, param_name, param_value)
Sets a parameter on a node
- node_id: ID of the node
- param_name: Name of the parameter
- param_value: Value to set

## Example Response Format:
```json
{{
  "workflow": [
    {{
      "operation": "add_node",
      "params": {{
        "node_id": "OpenAITextGeneration",
        "node_params": {{
          "prompt": "Write a story about a cat",
          "model": "gpt-4.1",
          "max_tokens": 1000,
          "temperature": 0.7
        }},
        "position": {{"x": 100, "y": 100}}
      }}
    }},
    {{
      "operation": "add_node", 
      "params": {{
        "node_id": "TextToImageDisplay",
        "node_params": {{
          "text": "",
          "width": 800,
          "height": 400,
          "font_size": 24,
          "background_color": "white",
          "text_color": "black",
          "padding": 20
        }},
        "position": {{"x": 400, "y": 100}}
      }}
    }},
    {{
      "operation": "add_node", 
      "params": {{
        "node_id": "PreviewImage",
        "node_params": {{}},
        "position": {{"x": 700, "y": 100}}
      }}
    }},
    {{
      "operation": "link_node",
      "params": {{
        "source_node_id": "OpenAITextGeneration",
        "source_output": "generated_text",
        "target_node_id": "TextToImageDisplay", 
        "target_input": "text"
      }}
    }},
    {{
      "operation": "link_node",
      "params": {{
        "source_node_id": "TextToImageDisplay",
        "source_output": "image",
        "target_node_id": "PreviewImage", 
        "target_input": "images"
      }}
    }}
  ],
  "description": "This workflow generates a story using OpenAI, converts it to an image using TextToImageDisplay, and displays it using PreviewImage."
}}
```

## Example: Connecting to Existing Nodes
If current workflow has a LoadImage node with ID "1", and user asks to edit the image:
```json
{{
  "workflow": [
    {{
      "operation": "add_node",
      "params": {{
        "node_id": "OpenAIImageEditing",
        "node_params": {{
          "prompt": "Make this image brighter",
          "model": "flux-kontext-max"
        }},
        "position": {{"x": 300, "y": 100}}
      }}
    }},
    {{
      "operation": "add_node",
      "params": {{
        "node_id": "PreviewImage",
        "node_params": {{}},
        "position": {{"x": 600, "y": 100}}
      }}
    }},
    {{
      "operation": "link_node",
      "params": {{
        "source_node_id": "1",
        "source_output": "image",
        "target_node_id": "OpenAIImageEditing",
        "target_input": "image"
      }}
    }},
    {{
      "operation": "link_node",
      "params": {{
        "source_node_id": "OpenAIImageEditing",
        "source_output": "edited_image",
        "target_node_id": "PreviewImage",
        "target_input": "images"
      }}
    }}
  ],
  "description": "Connects to existing LoadImage node and adds image editing with preview."
}}
```

## Important Notes:
- Always include a description of what the workflow does
- Position nodes logically from left to right based on data flow
- Ensure all required inputs are connected or have default values
- Use output nodes (like PreviewImage) to display results
- Keep workflows simple and focused on the user's specific request
- **CRITICAL**: Output ONLY valid JSON without any comments or extra text
- **NO COMMENTS**: Do not include // comments in JSON as they make it invalid
"""

    def generate_workflow(self, user_request: str, current_workflow: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate a workflow based on user request and optional current workflow context"""
        try:
            system_prompt = self.create_system_prompt()
            
            # Prepare user message with context if available
            user_message = f"Create a workflow for: {user_request}"
            
            if current_workflow:
                user_message += f"\n\nCurrent workflow context:\n{json.dumps(current_workflow, indent=2)}"
                user_message += "\n\nIMPORTANT: The above workflow already exists on the canvas. When creating link_node operations:"
                user_message += "\n- Use the EXACT node IDs from the current workflow (e.g., if there's a node with ID '1', reference it as '1')"
                user_message += "\n- Connect new nodes TO existing nodes whenever possible"
                user_message += "\n- Reuse existing nodes instead of creating duplicates when appropriate"
                user_message += "\n- If modifying existing workflow, prefer connecting to existing nodes over creating isolated new workflows"
            
            response = self.client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            response_content = response.choices[0].message.content
            
            # Try to parse JSON response
            try:
                # Extract JSON from response (in case there's extra text)
                start_idx = response_content.find('{')
                end_idx = response_content.rfind('}') + 1
                json_str = response_content[start_idx:end_idx]
                
                workflow_data = json.loads(json_str)
                
                # Validate workflow structure
                if "workflow" not in workflow_data:
                    raise ValueError("Response missing 'workflow' key")
                
                # Convert to WorkflowAtom objects for validation
                atoms = []
                for step in workflow_data["workflow"]:
                    atom = WorkflowAtom(step["operation"], **step["params"])
                    atoms.append(atom)
                
                # Add metadata
                workflow_data["atoms"] = [atom.to_dict() for atom in atoms]
                workflow_data["user_request"] = user_request
                workflow_data["nodes_used"] = self._extract_nodes_used(atoms)
                
                return {
                    "success": True,
                    "workflow": workflow_data,
                    "raw_response": response_content
                }
                
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse JSON response: {e}")
                return {
                    "success": False,
                    "error": "Failed to parse workflow JSON",
                    "raw_response": response_content
                }
                
        except Exception as e:
            self.logger.error(f"Error generating workflow: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _extract_nodes_used(self, atoms: List[WorkflowAtom]) -> List[str]:
        """Extract list of node IDs used in the workflow"""
        nodes_used = set()
        for atom in atoms:
            if atom.operation == "add_node":
                nodes_used.add(atom.params.get("node_id"))
        return list(nodes_used)
    
    def validate_workflow(self, workflow_data: Dict[str, Any], current_workflow: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Validate a generated workflow"""
        errors = []
        warnings = []
        
        if "workflow" not in workflow_data:
            errors.append("Missing 'workflow' key")
            return {"valid": False, "errors": errors, "warnings": warnings}
        
        nodes_added = set()
        existing_nodes = set()
        
        # If we have a current workflow, extract existing node IDs
        if current_workflow and "nodes" in current_workflow:
            existing_nodes = set(current_workflow["nodes"].keys())
        
        for i, step in enumerate(workflow_data["workflow"]):
            step_errors = []
            
            if "operation" not in step:
                step_errors.append(f"Step {i}: Missing 'operation'")
                continue
            
            operation = step["operation"]
            params = step.get("params", {})
            
            if operation == "add_node":
                node_id = params.get("node_id")
                if not node_id:
                    step_errors.append(f"Step {i}: Missing node_id")
                elif node_id not in self.nodes_info:
                    step_errors.append(f"Step {i}: Unknown node_id '{node_id}'")
                else:
                    nodes_added.add(node_id)
                    
            elif operation == "link_node":
                source_node = params.get("source_node_id")
                target_node = params.get("target_node_id")
                
                # Check if source node exists (either added in this workflow or existing)
                if source_node not in nodes_added and source_node not in existing_nodes:
                    step_errors.append(f"Step {i}: Source node '{source_node}' not found")
                
                # Check if target node exists (either added in this workflow or existing)
                if target_node not in nodes_added and target_node not in existing_nodes:
                    step_errors.append(f"Step {i}: Target node '{target_node}' not found")
                    
            elif operation == "set_param":
                node_id = params.get("node_id")
                if node_id not in nodes_added and node_id not in existing_nodes:
                    step_errors.append(f"Step {i}: Node '{node_id}' not found")
            
            errors.extend(step_errors)
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def get_available_nodes_summary(self) -> Dict[str, Any]:
        """Get a summary of available nodes for the frontend"""
        categories = self.node_collector.get_nodes_by_category(self.nodes_info)
        
        summary = {
            "total_nodes": len(self.nodes_info),
            "categories": {}
        }
        
        for category, node_ids in categories.items():
            summary["categories"][category] = {
                "count": len(node_ids),
                "nodes": [
                    {
                        "id": node_id,
                        "display_name": self.nodes_info[node_id]["display_name"],
                        "description": self.nodes_info[node_id]["description"][:100] + "..." 
                        if len(self.nodes_info[node_id]["description"]) > 100 
                        else self.nodes_info[node_id]["description"]
                    }
                    for node_id in node_ids
                ]
            }
        
        return summary