#!/usr/bin/env python3
"""
Comprehensive Investigation: Knowledge Hub Access Barriers
Analyzes authentication mechanisms, security measures, and access restrictions
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from urllib.parse import urljoin, urlparse, parse_qs
import re
from datetime import datetime

# Setup detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('access_investigation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AccessInvestigator:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
        
        # Multiple credential sets
        self.credentials = [
            {"username": "amagown@interweave.biz", "password": "k1AOF6my!", "label": "Set 1"},
            {"username": "bmagown@interweave.biz", "password": "Interweave$$0911", "label": "Set 2"}
        ]
        
        # URLs to investigate
        self.base_url = "https://knowledge-hub.creatio.com"
        self.login_url = f"{self.base_url}/solutions/user/login"
        self.test_urls = [
            f"{self.base_url}/solutions/",
            f"{self.base_url}/solutions/general",
            f"{self.base_url}/solutions/crm", 
            f"{self.base_url}/guides",
            f"{self.base_url}/articles"
        ]
        
        self.investigation_results = {
            'timestamp': datetime.now().isoformat(),
            'site_analysis': {},
            'authentication_analysis': {},
            'security_measures': {},
            'access_attempts': {},
            'recommendations': []
        }
        
    def investigate_site_structure(self):
        """Analyze the basic site structure and responses"""
        logger.info("🔍 Investigating site structure and responses...")
        
        site_analysis = {}
        
        # Test basic connectivity
        try:
            response = self.session.get(self.base_url, timeout=15)
            site_analysis['base_url_status'] = response.status_code
            site_analysis['base_url_headers'] = dict(response.headers)
            site_analysis['base_url_redirects'] = len(response.history)
            
            if response.history:
                site_analysis['redirect_chain'] = [r.url for r in response.history]
                site_analysis['final_url'] = response.url
                
        except Exception as e:
            site_analysis['base_url_error'] = str(e)
            
        # Test login page accessibility
        try:
            login_response = self.session.get(self.login_url, timeout=15)
            site_analysis['login_page_status'] = login_response.status_code
            site_analysis['login_page_headers'] = dict(login_response.headers)
            
            if login_response.status_code == 200:
                soup = BeautifulSoup(login_response.content, 'html.parser')
                
                # Analyze login form
                forms = soup.find_all('form')
                site_analysis['login_forms_count'] = len(forms)
                
                if forms:
                    form = forms[0]
                    site_analysis['login_form_action'] = form.get('action')
                    site_analysis['login_form_method'] = form.get('method', 'GET')
                    
                    # Extract all form fields
                    form_fields = {}
                    for inp in form.find_all('input'):
                        field_name = inp.get('name')
                        field_type = inp.get('type', 'text')
                        field_value = inp.get('value', '')
                        if field_name:
                            form_fields[field_name] = {
                                'type': field_type,
                                'value': field_value,
                                'required': inp.get('required') is not None
                            }
                    site_analysis['login_form_fields'] = form_fields
                    
                # Check for JavaScript requirements
                scripts = soup.find_all('script')
                site_analysis['javascript_scripts_count'] = len(scripts)
                
                # Look for CSRF or security tokens
                csrf_indicators = soup.find_all(attrs={'name': re.compile(r'csrf|token|security', re.I)})
                site_analysis['csrf_tokens_found'] = len(csrf_indicators)
                
        except Exception as e:
            site_analysis['login_page_error'] = str(e)
            
        self.investigation_results['site_analysis'] = site_analysis
        logger.info(f"✅ Site structure analysis complete")
        
    def test_authentication_methods(self):
        """Test different authentication approaches"""
        logger.info("🔐 Testing authentication methods...")
        
        auth_results = {}
        
        for creds in self.credentials:
            cred_label = creds['label']
            logger.info(f"Testing {cred_label}: {creds['username']}")
            
            cred_results = {
                'username': creds['username'],
                'attempts': []
            }
            
            # Method 1: Standard form submission
            attempt1 = self.attempt_form_login(creds)
            cred_results['attempts'].append({
                'method': 'standard_form',
                'result': attempt1
            })
            
            # Method 2: JSON login
            attempt2 = self.attempt_json_login(creds)
            cred_results['attempts'].append({
                'method': 'json_payload',
                'result': attempt2
            })
            
            # Method 3: Ajax-style login
            attempt3 = self.attempt_ajax_login(creds)
            cred_results['attempts'].append({
                'method': 'ajax_request',
                'result': attempt3
            })
            
            auth_results[cred_label] = cred_results
            
            # Reset session between credential attempts
            self.reset_session()
            
        self.investigation_results['authentication_analysis'] = auth_results
        
    def attempt_form_login(self, creds):
        """Attempt standard form-based login"""
        try:
            # Get fresh login page
            login_page = self.session.get(self.login_url, timeout=15)
            if login_page.status_code != 200:
                return {'error': f'Cannot access login page: {login_page.status_code}'}
                
            soup = BeautifulSoup(login_page.content, 'html.parser')
            form = soup.find('form')
            
            if not form:
                return {'error': 'No login form found'}
                
            # Build complete form data
            form_data = {}
            for inp in form.find_all('input'):
                field_name = inp.get('name')
                field_value = inp.get('value', '')
                field_type = inp.get('type', 'text')
                
                if field_name:
                    if field_name == 'name' or 'email' in field_name.lower() or 'user' in field_name.lower():
                        form_data[field_name] = creds['username']
                    elif field_name == 'pass' or 'password' in field_name.lower():
                        form_data[field_name] = creds['password']
                    else:
                        form_data[field_name] = field_value
                        
            # Determine action URL
            form_action = form.get('action', self.login_url)
            if not form_action.startswith('http'):
                form_action = urljoin(self.base_url, form_action)
                
            # Submit form
            login_response = self.session.post(
                form_action,
                data=form_data,
                timeout=30,
                allow_redirects=False  # Don't follow redirects initially
            )
            
            result = {
                'status_code': login_response.status_code,
                'headers': dict(login_response.headers),
                'form_data_sent': {k: v for k, v in form_data.items() if 'pass' not in k.lower()},
                'response_size': len(login_response.content),
                'cookies_received': len(login_response.cookies),
                'redirect_location': login_response.headers.get('Location')
            }
            
            # Check response content for success/failure indicators
            if login_response.status_code in [200, 302, 303]:
                response_text = login_response.text.lower()
                result['success_indicators'] = {
                    'has_error_message': any(error in response_text for error in ['error', 'invalid', 'failed', 'incorrect']),
                    'has_success_message': any(success in response_text for success in ['welcome', 'dashboard', 'success']),
                    'still_has_login_form': 'login' in response_text and 'password' in response_text
                }
                
            # If redirect, follow it
            if login_response.status_code in [302, 303] and result['redirect_location']:
                redirect_response = self.session.get(result['redirect_location'], timeout=15)
                result['after_redirect'] = {
                    'status_code': redirect_response.status_code,
                    'final_url': redirect_response.url,
                    'content_size': len(redirect_response.content)
                }
                
            return result
            
        except Exception as e:
            return {'error': str(e)}
            
    def attempt_json_login(self, creds):
        """Attempt JSON-based login"""
        try:
            json_data = {
                'username': creds['username'],
                'password': creds['password'],
                'email': creds['username'],
                'name': creds['username']
            }
            
            response = self.session.post(
                self.login_url,
                json=json_data,
                headers={'Content-Type': 'application/json'},
                timeout=15,
                allow_redirects=False
            )
            
            return {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'content_type': response.headers.get('Content-Type', ''),
                'response_size': len(response.content),
                'cookies_received': len(response.cookies)
            }
            
        except Exception as e:
            return {'error': str(e)}
            
    def attempt_ajax_login(self, creds):
        """Attempt AJAX-style login"""
        try:
            # Add AJAX headers
            ajax_headers = {
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
            
            form_data = {
                'name': creds['username'],
                'pass': creds['password']
            }
            
            response = self.session.post(
                self.login_url,
                data=form_data,
                headers=ajax_headers,
                timeout=15,
                allow_redirects=False
            )
            
            return {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'content_type': response.headers.get('Content-Type', ''),
                'response_size': len(response.content),
                'cookies_received': len(response.cookies)
            }
            
        except Exception as e:
            return {'error': str(e)}
            
    def analyze_access_patterns(self):
        """Analyze access patterns to protected content"""
        logger.info("📊 Analyzing access patterns...")
        
        access_analysis = {}
        
        # Test access without authentication
        logger.info("Testing unauthenticated access...")
        unauth_results = {}
        
        for url in self.test_urls:
            try:
                response = self.session.get(url, timeout=15, allow_redirects=False)
                unauth_results[url] = {
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'redirect_location': response.headers.get('Location'),
                    'content_preview': response.text[:500] if response.text else None
                }
            except Exception as e:
                unauth_results[url] = {'error': str(e)}
                
        access_analysis['unauthenticated_access'] = unauth_results
        
        # Test with different User-Agent strings
        logger.info("Testing different User-Agent strings...")
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'CreatioBot/1.0 (+https://www.creatio.com/bot)',
            'curl/7.68.0'
        ]
        
        ua_results = {}
        for ua in user_agents:
            self.session.headers['User-Agent'] = ua
            try:
                response = self.session.get(f"{self.base_url}/solutions/", timeout=10)
                ua_results[ua[:50]] = {
                    'status_code': response.status_code,
                    'blocked': response.status_code in [403, 406, 429]
                }
            except Exception as e:
                ua_results[ua[:50]] = {'error': str(e)}
                
        access_analysis['user_agent_tests'] = ua_results
        
        # Reset to original User-Agent
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        
        self.investigation_results['access_attempts'] = access_analysis
        
    def detect_security_measures(self):
        """Detect various security measures"""
        logger.info("🛡️ Detecting security measures...")
        
        security_analysis = {}
        
        # Check for rate limiting
        logger.info("Testing rate limiting...")
        rate_limit_results = []
        
        for i in range(10):
            try:
                start_time = time.time()
                response = self.session.get(f"{self.base_url}/solutions/", timeout=5)
                end_time = time.time()
                
                rate_limit_results.append({
                    'attempt': i + 1,
                    'status_code': response.status_code,
                    'response_time': end_time - start_time,
                    'rate_limit_headers': {
                        k: v for k, v in response.headers.items() 
                        if 'rate' in k.lower() or 'limit' in k.lower() or 'retry' in k.lower()
                    }
                })
                
                time.sleep(0.5)  # Small delay between requests
                
            except Exception as e:
                rate_limit_results.append({
                    'attempt': i + 1,
                    'error': str(e)
                })
                
        security_analysis['rate_limiting'] = rate_limit_results
        
        # Check for IP-based restrictions
        logger.info("Analyzing IP restrictions...")
        try:
            # Try to get our IP from the server's perspective
            ip_check_response = self.session.get('https://httpbin.org/ip', timeout=10)
            if ip_check_response.status_code == 200:
                our_ip = ip_check_response.json().get('origin', 'unknown')
                security_analysis['client_ip'] = our_ip
        except:
            security_analysis['client_ip'] = 'unknown'
            
        # Check for CAPTCHA or bot detection
        logger.info("Checking for bot detection...")
        try:
            response = self.session.get(f"{self.base_url}/solutions/", timeout=15)
            response_text = response.text.lower()
            
            bot_detection = {
                'has_captcha': 'captcha' in response_text or 'recaptcha' in response_text,
                'has_cloudflare': 'cloudflare' in response_text or 'cf-ray' in str(response.headers),
                'has_bot_detection': any(indicator in response_text for indicator in [
                    'bot detected', 'access denied', 'blocked', 'security check'
                ]),
                'suspicious_headers': {
                    k: v for k, v in response.headers.items() 
                    if any(sec in k.lower() for sec in ['security', 'protection', 'cf-', 'x-'])
                }
            }
            
            security_analysis['bot_detection'] = bot_detection
            
        except Exception as e:
            security_analysis['bot_detection'] = {'error': str(e)}
            
        self.investigation_results['security_measures'] = security_analysis
        
    def check_session_requirements(self):
        """Check for specific session or cookie requirements"""
        logger.info("🍪 Analyzing session and cookie requirements...")
        
        session_analysis = {}
        
        # Attempt login with first credential set and analyze session behavior
        try:
            # Get login page and extract all cookies
            login_page = self.session.get(self.login_url, timeout=15)
            initial_cookies = dict(self.session.cookies)
            
            # Attempt login
            soup = BeautifulSoup(login_page.content, 'html.parser')
            form = soup.find('form')
            
            if form:
                form_data = {}
                for inp in form.find_all('input'):
                    field_name = inp.get('name')
                    field_value = inp.get('value', '')
                    
                    if field_name:
                        if field_name == 'name':
                            form_data[field_name] = self.credentials[0]['username']
                        elif field_name == 'pass':
                            form_data[field_name] = self.credentials[0]['password']
                        else:
                            form_data[field_name] = field_value
                            
                # Submit login
                login_response = self.session.post(
                    urljoin(self.base_url, form.get('action', self.login_url)),
                    data=form_data,
                    timeout=30,
                    allow_redirects=True
                )
                
                post_login_cookies = dict(self.session.cookies)
                
                session_analysis['cookie_analysis'] = {
                    'initial_cookies': initial_cookies,
                    'post_login_cookies': post_login_cookies,
                    'new_cookies': {k: v for k, v in post_login_cookies.items() if k not in initial_cookies},
                    'login_response_status': login_response.status_code,
                    'login_final_url': login_response.url
                }
                
                # Test access with acquired session
                test_response = self.session.get(f"{self.base_url}/solutions/", timeout=15)
                session_analysis['authenticated_access_test'] = {
                    'status_code': test_response.status_code,
                    'content_preview': test_response.text[:500],
                    'has_login_indicators': 'login' in test_response.text.lower()
                }
                
        except Exception as e:
            session_analysis['error'] = str(e)
            
        self.investigation_results['session_analysis'] = session_analysis
        
    def reset_session(self):
        """Reset session to clean state"""
        self.session.cookies.clear()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
    def generate_recommendations(self):
        """Generate recommendations based on investigation results"""
        logger.info("💡 Generating recommendations...")
        
        recommendations = []
        
        # Analyze results and provide recommendations
        site_analysis = self.investigation_results.get('site_analysis', {})
        auth_analysis = self.investigation_results.get('authentication_analysis', {})
        security_measures = self.investigation_results.get('security_measures', {})
        
        # Check login form accessibility
        if site_analysis.get('login_forms_count', 0) == 0:
            recommendations.append({
                'issue': 'No login form found',
                'recommendation': 'Check if login URL is correct or if JavaScript is required to load the form',
                'priority': 'high'
            })
            
        # Check for successful login responses
        login_success_found = False
        for cred_set in auth_analysis.values():
            for attempt in cred_set.get('attempts', []):
                result = attempt.get('result', {})
                if result.get('status_code') in [200, 302, 303] and not result.get('error'):
                    login_success_found = True
                    
        if not login_success_found:
            recommendations.append({
                'issue': 'No successful login responses detected',
                'recommendation': 'Verify credentials are correct and account is active',
                'priority': 'high'
            })
            
        # Check for access issues
        if all(result.get('status_code') == 403 for result in self.investigation_results.get('access_attempts', {}).get('unauthenticated_access', {}).values()):
            recommendations.append({
                'issue': 'All content returns 403 Forbidden',
                'recommendation': 'Content requires valid authentication and proper account permissions',
                'priority': 'medium'
            })
            
        # Check for bot detection
        bot_detection = security_measures.get('bot_detection', {})
        if bot_detection.get('has_captcha') or bot_detection.get('has_bot_detection'):
            recommendations.append({
                'issue': 'Bot detection or CAPTCHA present',
                'recommendation': 'Use browser automation tools (Selenium) or request API access',
                'priority': 'high'
            })
            
        # Check for rate limiting
        rate_limit_results = security_measures.get('rate_limiting', [])
        if any(result.get('status_code') == 429 for result in rate_limit_results):
            recommendations.append({
                'issue': 'Rate limiting detected',
                'recommendation': 'Implement delays between requests and respect rate limits',
                'priority': 'medium'
            })
            
        self.investigation_results['recommendations'] = recommendations
        
    def save_investigation_results(self):
        """Save comprehensive investigation results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"access_investigation_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.investigation_results, f, indent=2, ensure_ascii=False, default=str)
            
        logger.info(f"📋 Investigation results saved to: {filename}")
        return filename
        
    def run_investigation(self):
        """Run complete investigation"""
        logger.info("🚀 Starting comprehensive access investigation...")
        
        try:
            # Step 1: Analyze site structure
            self.investigate_site_structure()
            
            # Step 2: Test authentication methods
            self.test_authentication_methods()
            
            # Step 3: Analyze access patterns
            self.analyze_access_patterns()
            
            # Step 4: Detect security measures
            self.detect_security_measures()
            
            # Step 5: Check session requirements
            self.check_session_requirements()
            
            # Step 6: Generate recommendations
            self.generate_recommendations()
            
            # Step 7: Save results
            results_file = self.save_investigation_results()
            
            logger.info("✅ Investigation complete!")
            return results_file
            
        except Exception as e:
            logger.error(f"❌ Investigation failed: {str(e)}")
            return None

if __name__ == "__main__":
    investigator = AccessInvestigator()
    results_file = investigator.run_investigation()
    
    if results_file:
        print(f"\n🎯 Investigation completed successfully!")
        print(f"📋 Detailed results saved in: {results_file}")
        print(f"📊 Check the logs in: access_investigation.log")
        
        # Print summary of key findings
        print(f"\n📋 Key Findings Summary:")
        print(f"{'='*50}")
        
        if investigator.investigation_results.get('recommendations'):
            print("🔍 Recommendations:")
            for i, rec in enumerate(investigator.investigation_results['recommendations'], 1):
                print(f"  {i}. {rec['issue']}")
                print(f"     → {rec['recommendation']}")
                print(f"     Priority: {rec['priority']}")
                print()
    else:
        print("❌ Investigation failed. Check the logs for details.")
