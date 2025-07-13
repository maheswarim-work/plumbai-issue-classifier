#!/usr/bin/env python3
"""
Example script to test the Smart Plumbing Issue Classifier API
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("🏥 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Health check passed: {data['status']}")
        print(f"   Model loaded: {data['model_loaded']}")
        print(f"   Version: {data['version']}")
        print(f"   Uptime: {data['uptime_seconds']:.2f} seconds")
    else:
        print(f"❌ Health check failed: {response.status_code}")
    print()

def test_categories():
    """Test the categories endpoint"""
    print("📋 Testing categories endpoint...")
    response = requests.get(f"{BASE_URL}/categories")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {len(data['categories'])} categories:")
        for category in data['categories']:
            description = data['descriptions'].get(category, 'No description')
            print(f"   - {category}: {description}")
    else:
        print(f"❌ Categories request failed: {response.status_code}")
    print()

def classify_issue(description, customer_info=None):
    """Classify a plumbing issue"""
    payload = {
        "description": description
    }
    if customer_info:
        payload.update(customer_info)
    
    print(f"🔍 Classifying: '{description}'")
    response = requests.post(f"{BASE_URL}/classify", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        classification = data['classification']
        
        print(f"✅ Classification Results:")
        print(f"   Category: {classification['category']}")
        print(f"   Confidence: {classification['confidence']:.2%}")
        print(f"   Severity: {classification['severity']}")
        print(f"   Urgency: {classification['urgency']}")
        print(f"   Estimated Duration: {classification['estimated_duration']}")
        print(f"   Required Tools: {', '.join(classification['required_tools'])}")
        print(f"   Recommended Parts: {', '.join(classification['recommended_parts'])}")
        print(f"   Safety Notes: {', '.join(classification['safety_notes'])}")
        print(f"   Next Steps: {', '.join(classification['next_steps'])}")
        print(f"   Processing Time: {data['processing_time_ms']:.2f}ms")
    else:
        print(f"❌ Classification failed: {response.status_code}")
        print(f"   Error: {response.text}")
    print()

def main():
    """Main function to test various plumbing issues"""
    print("🚰 Smart Plumbing Issue Classifier API - Test Examples")
    print("=" * 60)
    
    # Test health endpoint
    test_health()
    
    # Test categories endpoint
    test_categories()
    
    # Test various plumbing issues
    test_cases = [
        {
            "description": "Water is leaking from under the kitchen sink",
            "customer_info": {
                "customer_name": "John Doe",
                "phone_number": "555-1234",
                "address": "123 Main St"
            }
        },
        {
            "description": "Kitchen sink is clogged and water won't drain",
            "customer_info": {
                "customer_name": "Jane Smith",
                "phone_number": "555-5678"
            }
        },
        {
            "description": "No hot water coming from faucet",
            "customer_info": {
                "customer_name": "Bob Johnson",
                "phone_number": "555-9012"
            }
        },
        {
            "description": "Faucet handle is loose and dripping",
            "customer_info": {
                "customer_name": "Alice Brown",
                "phone_number": "555-3456"
            }
        },
        {
            "description": "Toilet won't flush properly",
            "customer_info": {
                "customer_name": "Charlie Wilson",
                "phone_number": "555-7890"
            }
        },
        {
            "description": "Emergency! Pipe burst and water is flooding the basement",
            "customer_info": {
                "customer_name": "David Emergency",
                "phone_number": "555-9999"
            }
        },
        {
            "description": "Slight drip from bathroom faucet",
            "customer_info": {
                "customer_name": "Eva Minor",
                "phone_number": "555-1111"
            }
        },
        {
            "description": "Sewer line is backing up into the house",
            "customer_info": {
                "customer_name": "Frank Sewer",
                "phone_number": "555-2222"
            }
        }
    ]
    
    print("🔧 Testing Issue Classifications:")
    print("-" * 40)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. ", end="")
        classify_issue(
            test_case["description"], 
            test_case.get("customer_info")
        )
        time.sleep(0.5)  # Small delay between requests
    
    print("✅ All tests completed!")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure it's running on http://localhost:8000")
        print("   Start the API with: python run.py")
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}") 