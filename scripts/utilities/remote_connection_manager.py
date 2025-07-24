#!/usr/bin/env python3
"""
Remote Connection Manager for Creatio Environments
Handles secure connections to mkpdev-interweave.creatio.com and other environments
"""

import os
import sys
import yaml
import json
import time
import logging
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from pathlib import Path
import keyring
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from requests.auth import HTTPBasicAuth
import hashlib
import base64

class CreatioConnectionManager:
    """Manages secure connections to Creatio environments"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or "config/remote_connections.yaml"
        self.config = self._load_config()
        self.sessions = {}
        self.tokens = {}
        self.logger = self._setup_logging()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            config_file = Path(self.config_path)
            if not config_file.exists():
                raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
            
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading configuration: {e}")
            sys.exit(1)
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration"""
        log_level = self.config.get('global_settings', {}).get('log_level', 'INFO')
        log_file = self.config.get('global_settings', {}).get('log_file', 'logs/remote_connections.log')
        
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        return logging.getLogger(__name__)
    
    def _get_credential(self, env_var: str) -> Optional[str]:
        """Get credential from environment variable or keyring"""
        credential = os.getenv(env_var)
        if credential:
            return credential
        
        # Try keyring if env var not found
        storage_type = self.config.get('credentials', {}).get('storage_type', 'keyring')
        if storage_type == 'keyring':
            service = self.config.get('credentials', {}).get('keyring_service', 'creatio-ai-hub')
            try:
                return keyring.get_password(service, env_var)
            except Exception as e:
                self.logger.warning(f"Could not retrieve credential from keyring: {e}")
        
        return None
    
    def _create_session(self, env_name: str) -> requests.Session:
        """Create configured requests session for environment"""
        env_config = self.config['environments'][env_name]
        connection_config = env_config.get('connection', {})
        
        session = requests.Session()
        
        # Configure retries
        retry_strategy = Retry(
            total=connection_config.get('retry_attempts', 3),
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"],
            backoff_factor=connection_config.get('retry_delay', 5)
        )
        
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=connection_config.get('pool_connections', 10),
            pool_maxsize=connection_config.get('pool_maxsize', 20)
        )
        
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set timeout
        session.timeout = connection_config.get('timeout', 30)
        
        # Set user agent
        user_agent = self.config.get('global_settings', {}).get('user_agent', 'CreatioAI-KnowledgeHub/1.0')
        session.headers.update({'User-Agent': user_agent})
        
        # Configure SSL verification
        session.verify = connection_config.get('verify_ssl', True)
        
        # Configure proxy if enabled
        proxy_config = self.config.get('proxy', {})
        if proxy_config.get('enabled', False):
            proxies = {}
            if proxy_config.get('http_proxy'):
                proxies['http'] = os.path.expandvars(proxy_config['http_proxy'])
            if proxy_config.get('https_proxy'):
                proxies['https'] = os.path.expandvars(proxy_config['https_proxy'])
            session.proxies.update(proxies)
        
        return session
    
    def _authenticate_oauth2(self, env_name: str) -> str:
        """Perform OAuth2 authentication"""
        env_config = self.config['environments'][env_name]
        auth_config = env_config['auth']
        
        client_id = self._get_credential(auth_config['client_id_env'])
        client_secret = self._get_credential(auth_config['client_secret_env'])
        
        if not client_id or not client_secret:
            raise ValueError(f"Missing OAuth2 credentials for environment: {env_name}")
        
        session = self._get_session(env_name)
        token_url = env_config['base_url'] + auth_config['token_endpoint']
        
        data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'scope': auth_config.get('scope', '')
        }
        
        response = session.post(token_url, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        access_token = token_data['access_token']
        
        # Store token with expiration
        expires_in = token_data.get('expires_in', 3600)
        self.tokens[env_name] = {
            'access_token': access_token,
            'expires_at': datetime.now() + timedelta(seconds=expires_in - 60)  # 60s buffer
        }
        
        self.logger.info(f"OAuth2 authentication successful for {env_name}")
        return access_token
    
    def _authenticate_basic(self, env_name: str) -> None:
        """Configure basic authentication"""
        env_config = self.config['environments'][env_name]
        auth_config = env_config['auth']
        
        username = self._get_credential(auth_config['username_env'])
        password = self._get_credential(auth_config['password_env'])
        
        if not username or not password:
            raise ValueError(f"Missing basic auth credentials for environment: {env_name}")
        
        session = self._get_session(env_name)
        session.auth = HTTPBasicAuth(username, password)
        
        self.logger.info(f"Basic authentication configured for {env_name}")
    
    def _get_session(self, env_name: str) -> requests.Session:
        """Get or create session for environment"""
        if env_name not in self.sessions:
            self.sessions[env_name] = self._create_session(env_name)
        return self.sessions[env_name]
    
    def connect(self, env_name: str = None) -> requests.Session:
        """Connect to specified environment"""
        if env_name is None:
            env_name = self.config.get('default_environment', 'production')
        
        if env_name not in self.config['environments']:
            raise ValueError(f"Unknown environment: {env_name}")
        
        env_config = self.config['environments'][env_name]
        auth_config = env_config.get('auth', {})
        auth_type = auth_config.get('type', 'oauth2')
        
        session = self._get_session(env_name)
        
        if auth_type == 'oauth2':
            # Check if token exists and is valid
            token_info = self.tokens.get(env_name)
            if not token_info or datetime.now() >= token_info['expires_at']:
                access_token = self._authenticate_oauth2(env_name)
            else:
                access_token = token_info['access_token']
            
            session.headers.update({'Authorization': f'Bearer {access_token}'})
            
        elif auth_type == 'basic':
            self._authenticate_basic(env_name)
            
        elif auth_type == 'api_key':
            api_key = self._get_credential(auth_config['api_key_env'])
            if not api_key:
                raise ValueError(f"Missing API key for environment: {env_name}")
            session.headers.update({'X-API-Key': api_key})
        
        self.logger.info(f"Connected to environment: {env_name} ({env_config['name']})")
        return session
    
    def test_connection(self, env_name: str = None) -> bool:
        """Test connection to environment"""
        try:
            if env_name is None:
                env_name = self.config.get('default_environment', 'production')
            
            session = self.connect(env_name)
            env_config = self.config['environments'][env_name]
            
            # Try health check endpoint if available
            health_config = self.config.get('health_check', {})
            if health_config.get('enabled', True):
                health_url = env_config['base_url'] + health_config.get('endpoint', '/health')
                response = session.get(health_url, timeout=health_config.get('timeout', 10))
                
                if response.status_code == 200:
                    self.logger.info(f"Health check passed for {env_name}")
                    return True
                else:
                    self.logger.warning(f"Health check failed for {env_name}: {response.status_code}")
            
            # Fallback: try to list packages
            list_url = env_config['base_url'] + env_config['package_endpoints']['list']
            response = session.get(list_url, timeout=10)
            
            if response.status_code in [200, 401, 403]:  # 401/403 means auth issue, but connection works
                self.logger.info(f"Connection test passed for {env_name}")
                return True
            else:
                self.logger.error(f"Connection test failed for {env_name}: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Connection test failed for {env_name}: {e}")
            return False
    
    def list_packages(self, env_name: str = None, search_term: str = None) -> List[Dict[str, Any]]:
        """List available packages"""
        if env_name is None:
            env_name = self.config.get('default_environment', 'production')
        
        session = self.connect(env_name)
        env_config = self.config['environments'][env_name]
        
        if search_term:
            url = env_config['base_url'] + env_config['package_endpoints']['search']
            params = {'q': search_term}
        else:
            url = env_config['base_url'] + env_config['package_endpoints']['list']
            params = {}
        
        response = session.get(url, params=params)
        response.raise_for_status()
        
        packages = response.json()
        self.logger.info(f"Retrieved {len(packages)} packages from {env_name}")
        return packages
    
    def download_package(self, package_id: str, destination: str = None, env_name: str = None) -> str:
        """Download a package"""
        if env_name is None:
            env_name = self.config.get('default_environment', 'production')
        
        session = self.connect(env_name)
        env_config = self.config['environments'][env_name]
        
        url = env_config['base_url'] + env_config['package_endpoints']['download'].format(package_id=package_id)
        
        if destination is None:
            temp_dir = self.config.get('global_settings', {}).get('temp_directory', '/tmp/creatio_packages')
            os.makedirs(temp_dir, exist_ok=True)
            destination = os.path.join(temp_dir, f"{package_id}.zip")
        
        self.logger.info(f"Downloading package {package_id} from {env_name}")
        
        response = session.get(url, stream=True)
        response.raise_for_status()
        
        chunk_size = self.config.get('global_settings', {}).get('download_chunk_size', 8192)
        
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
        
        self.logger.info(f"Package downloaded to: {destination}")
        return destination
    
    def get_package_metadata(self, package_id: str, env_name: str = None) -> Dict[str, Any]:
        """Get package metadata"""
        if env_name is None:
            env_name = self.config.get('default_environment', 'production')
        
        session = self.connect(env_name)
        env_config = self.config['environments'][env_name]
        
        url = env_config['base_url'] + env_config['package_endpoints']['metadata'].format(package_id=package_id)
        
        response = session.get(url)
        response.raise_for_status()
        
        metadata = response.json()
        self.logger.info(f"Retrieved metadata for package {package_id} from {env_name}")
        return metadata
    
    def close_connections(self):
        """Close all active sessions"""
        for env_name, session in self.sessions.items():
            session.close()
            self.logger.info(f"Closed connection to {env_name}")
        
        self.sessions.clear()
        self.tokens.clear()


def main():
    """Command line interface for connection manager"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Creatio Remote Connection Manager')
    parser.add_argument('--config', '-c', help='Configuration file path')
    parser.add_argument('--environment', '-e', help='Environment name')
    parser.add_argument('command', choices=['test', 'list', 'download', 'metadata'])
    parser.add_argument('--package-id', '-p', help='Package ID for download/metadata')
    parser.add_argument('--search', '-s', help='Search term for package listing')
    parser.add_argument('--destination', '-d', help='Download destination')
    
    args = parser.parse_args()
    
    try:
        manager = CreatioConnectionManager(args.config)
        
        if args.command == 'test':
            result = manager.test_connection(args.environment)
            print(f"Connection test: {'PASSED' if result else 'FAILED'}")
            sys.exit(0 if result else 1)
            
        elif args.command == 'list':
            packages = manager.list_packages(args.environment, args.search)
            print(json.dumps(packages, indent=2))
            
        elif args.command == 'download':
            if not args.package_id:
                print("Package ID required for download")
                sys.exit(1)
            path = manager.download_package(args.package_id, args.destination, args.environment)
            print(f"Downloaded to: {path}")
            
        elif args.command == 'metadata':
            if not args.package_id:
                print("Package ID required for metadata")
                sys.exit(1)
            metadata = manager.get_package_metadata(args.package_id, args.environment)
            print(json.dumps(metadata, indent=2))
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        manager.close_connections()


if __name__ == '__main__':
    main()
