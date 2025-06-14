"""
Chat Service for AI Workflow Generation
Handles chat interactions and workflow generation requests
"""

import json
import logging
import time
import os
from typing import Dict, List, Any, Optional
from aiohttp import web
from .workflow_generator import WorkflowGenerator

class ChatService:
    """Service for handling chat interactions and workflow generation"""
    
    def __init__(self):
        self.workflow_generator = WorkflowGenerator()
        self.logger = logging.getLogger(__name__)
        self.chat_history = []  # In production, this should be stored in a database
        self.current_workflow = None  # Store the current workflow for context
    
    def add_routes(self, routes):
        """Add chat-related routes to the server"""
        
        @routes.get('/landing')
        async def landing_page(request):
            """Serve the landing page"""
            try:
                landing_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "web_chat", "landing.html")
                return web.FileResponse(landing_path)
            except Exception as e:
                self.logger.error(f"Error serving landing page: {e}")
                return web.Response(text="Landing page not found", status=404)
        
        @routes.post('/chat/generate_workflow')
        async def generate_workflow(request):
            """Generate a workflow based on user request"""
            try:
                data = await request.json()
                user_request = data.get('request', '')
                current_workflow = data.get('current_workflow', None)
                
                if not user_request.strip():
                    return web.json_response({
                        'success': False,
                        'error': 'Empty request'
                    }, status=400)
                
                # Generate workflow with current context if provided
                result = self.workflow_generator.generate_workflow(user_request, current_workflow)
                
                # Add to chat history
                chat_entry = {
                    'timestamp': time.time(),
                    'user_request': user_request,
                    'result': result,
                    'id': len(self.chat_history)
                }
                self.chat_history.append(chat_entry)
                
                return web.json_response(result)
                
            except Exception as e:
                self.logger.error(f"Error in generate_workflow: {e}")
                return web.json_response({
                    'success': False,
                    'error': str(e)
                }, status=500)
        
        @routes.get('/chat/nodes_info')
        async def get_nodes_info(request):
            """Get information about available nodes"""
            try:
                summary = self.workflow_generator.get_available_nodes_summary()
                return web.json_response({
                    'success': True,
                    'data': summary
                })
            except Exception as e:
                self.logger.error(f"Error in get_nodes_info: {e}")
                return web.json_response({
                    'success': False,
                    'error': str(e)
                }, status=500)
        
        @routes.get('/chat/history')
        async def get_chat_history(request):
            """Get chat history"""
            try:
                # Return last 50 entries
                recent_history = self.chat_history[-50:] if len(self.chat_history) > 50 else self.chat_history
                return web.json_response({
                    'success': True,
                    'data': recent_history
                })
            except Exception as e:
                self.logger.error(f"Error in get_chat_history: {e}")
                return web.json_response({
                    'success': False,
                    'error': str(e)
                }, status=500)
        
        @routes.post('/chat/validate_workflow')
        async def validate_workflow(request):
            """Validate a workflow"""
            try:
                data = await request.json()
                workflow_data = data.get('workflow', {})
                current_workflow = data.get('current_workflow', None)
                
                validation_result = self.workflow_generator.validate_workflow(workflow_data, current_workflow)
                
                return web.json_response({
                    'success': True,
                    'validation': validation_result
                })
                
            except Exception as e:
                self.logger.error(f"Error in validate_workflow: {e}")
                return web.json_response({
                    'success': False,
                    'error': str(e)
                }, status=500)
        
        @routes.post('/chat/execute_workflow')
        async def execute_workflow(request):
            """Execute a generated workflow (placeholder for future implementation)"""
            try:
                data = await request.json()
                workflow_data = data.get('workflow', {})
                
                # For now, just return the workflow data
                # In the future, this could integrate with ComfyUI's execution system
                return web.json_response({
                    'success': True,
                    'message': 'Workflow execution not yet implemented',
                    'workflow': workflow_data
                })
                
            except Exception as e:
                self.logger.error(f"Error in execute_workflow: {e}")
                return web.json_response({
                    'success': False,
                    'error': str(e)
                }, status=500)
        
        @routes.post('/chat/current_workflow')
        async def get_current_workflow(request):
            """Receive and analyze the current workflow from the canvas"""
            try:
                data = await request.json()
                workflow_data = data.get('workflow', {})
                
                # Analyze the current workflow
                analysis = self.analyze_current_workflow(workflow_data)
                
                return web.json_response({
                    'success': True,
                    'analysis': analysis
                })
                
            except Exception as e:
                self.logger.error(f"Error in get_current_workflow: {e}")
                return web.json_response({
                    'success': False,
                    'error': str(e)
                }, status=500)

        @routes.get('/chat/status')
        async def get_status(request):
            """Get chat service status"""
            try:
                nodes_info = self.workflow_generator.nodes_info
                return web.json_response({
                    'success': True,
                    'status': 'active',
                    'nodes_loaded': len(nodes_info),
                    'chat_entries': len(self.chat_history)
                })
            except Exception as e:
                self.logger.error(f"Error in get_status: {e}")
                return web.json_response({
                    'success': False,
                    'error': str(e)
                }, status=500)
    
    def analyze_current_workflow(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the current workflow and extract useful information"""
        try:
            # Store the current workflow for context
            self.current_workflow = workflow_data
            
            analysis = {
                'nodes': [],
                'connections': [],
                'has_image_input': False,
                'has_text_input': False,
                'has_image_output': False,
                'has_text_output': False,
                'existing_editing_nodes': [],
                'existing_display_nodes': [],
                'summary': ''
            }
            
            # Extract nodes information
            nodes = workflow_data.get('nodes', {})
            links = workflow_data.get('links', [])
            
            for node_id, node_data in nodes.items():
                node_type = node_data.get('class_type', '')
                node_info = {
                    'id': node_id,
                    'type': node_type,
                    'inputs': node_data.get('inputs', {}),
                    'outputs': []
                }
                
                # Check for specific node types
                if 'image' in node_type.lower() and 'edit' in node_type.lower():
                    analysis['existing_editing_nodes'].append(node_info)
                
                if 'display' in node_type.lower() or 'preview' in node_type.lower():
                    analysis['existing_display_nodes'].append(node_info)
                
                # Check for image/text inputs and outputs
                for input_name, input_data in node_data.get('inputs', {}).items():
                    if isinstance(input_data, list) and len(input_data) >= 2:
                        # This is a connection [source_node_id, output_slot]
                        continue
                    # Check input types
                    if 'image' in input_name.lower():
                        analysis['has_image_input'] = True
                    if 'text' in input_name.lower() or 'prompt' in input_name.lower():
                        analysis['has_text_input'] = True
                
                analysis['nodes'].append(node_info)
            
            # Extract connections
            for link in links:
                if len(link) >= 6:  # [link_id, source_node, source_slot, target_node, target_slot, type]
                    connection = {
                        'source_node': link[1],
                        'source_slot': link[2],
                        'target_node': link[3],
                        'target_slot': link[4],
                        'type': link[5] if len(link) > 5 else 'unknown'
                    }
                    analysis['connections'].append(connection)
                    
                    # Check connection types
                    if connection['type'] == 'IMAGE':
                        analysis['has_image_output'] = True
                    elif connection['type'] == 'STRING':
                        analysis['has_text_output'] = True
            
            # Generate summary
            node_count = len(analysis['nodes'])
            connection_count = len(analysis['connections'])
            editing_count = len(analysis['existing_editing_nodes'])
            display_count = len(analysis['existing_display_nodes'])
            
            summary_parts = [f"{node_count} nodes", f"{connection_count} connections"]
            if editing_count > 0:
                summary_parts.append(f"{editing_count} image editing nodes")
            if display_count > 0:
                summary_parts.append(f"{display_count} display nodes")
            
            analysis['summary'] = f"Current workflow has {', '.join(summary_parts)}"
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing workflow: {e}")
            return {
                'error': str(e),
                'summary': 'Failed to analyze workflow'
            }