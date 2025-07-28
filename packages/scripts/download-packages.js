#!/usr/bin/env node

/**
 * Package Download Automation System
 * Handles downloading packages from remote registries with caching and dependency tracking
 */

const fs = require('fs').promises;
const path = require('path');
const https = require('https');
const crypto = require('crypto');

class PackageDownloader {
    constructor(configPath = '../package-registry.json') {
        this.configPath = configPath;
        this.config = null;
        this.cacheDir = path.join(__dirname, '../cache');
        this.downloadQueue = [];
    }

    async initialize() {
        try {
            const configData = await fs.readFile(path.join(__dirname, this.configPath), 'utf8');
            this.config = JSON.parse(configData);
            
            // Ensure cache directory exists
            await fs.mkdir(this.cacheDir, { recursive: true });
            
            console.log('Package downloader initialized successfully');
        } catch (error) {
            throw new Error(`Failed to initialize package downloader: ${error.message}`);
        }
    }

    /**
     * Download package from remote registry
     */
    async downloadPackage(packageName, version = 'latest', registry = 'npm') {
        try {
            const registryConfig = this.config.registries[registry];
            if (!registryConfig || !registryConfig.enabled) {
                throw new Error(`Registry ${registry} is not available or disabled`);
            }

            console.log(`Downloading ${packageName}@${version} from ${registry}...`);

            const packageInfo = await this.getPackageInfo(packageName, version, registryConfig);
            const downloadUrl = this.buildDownloadUrl(packageInfo, registryConfig);
            
            // Check cache first
            const cacheKey = this.generateCacheKey(packageName, version, registry);
            const cachedPath = await this.checkCache(cacheKey, registryConfig.cache_ttl);
            
            if (cachedPath) {
                console.log(`Using cached version of ${packageName}@${version}`);
                return cachedPath;
            }

            // Download package
            const downloadPath = await this.performDownload(downloadUrl, packageName, version);
            
            // Cache the downloaded package
            if (registryConfig.cache) {
                await this.cachePackage(cacheKey, downloadPath);
            }

            // Track dependency
            await this.trackDependency(packageName, version, registry, downloadPath);

            console.log(`Successfully downloaded ${packageName}@${version}`);
            return downloadPath;

        } catch (error) {
            console.error(`Failed to download ${packageName}@${version}: ${error.message}`);
            throw error;
        }
    }

    /**
     * Get package information from registry
     */
    async getPackageInfo(packageName, version, registryConfig) {
        // This would implement registry-specific API calls
        // For now, return mock data
        return {
            name: packageName,
            version: version,
            downloadUrl: `${registryConfig.url}${packageName}/-/${packageName}-${version}.tgz`,
            dependencies: {},
            devDependencies: {}
        };
    }

    /**
     * Build download URL based on registry type
     */
    buildDownloadUrl(packageInfo, registryConfig) {
        if (registryConfig.type === 'npm') {
            return packageInfo.downloadUrl;
        } else if (registryConfig.type === 'pypi') {
            return `${registryConfig.url}${packageInfo.name}/`;
        }
        return packageInfo.downloadUrl;
    }

    /**
     * Generate cache key for package
     */
    generateCacheKey(packageName, version, registry) {
        const input = `${packageName}-${version}-${registry}`;
        return crypto.createHash('sha256').update(input).digest('hex');
    }

    /**
     * Check if package exists in cache and is not expired
     */
    async checkCache(cacheKey, ttl) {
        try {
            const cachePath = path.join(this.cacheDir, cacheKey);
            const stats = await fs.stat(cachePath);
            
            if (ttl && Date.now() - stats.mtime.getTime() > ttl * 1000) {
                return null; // Expired
            }
            
            return cachePath;
        } catch (error) {
            return null; // Not in cache
        }
    }

