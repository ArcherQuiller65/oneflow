#!/usr/bin/env python3
"""
Test script for enhanced OneFlow chat functionality
Tests all the new features:
1. Text-to-image display requirement
2. Canvas workflow inspection
3. OSS upload in image editing
4. Context-aware workflow generation
"""

import requests
import json
import time

BASE_URL = "http://localhost:12000"

def test_api_endpoint(endpoint, method="GET", data=None):
    """Test an API endpoint and return the response"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "POST":
            response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        else:
            response = requests.get(url)
        
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error testing {endpoint}: {e}")
        return None

def test_text_rendering_requirement():
    """Test that text rendering uses TextToImageDisplay + ImagePreview"""
    print("\n🧪 Testing text rendering requirement...")
    
    result = test_api_endpoint("/api/chat/generate_workflow", "POST", {
        "request": "Generate a poem about the ocean and display it"
    })
    
    if result and result.get("success"):
        nodes_used = result.get("workflow", {}).get("nodes_used", [])
        if "TextToImageDisplay" in nodes_used and "PreviewImage" in nodes_used:
            print("✅ Text rendering correctly uses TextToImageDisplay + PreviewImage")
            return True
        else:
            print(f"❌ Text rendering doesn't use required nodes. Used: {nodes_used}")
            return False
    else:
        print("❌ Failed to generate workflow for text rendering")
        return False

def test_image_editing_with_oss():
    """Test that image editing uses OpenAIImageEditing with OSS upload"""
    print("\n🧪 Testing image editing with OSS upload...")
    
    result = test_api_endpoint("/api/chat/generate_workflow", "POST", {
        "request": "Edit an image to make it more artistic"
    })
    
    if result and result.get("success"):
        nodes_used = result.get("workflow", {}).get("nodes_used", [])
        if "OpenAIImageEditing" in nodes_used:
            print("✅ Image editing correctly uses OpenAIImageEditing node")
            return True
        else:
            print(f"❌ Image editing doesn't use OpenAIImageEditing. Used: {nodes_used}")
            return False
    else:
        print("❌ Failed to generate workflow for image editing")
        return False

def test_workflow_analysis():
    """Test workflow analysis endpoint"""
    print("\n🧪 Testing workflow analysis...")
    
    sample_workflow = {
        "workflow": {
            "nodes": {
                "1": {
                    "class_type": "OpenAITextGeneration",
                    "inputs": {
                        "prompt": "Write a story about space",
                        "model": "gpt-4.1"
                    }
                },
                "2": {
                    "class_type": "TextToImageDisplay",
                    "inputs": {
                        "text": ["1", 0],
                        "width": 800,
                        "height": 400
                    }
                },
                "3": {
                    "class_type": "PreviewImage",
                    "inputs": {
                        "images": ["2", 0]
                    }
                }
            },
            "links": [
                [1, 1, 0, 2, 0, "STRING"],
                [2, 2, 0, 3, 0, "IMAGE"]
            ]
        }
    }
    
    result = test_api_endpoint("/api/chat/current_workflow", "POST", sample_workflow)
    
    if result and result.get("success"):
        analysis = result.get("analysis", {})
        if analysis.get("summary") and len(analysis.get("nodes", [])) == 3:
            print("✅ Workflow analysis working correctly")
            print(f"   Summary: {analysis.get('summary')}")
            return True
        else:
            print("❌ Workflow analysis incomplete")
            return False
    else:
        print("❌ Failed to analyze workflow")
        return False

def test_context_aware_generation():
    """Test context-aware workflow generation"""
    print("\n🧪 Testing context-aware workflow generation...")
    
    # First, create a base workflow
    current_workflow = {
        "nodes": {
            "1": {
                "class_type": "OpenAITextGeneration",
                "inputs": {
                    "prompt": "Write a story about cats",
                    "model": "gpt-4.1"
                }
            },
            "2": {
                "class_type": "TextToImageDisplay",
                "inputs": {
                    "text": ["1", 0],
                    "width": 800,
                    "height": 400
                }
            }
        },
        "links": [
            [1, 1, 0, 2, 0, "STRING"]
        ]
    }
    
    # Test modification request
    result = test_api_endpoint("/api/chat/generate_workflow", "POST", {
        "request": "Change the story to be about robots instead",
        "current_workflow": current_workflow
    })
    
    if result and result.get("success"):
        workflow = result.get("workflow", {}).get("workflow", [])
        # Check if it uses set_param instead of creating new nodes
        has_set_param = any(op.get("operation") == "set_param" for op in workflow)
        if has_set_param:
            print("✅ Context-aware generation working - uses set_param for modifications")
            return True
        else:
            print("❌ Context-aware generation not working - doesn't use set_param")
            return False
    else:
        print("❌ Failed to generate context-aware workflow")
        return False

def test_chat_status():
    """Test chat service status"""
    print("\n🧪 Testing chat service status...")
    
    result = test_api_endpoint("/api/chat/status")
    
    if result and result.get("success"):
        nodes_loaded = result.get("nodes_loaded", 0)
        if nodes_loaded >= 7:  # We expect at least 7 nodes
            print(f"✅ Chat service active with {nodes_loaded} nodes loaded")
            return True
        else:
            print(f"❌ Not enough nodes loaded: {nodes_loaded}")
            return False
    else:
        print("❌ Chat service not responding")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting OneFlow Enhanced Chat Tests")
    print("=" * 50)
    
    tests = [
        ("Chat Service Status", test_chat_status),
        ("Text Rendering Requirement", test_text_rendering_requirement),
        ("Image Editing with OSS", test_image_editing_with_oss),
        ("Workflow Analysis", test_workflow_analysis),
        ("Context-Aware Generation", test_context_aware_generation),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Enhanced chat functionality is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")

if __name__ == "__main__":
    main()