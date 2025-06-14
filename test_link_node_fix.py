#!/usr/bin/env python3
"""
Test Link Node Fix
Tests that the link_node operation now works properly with existing nodes
"""

import requests
import json

def test_link_node_fix():
    """Test that link_node operations work with existing nodes"""
    
    print("🔗 Testing Link Node Fix")
    print("=" * 50)
    
    base_url = "http://localhost:12000"
    
    # Test 1: Simple connection to existing node
    print("\n🧪 Test 1: Generate workflow that connects to existing node")
    test_workflow = {
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
        "current_workflow": test_workflow
    })
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            workflow = result['workflow']['workflow']
            
            # Check for link_node operations
            link_operations = [op for op in workflow if op['operation'] == 'link_node']
            
            print(f"✅ Generated {len(link_operations)} link operations")
            
            # Check if it connects to existing node "1"
            connects_to_existing = any(
                op['params']['source_node_id'] == "1" 
                for op in link_operations
            )
            
            print(f"✅ Connects to existing node: {connects_to_existing}")
            
            # Show the link operations
            for i, op in enumerate(link_operations):
                params = op['params']
                print(f"  Link {i+1}: {params['source_node_id']} → {params['target_node_id']}")
                print(f"    {params['source_output']} → {params['target_input']}")
            
        else:
            print(f"❌ Failed: {result['error']}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
    
    # Test 2: Complex workflow with multiple connections
    print("\n🧪 Test 2: Complex workflow with multiple existing nodes")
    complex_workflow = {
        "nodes": {
            "5": {
                "class_type": "OpenAITextGeneration",
                "inputs": {"prompt": "Story about cats", "model": "gpt-4.1"}
            },
            "6": {
                "class_type": "TextToImageDisplay",
                "inputs": {}
            },
            "7": {
                "class_type": "PreviewImage",
                "inputs": {}
            }
        },
        "links": [
            [1, "5", 0, "6", 0, "STRING"],
            [2, "6", 0, "7", 0, "IMAGE"]
        ]
    }
    
    response = requests.post(f"{base_url}/api/chat/generate_workflow", json={
        "request": "Also generate an AI image based on the story text",
        "current_workflow": complex_workflow
    })
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            workflow = result['workflow']['workflow']
            
            # Check for link_node operations
            link_operations = [op for op in workflow if op['operation'] == 'link_node']
            
            print(f"✅ Generated {len(link_operations)} link operations")
            
            # Check if it connects to existing text node "5"
            uses_existing_text = any(
                op['params']['source_node_id'] == "5" 
                for op in link_operations
            )
            
            print(f"✅ Uses existing text node: {uses_existing_text}")
            
            # Show the link operations
            for i, op in enumerate(link_operations):
                params = op['params']
                print(f"  Link {i+1}: {params['source_node_id']} → {params['target_node_id']}")
                print(f"    {params['source_output']} → {params['target_input']}")
            
        else:
            print(f"❌ Failed: {result['error']}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
    
    print("\n🎯 Link Node Fix Test Complete!")
    print("The AI should now generate proper link_node operations that can connect to existing canvas nodes.")

if __name__ == "__main__":
    test_link_node_fix()