    /**
     * Perform actual download
     */
    async performDownload(url, packageName, version) {
        return new Promise((resolve, reject) => {
            const fileName = `${packageName}-${version}.tgz`;
            const downloadPath = path.join(__dirname, '../remote', fileName);
            
            // Ensure remote directory exists
            fs.mkdir(path.dirname(downloadPath), { recursive: true }).then(() => {
                const file = require('fs').createWriteStream(downloadPath);
                
                https.get(url, (response) => {
                    if (response.statusCode !== 200) {
                        reject(new Error(`HTTP ${response.statusCode}: ${response.statusMessage}`));
                        return;
                    }
                    
                    response.pipe(file);
                    
                    file.on('finish', () => {
                        file.close();
                        resolve(downloadPath);
                    });
                    
                    file.on('error', (error) => {
                        fs.unlink(downloadPath);
                        reject(error);
                    });
                }).on('error', reject);
            });
        });
    }

    /**
     * Cache downloaded package
     */
    async cachePackage(cacheKey, sourcePath) {
        const cachePath = path.join(this.cacheDir, cacheKey);
        await fs.copyFile(sourcePath, cachePath);
    }

    /**
     * Track package dependency
     */
    async trackDependency(packageName, version, registry, downloadPath) {
        if (!this.config.dependency_tracking.enabled) {
            return;
        }

        const trackingFile = path.join(__dirname, '../dependency-tracking.json');
        let tracking = {};

        try {
            const trackingData = await fs.readFile(trackingFile, 'utf8');
            tracking = JSON.parse(trackingData);
        } catch (error) {
            // File doesn't exist, start fresh
        }

        if (!tracking.dependencies) {
            tracking.dependencies = {};
        }

        tracking.dependencies[packageName] = {
            version,
            registry,
            downloadPath,
            downloadDate: new Date().toISOString(),
            lastUsed: new Date().toISOString()
        };

        await fs.writeFile(trackingFile, JSON.stringify(tracking, null, 2));
    }

    /**
     * Batch download packages
     */
    async downloadBatch(packages) {
        const results = [];
        
        for (const pkg of packages) {
            try {
                const result = await this.downloadPackage(
                    pkg.name, 
                    pkg.version || 'latest', 
                    pkg.registry || 'npm'
                );
                results.push({ ...pkg, success: true, path: result });
            } catch (error) {
                results.push({ ...pkg, success: false, error: error.message });
            }
        }
        
        return results;
    }

    /**
     * Clean expired cache entries
     */
    async cleanCache() {
        try {
            const files = await fs.readdir(this.cacheDir);
            let cleaned = 0;

            for (const file of files) {
                const filePath = path.join(this.cacheDir, file);
                const stats = await fs.stat(filePath);
                
                // Remove files older than 7 days
                if (Date.now() - stats.mtime.getTime() > 7 * 24 * 60 * 60 * 1000) {
                    await fs.unlink(filePath);
                    cleaned++;
                }
            }

            console.log(`Cleaned ${cleaned} expired cache entries`);
        } catch (error) {
            console.error(`Failed to clean cache: ${error.message}`);
        }
    }
}

// CLI interface
if (require.main === module) {
    const downloader = new PackageDownloader();
    
    async function main() {
        const args = process.argv.slice(2);
        
        if (args.length === 0) {
            console.log('Usage: node download-packages.js <command> [options]');
            console.log('Commands:');
            console.log('  download <package> [version] [registry] - Download a single package');
            console.log('  batch <file>                           - Download packages from JSON file');
            console.log('  clean                                  - Clean expired cache entries');
            return;
        }

        await downloader.initialize();

        const command = args[0];
        
        switch (command) {
            case 'download':
                if (args.length < 2) {
                    console.error('Package name required');
                    return;
                }
                await downloader.downloadPackage(args[1], args[2], args[3]);
                break;
                
            case 'batch':
                if (args.length < 2) {
                    console.error('Batch file required');
                    return;
                }
                const batchFile = await fs.readFile(args[1], 'utf8');
                const packages = JSON.parse(batchFile);
                const results = await downloader.downloadBatch(packages);
                console.log('Batch download results:', results);
                break;
                
            case 'clean':
                await downloader.cleanCache();
                break;
                
            default:
                console.error(`Unknown command: ${command}`);
        }
    }

    main().catch(console.error);
}

module.exports = PackageDownloader;
