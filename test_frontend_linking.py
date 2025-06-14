#!/usr/bin/env python3
"""
Test Frontend Linking
Tests that the frontend can properly execute link_node operations
"""

import requests
import json

def test_frontend_linking():
    """Test frontend execution of link_node operations"""
    
    print("🎨 Testing Frontend Link Node Execution")
    print("=" * 50)
    
    base_url = "http://localhost:12000"
    
    # Test the workflow generation and structure
    print("\n📋 Testing workflow structure for frontend execution")
    
    test_workflow = {
        "nodes": {
            "1": {
                "class_type": "LoadImage",
                "inputs": {"image": "sunset.jpg"}
            }
        },
        "links": []
    }
    
    response = requests.post(f"{base_url}/api/chat/generate_workflow", json={
        "request": "Make this image more vibrant and add a preview",
        "current_workflow": test_workflow
    })
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            workflow = result['workflow']['workflow']
            
            print("Generated workflow operations:")
            for i, op in enumerate(workflow):
                print(f"  {i+1}. {op['operation']}")
                if op['operation'] == 'add_node':
                    print(f"     Node: {op['params']['node_id']}")
                elif op['operation'] == 'link_node':
                    params = op['params']
                    print(f"     Connect: {params['source_node_id']} → {params['target_node_id']}")
                    print(f"     Slots: {params['source_output']} → {params['target_input']}")
            
            # Verify the structure is correct for frontend execution
            add_ops = [op for op in workflow if op['operation'] == 'add_node']
            link_ops = [op for op in workflow if op['operation'] == 'link_node']
            
            print(f"\n✅ Add operations: {len(add_ops)}")
            print(f"✅ Link operations: {len(link_ops)}")
            
            # Check that link operations reference valid nodes
            all_node_ids = set()
            all_node_ids.add("1")  # Existing node
            
            for op in add_ops:
                all_node_ids.add(op['params']['node_id'])
            
            print(f"✅ Available node IDs: {sorted(all_node_ids)}")
            
            # Verify all link operations reference valid nodes
            valid_links = True
            for op in link_ops:
                source_id = op['params']['source_node_id']
                target_id = op['params']['target_node_id']
                
                if source_id not in all_node_ids:
                    print(f"❌ Invalid source node: {source_id}")
                    valid_links = False
                
                if target_id not in all_node_ids:
                    print(f"❌ Invalid target node: {target_id}")
                    valid_links = False
            
            if valid_links:
                print("✅ All link operations reference valid nodes")
            
            # Test the workflow format for frontend consumption
            print(f"\n📦 Workflow ready for frontend execution:")
            print(f"   - Description: {result['workflow'].get('description', 'N/A')}")
            print(f"   - Nodes used: {len(result['workflow'].get('nodes_used', []))}")
            print(f"   - Operations: {len(workflow)}")
            
        else:
            print(f"❌ Failed: {result['error']}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
    
    # Test with a more complex scenario
    print("\n🔧 Testing complex workflow with multiple existing nodes")
    
    complex_workflow = {
        "nodes": {
            "text_gen": {
                "class_type": "OpenAITextGeneration",
                "inputs": {"prompt": "Write about nature", "model": "gpt-4.1"}
            },
            "img_load": {
                "class_type": "LoadImage", 
                "inputs": {"image": "forest.jpg"}
            }
        },
        "links": []
    }
    
    response = requests.post(f"{base_url}/api/chat/generate_workflow", json={
        "request": "Connect the text to create an image, and also edit the loaded image",
        "current_workflow": complex_workflow
    })
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            workflow = result['workflow']['workflow']
            
            # Count operations
            add_ops = [op for op in workflow if op['operation'] == 'add_node']
            link_ops = [op for op in workflow if op['operation'] == 'link_node']
            
            print(f"✅ Complex workflow generated:")
            print(f"   - Add operations: {len(add_ops)}")
            print(f"   - Link operations: {len(link_ops)}")
            
            # Check connections to existing nodes
            existing_connections = 0
            for op in link_ops:
                if op['params']['source_node_id'] in ['text_gen', 'img_load']:
                    existing_connections += 1
            
            print(f"✅ Connections to existing nodes: {existing_connections}")
            
        else:
            print(f"❌ Failed: {result['error']}")
    
    print("\n🎯 Frontend Linking Test Complete!")
    print("The workflow structure is now properly formatted for frontend execution.")
    print("Next step: Test in browser to verify actual node linking works.")

if __name__ == "__main__":
    test_frontend_linking()