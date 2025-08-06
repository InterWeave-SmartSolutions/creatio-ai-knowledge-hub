#!/usr/bin/env python3
"""
Updated login test with proper form fields
"""

import requests
from bs4 import BeautifulSoup

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

print("🔐 Testing proper form login...")

try:
    # Get login page
    print("📄 Getting login page...")
    login_page = session.get(login_url, timeout=30)
    print(f"Login page status: {login_page.status_code}")
    
    soup = BeautifulSoup(login_page.content, 'html.parser')
    form = soup.find('form')
    
    if form:
        # Extract all form data exactly as shown
        form_data = {}
        
        for input_field in form.find_all('input'):
            field_name = input_field.get('name')
            field_value = input_field.get('value', '')
            
            if field_name:
                if field_name == 'name':
                    form_data[field_name] = username
                elif field_name == 'pass':
                    form_data[field_name] = password
                else:
                    form_data[field_name] = field_value
                    
        print(f"Form data: {form_data}")
        
        # Submit form with proper action
        form_action = form.get('action')
        if not form_action.startswith('http'):
            form_action = f"{base_url}{form_action}"
            
        print(f"Submitting to: {form_action}")
        
        # Submit with allow_redirects=False to see what happens
        login_response = session.post(
            form_action, 
            data=form_data, 
            timeout=30,
            allow_redirects=False
        )
        print(f"Form login status: {login_response.status_code}")
        print(f"Response headers: {dict(login_response.headers)}")
        
        if login_response.status_code in [302, 303]:
            print("✅ Login redirect received - following...")
            
            # Get the redirect location
            redirect_url = login_response.headers.get('Location')
            print(f"Redirect location: {redirect_url}")
            
            if redirect_url:
                if not redirect_url.startswith('http'):
                    redirect_url = f"{base_url}{redirect_url}"
                    
                # Follow redirect
                redirect_response = session.get(redirect_url, timeout=30)
                print(f"After redirect status: {redirect_response.status_code}")
                
                # Now try to access solutions
                print("\n📋 Testing solutions access after proper login...")
                solutions_response = session.get(f"{base_url}/solutions/", timeout=30)
                print(f"Solutions page status: {solutions_response.status_code}")
                
                if solutions_response.status_code == 200:
                    print("🎉 SUCCESS! Solutions page is now accessible!")
                    
                    # Extract some sample content
                    soup = BeautifulSoup(solutions_response.content, 'html.parser')
                    
                    # Look for solution links
                    solution_links = []
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        if '/solutions/' in href and href != '/solutions/':
                            full_url = href if href.startswith('http') else f"{base_url}{href}"
                            solution_links.append({
                                'url': full_url,
                                'text': link.get_text(strip=True)[:100]
                            })
                    
                    print(f"\n🔗 Found {len(solution_links)} solution links:")
                    for i, link in enumerate(solution_links[:10]):  # Show first 10
                        print(f"  {i+1}. {link['url']}")
                        print(f"     {link['text']}")
                        print()
                        
                else:
                    print(f"❌ Solutions page still not accessible: {solutions_response.status_code}")
                    # Show response content for debugging
                    content_preview = solutions_response.text[:500]
                    print(f"Response preview: {content_preview}")
                    
        elif login_response.status_code == 200:
            print("⚠️ Login returned 200 - checking if we're logged in...")
            
            # Check if we're on a success page or still on login
            response_text = login_response.text.lower()
            if 'invalid' in response_text or 'error' in response_text or 'login' in response_text:
                print("❌ Login failed - still on login page")
                print("Response preview:")
                print(login_response.text[:500])
            else:
                print("✅ Login may have succeeded - testing access...")
                solutions_response = session.get(f"{base_url}/solutions/", timeout=30)
                print(f"Solutions page status: {solutions_response.status_code}")
        else:
            print(f"❌ Login failed with status: {login_response.status_code}")
            print("Response preview:")
            print(login_response.text[:500])
            
except Exception as e:
    print(f"Error during login: {e}")

print("\n🏁 Enhanced login test completed")
