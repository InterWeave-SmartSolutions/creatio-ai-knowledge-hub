#!/usr/bin/env python3
"""
Simple login test to verify authentication and discover structure
"""

import requests
from bs4 import BeautifulSoup
import json

# Setup session
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
})

# Credentials
username = "amagown@interweave.biz"
password = "k1AOF6my!"

# URLs
base_url = "https://knowledge-hub.creatio.com"
login_url = f"{base_url}/solutions/user/login"

print("🔐 Testing login...")

# Method 1: Get login page and check structure
try:
    print("📄 Getting login page...")
    login_page = session.get(login_url, timeout=30)
    print(f"Login page status: {login_page.status_code}")
    
    soup = BeautifulSoup(login_page.content, 'html.parser')
    
    # Print form structure
    forms = soup.find_all('form')
    print(f"Found {len(forms)} forms")
    
    for i, form in enumerate(forms):
        print(f"\nForm {i+1}:")
        print(f"  Action: {form.get('action')}")
        print(f"  Method: {form.get('method', 'GET')}")
        
        inputs = form.find_all('input')
        print(f"  Inputs ({len(inputs)}):")
        for inp in inputs:
            print(f"    - {inp.get('name')} ({inp.get('type', 'text')}): {inp.get('value', '')}")
            
except Exception as e:
    print(f"Error getting login page: {e}")

# Method 2: Try JSON login
print("\n🔄 Trying JSON login...")
try:
    json_login_data = {
        'email': username,
        'password': password
    }
    
    response = session.post(
        login_url,
        json=json_login_data,
        headers={'Content-Type': 'application/json'},
        timeout=15
    )
    
    print(f"JSON login status: {response.status_code}")
    if response.status_code in [200, 302]:
        print("✅ JSON login appeared successful")
        
        # Try to access solutions page
        print("\n📋 Testing access to solutions page...")
        solutions_page = session.get(f"{base_url}/solutions", timeout=15)
        print(f"Solutions page status: {solutions_page.status_code}")
        
        if solutions_page.status_code == 200:
            print("✅ Solutions page accessible!")
            # Extract some links
            soup = BeautifulSoup(solutions_page.content, 'html.parser')
            links = soup.find_all('a', href=True)[:10]  # First 10 links
            print("Sample links:")
            for link in links:
                href = link['href']
                text = link.get_text(strip=True)[:50]
                if href.startswith('/') or 'knowledge-hub' in href:
                    print(f"  - {href}: {text}")
        else:
            print(f"❌ Solutions page not accessible: {solutions_page.status_code}")
            # Print response content sample
            print("Response preview:")
            print(solutions_page.text[:500])
            
    else:
        print(f"❌ JSON login failed: {response.status_code}")
        print("Response preview:")
        print(response.text[:500])
        
except Exception as e:
    print(f"Error with JSON login: {e}")

# Method 3: Try traditional form login
print("\n📝 Trying traditional form login...")
try:
    # Get login page again
    login_page = session.get(login_url, timeout=30)
    soup = BeautifulSoup(login_page.content, 'html.parser')
    
    form = soup.find('form')
    if form:
        # Prepare form data
        form_data = {}
        
        for input_field in form.find_all('input'):
            field_name = input_field.get('name')
            field_value = input_field.get('value', '')
            field_type = input_field.get('type', 'text')
            
            if field_name:
                if field_type in ['email', 'text'] and any(x in field_name.lower() for x in ['mail', 'user', 'login', 'name']):
                    form_data[field_name] = username
                elif field_type == 'password':
                    form_data[field_name] = password
                elif field_type == 'hidden':
                    form_data[field_name] = field_value
                    
        # Add common field names as fallback
        form_data.update({
            'name': username,
            'mail': username,
            'pass': password
        })
        
        print(f"Form data keys: {list(form_data.keys())}")
        
        # Submit form
        form_action = form.get('action', login_url)
        if not form_action.startswith('http'):
            form_action = f"{base_url}{form_action}"
            
        print(f"Submitting to: {form_action}")
        login_response = session.post(form_action, data=form_data, timeout=30)
        print(f"Form login status: {login_response.status_code}")
        
        if login_response.status_code in [200, 302]:
            # Test access again
            solutions_page = session.get(f"{base_url}/solutions", timeout=15)
            print(f"Post-login solutions access: {solutions_page.status_code}")
            
            if solutions_page.status_code == 200:
                print("✅ Form login successful!")
            else:
                print("❌ Still can't access solutions page")
        
except Exception as e:
    print(f"Error with form login: {e}")

print("\n🏁 Login test completed")
