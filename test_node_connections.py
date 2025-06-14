#!/usr/bin/env python3
"""
Test Node Connection Behavior
Tests that the AI properly connects to existing nodes on the canvas
"""

import requests
import json

def test_connection_behavior():
    """Test various scenarios of connecting to existing nodes"""
    
    print("🔗 Testing Node Connection Behavior")
    print("=" * 50)
    
    base_url = "http://localhost:12000"
    
    # Test 1: Connect to existing LoadImage node
    print("\n🧪 Test 1: Connect to existing LoadImage node")
    test1_workflow = {
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
        "current_workflow": test1_workflow
    })
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            # Check if it connects to node "1"
            links = [step for step in result['workflow']['workflow'] if step['operation'] == 'link_node']
            connected_to_existing = any(link['params']['source_node_id'] == "1" for link in links)
            print(f"✅ Connects to existing LoadImage node: {connected_to_existing}")
        else:
            print(f"❌ Failed: {result['error']}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
    
    # Test 2: Reuse existing PreviewImage node
    print("\n🧪 Test 2: Reuse existing PreviewImage node")
    test2_workflow = {
        "nodes": {
            "5": {
                "class_type": "LoadImage",
                "inputs": {"image": "photo.jpg"}
            },
            "6": {
                "class_type": "PreviewImage",
                "inputs": {}
            }
        },
        "links": [[1, "5", 0, "6", 0, "IMAGE"]]
    }
    
    response = requests.post(f"{base_url}/api/chat/generate_workflow", json={
        "request": "Edit this image to add more contrast",
        "current_workflow": test2_workflow
    })
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            # Check if it reuses existing PreviewImage node "6"
            links = [step for step in result['workflow']['workflow'] if step['operation'] == 'link_node']
            reuses_preview = any(link['params']['target_node_id'] == "6" for link in links)
            print(f"✅ Reuses existing PreviewImage node: {reuses_preview}")
        else:
            print(f"❌ Failed: {result['error']}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
    
    # Test 3: Connect text generation to image generation
    print("\n🧪 Test 3: Connect text generation to image generation")
    test3_workflow = {
        "nodes": {
            "10": {
                "class_type": "OpenAITextGeneration",
                "inputs": {
                    "prompt": "Write a description of a sunset",
                    "model": "gpt-4.1"
                }
            }
        },
        "links": []
    }
    
    response = requests.post(f"{base_url}/api/chat/generate_workflow", json={
        "request": "Now generate an image based on this text description",
        "current_workflow": test3_workflow
    })
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            # Check if it connects text output to image input
            links = [step for step in result['workflow']['workflow'] if step['operation'] == 'link_node']
            text_to_image = any(
                link['params']['source_node_id'] == "10" and 
                'OpenAITextToImage' in link['params']['target_node_id']
                for link in links
            )
            print(f"✅ Connects text generation to image generation: {text_to_image}")
        else:
            print(f"❌ Failed: {result['error']}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
    
    # Test 4: Complex workflow modification
    print("\n🧪 Test 4: Complex workflow modification")
    test4_workflow = {
        "nodes": {
            "20": {
                "class_type": "OpenAITextGeneration",
                "inputs": {"prompt": "Story about cats", "model": "gpt-4.1"}
            },
            "21": {
                "class_type": "TextToImageDisplay",
                "inputs": {}
            },
            "22": {
                "class_type": "PreviewImage",
                "inputs": {}
            }
        },
        "links": [
            [10, "20", 0, "21", 0, "STRING"],
            [11, "21", 0, "22", 0, "IMAGE"]
        ]
    }
    
    response = requests.post(f"{base_url}/api/chat/generate_workflow", json={
        "request": "Also upload the text display to OSS cloud storage",
        "current_workflow": test4_workflow
    })
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            # Check if it connects to existing TextToImageDisplay node
            links = [step for step in result['workflow']['workflow'] if step['operation'] == 'link_node']
            connects_to_display = any(
                link['params']['source_node_id'] == "21" for link in links
            )
            print(f"✅ Connects to existing TextToImageDisplay node: {connects_to_display}")
        else:
            print(f"❌ Failed: {result['error']}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
    
    print("\n🎯 Node Connection Tests Complete!")

if __name__ == "__main__":
    test_connection_behavior()