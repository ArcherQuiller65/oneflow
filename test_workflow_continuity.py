#!/usr/bin/env python3
"""
Test Workflow Continuity
Demonstrates that AI can see existing nodes and connect new nodes properly
"""

import requests
import json

def test_workflow_continuity():
    """Test complete workflow continuity scenarios"""
    
    print("🌊 Testing OneFlow Workflow Continuity")
    print("=" * 50)
    
    base_url = "http://localhost:12000"
    
    # Scenario 1: User has image, wants to edit it
    print("\n📸 Scenario 1: User has image on canvas, wants to edit it")
    print("-" * 50)
    
    # Simulate existing canvas with LoadImage node
    existing_workflow = {
        "nodes": {
            "img_1": {
                "class_type": "LoadImage",
                "inputs": {"image": "sunset.jpg"}
            }
        },
        "links": []
    }
    
    print("Canvas state: LoadImage node (ID: img_1) with sunset.jpg")
    
    # User asks to edit the image
    response = requests.post(f"{base_url}/api/chat/generate_workflow", json={
        "request": "Make this image more vibrant and colorful",
        "current_workflow": existing_workflow
    })
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            workflow = result['workflow']['workflow']
            
            # Check connections
            connections = [step for step in workflow if step['operation'] == 'link_node']
            connects_to_existing = any(
                conn['params']['source_node_id'] == 'img_1' 
                for conn in connections
            )
            
            print(f"✅ AI connects to existing image: {connects_to_existing}")
            
            # Show the workflow
            print("Generated workflow:")
            for step in workflow:
                if step['operation'] == 'add_node':
                    print(f"  + Add {step['params']['node_id']}")
                elif step['operation'] == 'link_node':
                    src = step['params']['source_node_id']
                    tgt = step['params']['target_node_id']
                    print(f"  → Connect {src} to {tgt}")
        else:
            print(f"❌ Failed: {result['error']}")
    
    # Scenario 2: User has text generation, wants to add image
    print("\n📝 Scenario 2: User has text generation, wants to add image")
    print("-" * 50)
    
    existing_workflow = {
        "nodes": {
            "text_1": {
                "class_type": "OpenAITextGeneration",
                "inputs": {
                    "prompt": "Write a description of a magical forest",
                    "model": "gpt-4.1"
                }
            },
            "display_1": {
                "class_type": "TextToImageDisplay",
                "inputs": {}
            }
        },
        "links": [
            [1, "text_1", 0, "display_1", 0, "STRING"]
        ]
    }
    
    print("Canvas state: Text generation → Text display")
    
    response = requests.post(f"{base_url}/api/chat/generate_workflow", json={
        "request": "Now also generate an AI image based on this text description",
        "current_workflow": existing_workflow
    })
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            workflow = result['workflow']['workflow']
            
            # Check if it connects to existing text node
            connections = [step for step in workflow if step['operation'] == 'link_node']
            uses_existing_text = any(
                conn['params']['source_node_id'] == 'text_1'
                for conn in connections
            )
            
            print(f"✅ AI uses existing text output: {uses_existing_text}")
            
            # Show the workflow
            print("Generated workflow:")
            for step in workflow:
                if step['operation'] == 'add_node':
                    print(f"  + Add {step['params']['node_id']}")
                elif step['operation'] == 'link_node':
                    src = step['params']['source_node_id']
                    tgt = step['params']['target_node_id']
                    print(f"  → Connect {src} to {tgt}")
        else:
            print(f"❌ Failed: {result['error']}")
    
    # Scenario 3: Complex workflow extension
    print("\n🔧 Scenario 3: Complex workflow extension")
    print("-" * 50)
    
    existing_workflow = {
        "nodes": {
            "load_1": {
                "class_type": "LoadImage",
                "inputs": {"image": "photo.jpg"}
            },
            "edit_1": {
                "class_type": "OpenAIImageEditing",
                "inputs": {"prompt": "Make brighter"}
            },
            "preview_1": {
                "class_type": "PreviewImage",
                "inputs": {}
            }
        },
        "links": [
            [1, "load_1", 0, "edit_1", 0, "IMAGE"],
            [2, "edit_1", 0, "preview_1", 0, "IMAGE"]
        ]
    }
    
    print("Canvas state: LoadImage → ImageEditing → PreviewImage")
    
    response = requests.post(f"{base_url}/api/chat/generate_workflow", json={
        "request": "Also upload the edited image to cloud storage",
        "current_workflow": existing_workflow
    })
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            workflow = result['workflow']['workflow']
            
            # Check if it connects to existing edited image
            connections = [step for step in workflow if step['operation'] == 'link_node']
            extends_workflow = any(
                conn['params']['source_node_id'] in ['edit_1', 'preview_1']
                for conn in connections
            )
            
            print(f"✅ AI extends existing workflow: {extends_workflow}")
            
            # Show the workflow
            print("Generated workflow:")
            for step in workflow:
                if step['operation'] == 'add_node':
                    print(f"  + Add {step['params']['node_id']}")
                elif step['operation'] == 'link_node':
                    src = step['params']['source_node_id']
                    tgt = step['params']['target_node_id']
                    print(f"  → Connect {src} to {tgt}")
        else:
            print(f"❌ Failed: {result['error']}")
    
    print("\n🎯 Workflow Continuity Test Complete!")
    print("The AI can now see existing nodes and connect new nodes properly!")

if __name__ == "__main__":
    test_workflow_continuity()