"""
Node Information Collector
Collects and compiles information about all available custom nodes
"""

import os
import importlib.util
import inspect
import json
from typing import Dict, List, Any, Optional
import logging

class NodeInfoCollector:
    """Collects information about all available custom nodes"""
    
    def __init__(self):
        self.nodes_info = {}
        self.logger = logging.getLogger(__name__)
    
    def collect_node_info(self, node_class) -> Dict[str, Any]:
        """Extract information from a node class"""
        try:
            info = {
                "class_name": node_class.__name__,
                "category": getattr(node_class, "CATEGORY", "Unknown"),
                "function": getattr(node_class, "FUNCTION", ""),
                "description": node_class.__doc__ or "",
                "input_types": {},
                "return_types": [],
                "return_names": []
            }
            
            # Get input types
            if hasattr(node_class, "INPUT_TYPES"):
                try:
                    input_types = node_class.INPUT_TYPES()
                    info["input_types"] = input_types
                except Exception as e:
                    self.logger.warning(f"Error getting input types for {node_class.__name__}: {e}")
            
            # Get return types
            if hasattr(node_class, "RETURN_TYPES"):
                info["return_types"] = list(node_class.RETURN_TYPES)
            
            # Get return names
            if hasattr(node_class, "RETURN_NAMES"):
                info["return_names"] = list(node_class.RETURN_NAMES)
            
            # Check if it's an output node
            info["is_output_node"] = getattr(node_class, "OUTPUT_NODE", False)
            
            return info
            
        except Exception as e:
            self.logger.error(f"Error collecting info for node {node_class.__name__}: {e}")
            return None
    
    def scan_custom_nodes_directory(self, custom_nodes_path: str) -> Dict[str, Any]:
        """Scan the custom nodes directory and collect node information"""
        nodes_info = {}
        
        if not os.path.exists(custom_nodes_path):
            self.logger.warning(f"Custom nodes directory not found: {custom_nodes_path}")
            return nodes_info
        
        for filename in os.listdir(custom_nodes_path):
            if filename.endswith('.py') and not filename.startswith('__'):
                file_path = os.path.join(custom_nodes_path, filename)
                try:
                    # Load the module
                    spec = importlib.util.spec_from_file_location(filename[:-3], file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Look for NODE_CLASS_MAPPINGS
                    if hasattr(module, 'NODE_CLASS_MAPPINGS'):
                        mappings = module.NODE_CLASS_MAPPINGS
                        for node_name, node_class in mappings.items():
                            node_info = self.collect_node_info(node_class)
                            if node_info:
                                # Add display name if available
                                if hasattr(module, 'NODE_DISPLAY_NAME_MAPPINGS'):
                                    display_mappings = module.NODE_DISPLAY_NAME_MAPPINGS
                                    node_info["display_name"] = display_mappings.get(node_name, node_name)
                                else:
                                    node_info["display_name"] = node_name
                                
                                node_info["node_id"] = node_name
                                node_info["file_source"] = filename
                                nodes_info[node_name] = node_info
                                
                except Exception as e:
                    self.logger.error(f"Error loading custom node file {filename}: {e}")
        
        return nodes_info
    
    def get_builtin_nodes_info(self) -> Dict[str, Any]:
        """Get information about essential built-in ComfyUI nodes"""
        builtin_nodes = {}
        
        # Define essential built-in nodes that should be available to the AI
        essential_builtins = {
            "PreviewImage": {
                "class_name": "PreviewImage",
                "display_name": "Preview Image",
                "node_id": "PreviewImage",
                "category": "image",
                "function": "preview",
                "description": "Preview an image in the ComfyUI interface",
                "input_types": {
                    "required": {
                        "images": ("IMAGE",)
                    }
                },
                "return_types": [],
                "return_names": [],
                "is_output_node": True,
                "file_source": "builtin"
            },
            "LoadImage": {
                "class_name": "LoadImage", 
                "display_name": "Load Image",
                "node_id": "LoadImage",
                "category": "image",
                "function": "load_image",
                "description": "Load an image from file",
                "input_types": {
                    "required": {
                        "image": ("STRING", {"image_upload": True})
                    }
                },
                "return_types": ["IMAGE", "MASK"],
                "return_names": ["image", "mask"],
                "is_output_node": False,
                "file_source": "builtin"
            },
            "SaveImage": {
                "class_name": "SaveImage",
                "display_name": "Save Image", 
                "node_id": "SaveImage",
                "category": "image",
                "function": "save_image",
                "description": "Save an image to file",
                "input_types": {
                    "required": {
                        "images": ("IMAGE",),
                        "filename_prefix": ("STRING", {"default": "ComfyUI"})
                    }
                },
                "return_types": [],
                "return_names": [],
                "is_output_node": True,
                "file_source": "builtin"
            }
        }
        
        return essential_builtins

    def get_all_nodes_info(self) -> Dict[str, Any]:
        """Get information about all available nodes (custom + essential built-ins)"""
        custom_nodes_path = "/workspace/oneflow/custom_nodes"
        
        # Get custom nodes
        all_nodes = self.scan_custom_nodes_directory(custom_nodes_path)
        
        # Add essential built-in nodes
        builtin_nodes = self.get_builtin_nodes_info()
        all_nodes.update(builtin_nodes)
        
        return all_nodes
    
    def get_nodes_by_category(self, nodes_info: Dict[str, Any]) -> Dict[str, List[str]]:
        """Group nodes by category"""
        categories = {}
        for node_id, info in nodes_info.items():
            category = info.get("category", "Unknown")
            if category not in categories:
                categories[category] = []
            categories[category].append(node_id)
        return categories
    
    def format_for_gpt(self, nodes_info: Dict[str, Any]) -> str:
        """Format node information for GPT consumption"""
        formatted_info = []
        formatted_info.append("# Available Custom Nodes\n")
        
        categories = self.get_nodes_by_category(nodes_info)
        
        for category, node_ids in categories.items():
            formatted_info.append(f"## Category: {category}\n")
            
            for node_id in node_ids:
                info = nodes_info[node_id]
                formatted_info.append(f"### {info['display_name']} (ID: {node_id})")
                formatted_info.append(f"**Description:** {info['description']}")
                formatted_info.append(f"**Function:** {info['function']}")
                formatted_info.append(f"**Output Node:** {info['is_output_node']}")
                
                # Input types
                if info['input_types']:
                    formatted_info.append("**Inputs:**")
                    for input_category, inputs in info['input_types'].items():
                        formatted_info.append(f"  - {input_category.upper()}:")
                        for input_name, input_spec in inputs.items():
                            if isinstance(input_spec, tuple):
                                input_type = input_spec[0]
                                input_config = input_spec[1] if len(input_spec) > 1 else {}
                                formatted_info.append(f"    - {input_name}: {input_type} {input_config}")
                            else:
                                formatted_info.append(f"    - {input_name}: {input_spec}")
                
                # Outputs
                if info['return_types']:
                    formatted_info.append("**Outputs:**")
                    for i, return_type in enumerate(info['return_types']):
                        return_name = info['return_names'][i] if i < len(info['return_names']) else f"output_{i}"
                        formatted_info.append(f"  - {return_name}: {return_type}")
                
                formatted_info.append("")  # Empty line
        
        return "\n".join(formatted_info)