#!/usr/bin/env python3
"""
Debug Link Issue - Test the actual linking behavior
"""

import requests
import json

def debug_link_issue():
    """Debug the actual linking issue step by step"""
    
    print("🔍 Debugging Link Node Issue")
    print("=" * 50)
    
    base_url = "http://localhost:12000"
    
    # Test 1: Simple workflow generation
    print("\n🧪 Test 1: Generate simple workflow")
    
    current_workflow = {
        "nodes": {
            "1": {
                "class_type": "LoadImage",
                "inputs": {"image": "test.jpg"}
            }
        },
        "links": []
    }
    
    response = requests.post(f"{base_url}/api/chat/generate_workflow", json={
        "request": "Edit this image to make it brighter",
        "current_workflow": current_workflow
    })
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            print("✅ Workflow generated successfully")
            workflow = result['workflow']
            
            print("\n📋 Generated Workflow:")
            print(json.dumps(workflow, indent=2))
            
            # Check for link operations
            link_ops = [op for op in workflow['workflow'] if op['operation'] == 'link_node']
            print(f"\n🔗 Found {len(link_ops)} link operations:")
            
            for i, op in enumerate(link_ops):
                params = op['params']
                print(f"  {i+1}. {params['source_node_id']} → {params['target_node_id']}")
                print(f"     {params['source_output']} → {params['target_input']}")
                
                # Check if it references the existing node
                if params['source_node_id'] == "1":
                    print("     ✅ References existing LoadImage node!")
                elif params['target_node_id'] == "1":
                    print("     ✅ Targets existing LoadImage node!")
                else:
                    print("     ❌ Does not reference existing node")
            
        else:
            print(f"❌ Failed to generate workflow: {result.get('error', 'Unknown error')}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        print(f"Response: {response.text}")
    
    # Test 2: Check node information
    print("\n🧪 Test 2: Check available nodes")
    
    response = requests.get(f"{base_url}/api/chat/nodes")
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            nodes = result['nodes']
            print(f"✅ Found {len(nodes)} available node types")
            
            # Check for image editing nodes
            image_nodes = [node for node in nodes if 'image' in node.lower() or 'edit' in node.lower()]
            print(f"📸 Image-related nodes: {image_nodes}")
            
        else:
            print(f"❌ Failed to get nodes: {result.get('error', 'Unknown error')}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
    
    # Test 3: Test validation
    print("\n🧪 Test 3: Test workflow validation")
    
    test_workflow = {
        "workflow": [
            {
                "operation": "add_node",
                "params": {
                    "node_id": "OpenAIImageEditing",
                    "node_params": {"prompt": "Make brighter"},
                    "position": {"x": 300, "y": 100}
                }
            },
            {
                "operation": "link_node",
                "params": {
                    "source_node_id": "1",
                    "source_output": "image",
                    "target_node_id": "OpenAIImageEditing",
                    "target_input": "image"
                }
            }
        ]
    }
    
    response = requests.post(f"{base_url}/api/chat/validate_workflow", json={
        "workflow": test_workflow,
        "current_workflow": current_workflow
    })
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            validation = result['validation']
            print(f"✅ Validation result: {'VALID' if validation['valid'] else 'INVALID'}")
            
            if validation['errors']:
                print("❌ Validation errors:")
                for error in validation['errors']:
                    print(f"   - {error}")
            
            if validation['warnings']:
                print("⚠️ Validation warnings:")
                for warning in validation['warnings']:
                    print(f"   - {warning}")
                    
        else:
            print(f"❌ Validation failed: {result.get('error', 'Unknown error')}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
    
    print("\n🎯 Debug Complete!")
    print("Check the browser console for frontend debugging information.")

if __name__ == "__main__":
    debug_link_issue()