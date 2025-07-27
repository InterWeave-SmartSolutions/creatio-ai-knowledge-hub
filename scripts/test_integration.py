#!/usr/bin/env python3
"""
Test script to verify MCP server integration with developer course content
"""

import requests
import json
import sys
import os
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000"
TEST_USERNAME = "admin"
TEST_PASSWORD = "password"

def get_auth_token():
    """Get authentication token"""
    response = requests.post(
        f"{BASE_URL}/auth/token",
        data={"username": TEST_USERNAME, "password": TEST_PASSWORD}
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Failed to get auth token: {response.status_code}")
        return None

def test_developer_course_endpoint():
    """Test the developer course endpoint"""
    token = get_auth_token()
    if not token:
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 1: Search all developer course content
    print("Testing developer course search (all content)...")
    response = requests.post(
        f"{BASE_URL}/developer-course",
        json={
            "content_type": "all",
            "search_query": "integration",
            "limit": 5
        },
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Found {data['total_results']} results")
        for result in data['results'][:2]:
            print(f"  - {result['title']} ({result['content_type']})")
    else:
        print(f"✗ Failed: {response.status_code} - {response.text}")
        return False
    
    # Test 2: Search PDF content only
    print("\nTesting developer course search (PDF only)...")
    response = requests.post(
        f"{BASE_URL}/developer-course",
        json={
            "content_type": "pdf",
            "search_query": "configuration",
            "limit": 3
        },
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Found {data['total_results']} PDF results")
    else:
        print(f"✗ Failed: {response.status_code} - {response.text}")
        return False
    
    # Test 3: Search video content only
    print("\nTesting developer course search (Video only)...")
    response = requests.post(
        f"{BASE_URL}/developer-course",
        json={
            "content_type": "video",
            "search_query": "development",
            "limit": 3
        },
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Found {data['total_results']} video results")
    else:
        print(f"✗ Failed: {response.status_code} - {response.text}")
        return False
        
    return True

def test_content_search_integration():
    """Test general content search includes developer course"""
    token = get_auth_token()
    if not token:
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\nTesting general content search...")
    response = requests.post(
        f"{BASE_URL}/content-search",
        json={
            "query": "API",
            "content_type": "all",
            "limit": 10
        },
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Found {data['total_results']} total results")
        
        # Check if results include different content types
        content_types = set()
        for result in data['results']:
            content_types.add(result.get('type', 'unknown'))
        
        print(f"  Content types found: {', '.join(content_types)}")
        return True
    else:
        print(f"✗ Failed: {response.status_code} - {response.text}")
        return False

def test_video_transcript_integration():
    """Test video transcript loading from both locations"""
    token = get_auth_token()
    if not token:
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Check if there are any developer course videos
    dev_course_path = Path("ai_optimization/creatio-academy-db/developer_course/transcripts")
    if dev_course_path.exists():
        transcript_files = list(dev_course_path.glob("*.json"))
        if transcript_files:
            # Extract video ID from filename
            video_id = transcript_files[0].stem.replace("_transcript", "")
            
            print(f"\nTesting video transcript for {video_id}...")
            response = requests.get(
                f"{BASE_URL}/video-transcripts/{video_id}",
                params={"include_metadata": True, "include_summary": True},
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Successfully loaded transcript for {video_id}")
                print(f"  Has metadata: {'metadata' in data['transcript']}")
                print(f"  Has summary: {'enhanced_summary' in data['transcript']}")
                return True
            else:
                print(f"✗ Failed: {response.status_code} - {response.text}")
                return False
    
    print("No developer course video transcripts found to test")
    return True

def test_health_check():
    """Test basic health check"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Server healthy: {data['status']}")
        return True
    else:
        print(f"✗ Health check failed: {response.status_code}")
        return False

def check_data_files():
    """Check if required data files exist"""
    print("Checking data file structure...")
    
    # Check developer course files
    dev_course_path = Path("ai_optimization/creatio-academy-db/developer_course")
    master_index = dev_course_path / "master_index.json"
    
    if master_index.exists():
        print("✓ Developer course master index found")
        with open(master_index) as f:
            data = json.load(f)
            content_count = len(data.get('content_index', {}))
            print(f"  Contains {content_count} content items")
    else:
        print("✗ Developer course master index not found")
        return False
    
    # Check legacy files
    legacy_path = Path("transcriptions")
    if legacy_path.exists():
        print("✓ Legacy transcriptions directory found")
    else:
        print("! Legacy transcriptions directory not found (optional)")
    
    return True

def main():
    """Run all integration tests"""
    print("=== MCP Server Integration Tests ===\n")
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("✗ Server not responding properly")
            sys.exit(1)
    except requests.exceptions.RequestException:
        print("✗ Server not running or not accessible")
        print("Please start the MCP server with: uvicorn mcp_server:app --reload")
        sys.exit(1)
    
    print("✓ Server is running\n")
    
    # Run tests
    tests = [
        ("Data Files", check_data_files),
        ("Health Check", test_health_check),
        ("Developer Course API", test_developer_course_endpoint),
        ("Content Search Integration", test_content_search_integration),
        ("Video Transcript Integration", test_video_transcript_integration),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} PASSED")
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} ERROR: {e}")
    
    print(f"\n=== Results: {passed}/{total} tests passed ===")
    
    if passed == total:
        print("🎉 All integration tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Check the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
