#!/usr/bin/env python3

"""
Python Package Download Automation System
Handles downloading Python packages from PyPI and other registries with caching and dependency tracking
"""

import os
import sys
import json
import hashlib
import shutil
import requests
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class PythonPackageDownloader:
    def __init__(self, config_path: str = "../package-registry.json"):
        self.config_path = config_path
        self.config = None
        self.cache_dir = Path(__dirname__).parent / "cache"
        self.requirements_cache = {}
        
    async def initialize(self):
        """Initialize the package downloader"""
        try:
            config_file = Path(__file__).parent / self.config_path
            with open(config_file, 'r') as f:
                self.config = json.load(f)
                
            # Ensure cache directory exists
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            
            print("Python package downloader initialized successfully")
        except Exception as e:
            raise Exception(f"Failed to initialize package downloader: {str(e)}")
    
    def download_package(self, package_name: str, version: str = "latest", 
                        registry: str = "pypi") -> str:
        """Download a Python package from registry"""
        try:
            registry_config = self.config["registries"][registry]
            if not registry_config or not registry_config["enabled"]:
                raise Exception(f"Registry {registry} is not available or disabled")
                
            print(f"Downloading {package_name}=={version} from {registry}...")
            
            # Check cache first
            cache_key = self._generate_cache_key(package_name, version, registry)
            cached_path = self._check_cache(cache_key, registry_config.get("cache_ttl"))
            
            if cached_path:
                print(f"Using cached version of {package_name}=={version}")
                return cached_path
                
            # Download using pip
            download_path = self._download_with_pip(package_name, version)
            
            # Cache the downloaded package
            if registry_config.get("cache"):
                self._cache_package(cache_key, download_path)
                
            # Track dependency
            self._track_dependency(package_name, version, registry, download_path)
            
            print(f"Successfully downloaded {package_name}=={version}")
            return download_path
            
        except Exception as e:
            print(f"Failed to download {package_name}=={version}: {str(e)}")
            raise e
    
    def _download_with_pip(self, package_name: str, version: str) -> str:
        """Download package using pip"""
        download_dir = Path(__file__).parent.parent / "remote" / "python"
        download_dir.mkdir(parents=True, exist_ok=True)
        
        if version == "latest":
            package_spec = package_name
        else:
            package_spec = f"{package_name}=={version}"
            
        # Use pip download to get the package
        cmd = [
            sys.executable, "-m", "pip", "download",
            "--dest", str(download_dir),
            "--no-deps",  # Don't download dependencies automatically
            package_spec
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"pip download failed: {result.stderr}")
            
        # Find the downloaded file
        downloaded_files = list(download_dir.glob(f"{package_name.replace('-', '_')}*"))
        if not downloaded_files:
            raise Exception(f"Downloaded package not found in {download_dir}")
            
        return str(downloaded_files[0])
    
    def _generate_cache_key(self, package_name: str, version: str, registry: str) -> str:
        """Generate cache key for package"""
        input_str = f"{package_name}-{version}-{registry}"
        return hashlib.sha256(input_str.encode()).hexdigest()
    
    def _check_cache(self, cache_key: str, ttl: Optional[int]) -> Optional[str]:
        """Check if package exists in cache and is not expired"""
        try:
            cache_path = self.cache_dir / cache_key
            if not cache_path.exists():
                return None
                
            if ttl:
                mtime = datetime.fromtimestamp(cache_path.stat().st_mtime)
                if datetime.now() - mtime > timedelta(seconds=ttl):
                    return None  # Expired
                    
            return str(cache_path)
        except:
            return None
    
    def _cache_package(self, cache_key: str, source_path: str):
        """Cache downloaded package"""
        cache_path = self.cache_dir / cache_key
        shutil.copy2(source_path, cache_path)
    
    def _track_dependency(self, package_name: str, version: str, 
                         registry: str, download_path: str):
        """Track package dependency"""
        if not self.config["dependency_tracking"]["enabled"]:
            return
            
        tracking_file = Path(__file__).parent.parent / "dependency-tracking.json"
        tracking = {}
        
        try:
            if tracking_file.exists():
                with open(tracking_file, 'r') as f:
                    tracking = json.load(f)
        except:
            pass
            
        if "dependencies" not in tracking:
            tracking["dependencies"] = {}
            
        tracking["dependencies"][package_name] = {
            "version": version,
            "registry": registry,
            "downloadPath": download_path,
            "downloadDate": datetime.now().isoformat(),
            "lastUsed": datetime.now().isoformat(),
            "language": "python"
        }
        
        with open(tracking_file, 'w') as f:
            json.dump(tracking, f, indent=2)
    
    def download_batch(self, packages: List[Dict]) -> List[Dict]:
        """Download multiple packages"""
        results = []
        
        for pkg in packages:
            try:
                result = self.download_package(
                    pkg["name"],
                    pkg.get("version", "latest"),
                    pkg.get("registry", "pypi")
                )
                results.append({**pkg, "success": True, "path": result})
            except Exception as e:
                results.append({**pkg, "success": False, "error": str(e)})
                
        return results
    
    def install_from_requirements(self, requirements_file: str) -> Dict:
        """Install packages from requirements.txt file"""
        try:
            print(f"Installing packages from {requirements_file}")
            
            cmd = [
                sys.executable, "-m", "pip", "install",
                "-r", requirements_file,
                "--cache-dir", str(self.cache_dir)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_requirements_lock(self, output_file: str = "requirements.lock"):
        """Generate locked requirements file with exact versions"""
        try:
            cmd = [sys.executable, "-m", "pip", "freeze"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                output_path = Path(__file__).parent.parent / output_file
                with open(output_path, 'w') as f:
                    f.write(result.stdout)
                print(f"Generated locked requirements file: {output_path}")
                return str(output_path)
            else:
                raise Exception(f"pip freeze failed: {result.stderr}")
                
        except Exception as e:
            print(f"Failed to generate requirements lock: {str(e)}")
            raise e
    
    def clean_cache(self):
        """Clean expired cache entries"""
        try:
            cleaned = 0
            cutoff_time = datetime.now() - timedelta(days=7)
            
            for cache_file in self.cache_dir.iterdir():
                if cache_file.is_file():
                    mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
                    if mtime < cutoff_time:
                        cache_file.unlink()
                        cleaned += 1
                        
            print(f"Cleaned {cleaned} expired cache entries")
        except Exception as e:
            print(f"Failed to clean cache: {str(e)}")

def main():
    """CLI interface"""
    import asyncio
    
    if len(sys.argv) < 2:
        print("Usage: python download-packages.py <command> [options]")
        print("Commands:")
        print("  download <package> [version] [registry] - Download a single package")
        print("  batch <file>                           - Download packages from JSON file")
        print("  install <requirements_file>            - Install from requirements file")
        print("  freeze [output_file]                   - Generate locked requirements")
        print("  clean                                  - Clean expired cache entries")
        return
        
    downloader = PythonPackageDownloader()
    asyncio.run(downloader.initialize())
    
    command = sys.argv[1]
    
    if command == "download":
        if len(sys.argv) < 3:
            print("Package name required")
            return
        downloader.download_package(
            sys.argv[2],
            sys.argv[3] if len(sys.argv) > 3 else "latest",
            sys.argv[4] if len(sys.argv) > 4 else "pypi"
        )
        
    elif command == "batch":
        if len(sys.argv) < 3:
            print("Batch file required")
            return
        with open(sys.argv[2], 'r') as f:
            packages = json.load(f)
        results = downloader.download_batch(packages)
        print("Batch download results:", json.dumps(results, indent=2))
        
    elif command == "install":
        if len(sys.argv) < 3:
            print("Requirements file required")
            return
        result = downloader.install_from_requirements(sys.argv[2])
        if result["success"]:
            print("Installation completed successfully")
        else:
            print(f"Installation failed: {result.get('error', result.get('stderr'))}")
            
    elif command == "freeze":
        output_file = sys.argv[2] if len(sys.argv) > 2 else "requirements.lock"
        downloader.generate_requirements_lock(output_file)
        
    elif command == "clean":
        downloader.clean_cache()
        
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
