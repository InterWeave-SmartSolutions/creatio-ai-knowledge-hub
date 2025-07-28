#!/usr/bin/env node

/**
 * Dependency Tracking System
 * Tracks package dependencies, analyzes usage, and provides security scanning
 */

const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');

class DependencyTracker {
    constructor(configPath = '../package-registry.json') {
        this.configPath = configPath;
        this.config = null;
        this.trackingFile = path.join(__dirname, '../dependency-tracking.json');
        this.dependencies = {};
    }

    async initialize() {
        try {
            const configData = await fs.readFile(path.join(__dirname, this.configPath), 'utf8');
            this.config = JSON.parse(configData);
            
            // Load existing tracking data
            await this.loadTrackingData();
            
            console.log('Dependency tracker initialized successfully');
        } catch (error) {
            throw new Error(`Failed to initialize dependency tracker: ${error.message}`);
        }
    }

    async loadTrackingData() {
        try {
            if (await this.fileExists(this.trackingFile)) {
                const trackingData = await fs.readFile(this.trackingFile, 'utf8');
                const data = JSON.parse(trackingData);
                this.dependencies = data.dependencies || {};
            }
        } catch (error) {
            console.log('Starting with empty dependency tracking data');
            this.dependencies = {};
        }
    }

    async saveTrackingData() {
        const trackingData = {
            metadata: {
                lastUpdated: new Date().toISOString(),
                version: '1.0.0',
                totalDependencies: Object.keys(this.dependencies).length
            },
            dependencies: this.dependencies,
            analysis: await this.generateAnalysis()
        };

        await fs.writeFile(this.trackingFile, JSON.stringify(trackingData, null, 2));
    }

    /**
     * Track a new dependency
     */
    async trackDependency(packageName, version, registry, downloadPath, metadata = {}) {
        if (!this.config.dependency_tracking.enabled) {
            return;
        }

        const dependencyId = `${packageName}@${version}`;
        
        this.dependencies[dependencyId] = {
            name: packageName,
            version,
            registry,
            downloadPath,
            downloadDate: new Date().toISOString(),
            lastUsed: new Date().toISOString(),
            usageCount: (this.dependencies[dependencyId]?.usageCount || 0) + 1,
            size: await this.getPackageSize(downloadPath),
            checksum: await this.generateChecksum(downloadPath),
            metadata: {
                ...metadata,
                tracked: true
            }
        };

        await this.saveTrackingData();
        console.log(`Tracked dependency: ${dependencyId}`);
    }

    /**
     * Update usage statistics for a dependency
     */
    async updateUsage(packageName, version) {
        const dependencyId = `${packageName}@${version}`;
        
        if (this.dependencies[dependencyId]) {
            this.dependencies[dependencyId].lastUsed = new Date().toISOString();
            this.dependencies[dependencyId].usageCount++;
            await this.saveTrackingData();
        }
    }

    /**
     * Analyze dependency tree and detect conflicts
     */
    async analyzeDependencies() {
        const analysis = {
            totalDependencies: Object.keys(this.dependencies).length,
            byRegistry: {},
            byVersion: {},
            conflicts: [],
            unused: [],
            outdated: [],
            security: {
                vulnerabilities: [],
                licenses: {}
            }
        };

        // Group by registry
        for (const [id, dep] of Object.entries(this.dependencies)) {
            if (!analysis.byRegistry[dep.registry]) {
                analysis.byRegistry[dep.registry] = 0;
            }
            analysis.byRegistry[dep.registry]++;

            // Check for version conflicts
            const baseName = dep.name;
            const conflicts = Object.values(this.dependencies).filter(
                d => d.name === baseName && d.version !== dep.version
            );
            
            if (conflicts.length > 0) {
                analysis.conflicts.push({
                    package: baseName,
                    versions: [dep.version, ...conflicts.map(c => c.version)]
                });
            }

            // Check for unused packages (not accessed in 30 days)
            const lastUsed = new Date(dep.lastUsed);
            const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);
            
            if (lastUsed < thirtyDaysAgo) {
                analysis.unused.push({
                    package: id,
                    lastUsed: dep.lastUsed,
                    daysSinceUsed: Math.floor((Date.now() - lastUsed.getTime()) / (24 * 60 * 60 * 1000))
                });
            }
        }

        return analysis;
    }

    /**
     * Generate security report
     */
    async generateSecurityReport() {
        if (!this.config.dependency_tracking.security_scanning) {
            return { enabled: false };
        }

        const report = {
            enabled: true,
            scannedAt: new Date().toISOString(),
            vulnerabilities: [],
            licenses: {},
            checksumVerification: []
        };

        for (const [id, dep] of Object.entries(this.dependencies)) {
            // Verify checksums
            try {
                const currentChecksum = await this.generateChecksum(dep.downloadPath);
                if (currentChecksum !== dep.checksum) {
                    report.checksumVerification.push({
                        package: id,
                        status: 'MISMATCH',
                        expected: dep.checksum,
                        actual: currentChecksum
                    });
                } else {
                    report.checksumVerification.push({
                        package: id,
                        status: 'VERIFIED'
                    });
                }
            } catch (error) {
                report.checksumVerification.push({
                    package: id,
                    status: 'ERROR',
                    error: error.message
                });
            }

            // Mock vulnerability check (in real implementation, this would query security databases)
            if (Math.random() < 0.1) { // 10% chance of mock vulnerability
                report.vulnerabilities.push({
                    package: id,
                    severity: ['low', 'medium', 'high'][Math.floor(Math.random() * 3)],
                    description: `Mock vulnerability in ${dep.name}`,
                    cve: `CVE-2024-${Math.floor(Math.random() * 10000)}`
                });
            }
        }

        return report;
    }

    /**
     * Clean up unused dependencies
     */
    async cleanupUnused(daysThreshold = 30) {
        const cutoffDate = new Date(Date.now() - daysThreshold * 24 * 60 * 60 * 1000);
        let cleaned = 0;

        for (const [id, dep] of Object.entries(this.dependencies)) {
            const lastUsed = new Date(dep.lastUsed);
            
            if (lastUsed < cutoffDate) {
                try {
                    // Remove the package file
                    if (await this.fileExists(dep.downloadPath)) {
                        await fs.unlink(dep.downloadPath);
                    }
                    
                    // Remove from tracking
                    delete this.dependencies[id];
                    cleaned++;
                    
                    console.log(`Cleaned up unused dependency: ${id}`);
                } catch (error) {
                    console.error(`Failed to clean up ${id}: ${error.message}`);
                }
            }
        }

        if (cleaned > 0) {
            await this.saveTrackingData();
        }

        console.log(`Cleaned up ${cleaned} unused dependencies`);
        return cleaned;
    }

    /**
     * Generate comprehensive analysis report
     */
    async generateAnalysis() {
        const analysis = await this.analyzeDependencies();
        const security = await this.generateSecurityReport();

        return {
            ...analysis,
            security,
            recommendations: this.generateRecommendations(analysis, security)
        };
    }

    /**
     * Generate recommendations based on analysis
     */
    generateRecommendations(analysis, security) {
        const recommendations = [];

        // Conflict recommendations
        if (analysis.conflicts.length > 0) {
            recommendations.push({
                type: 'conflict',
                priority: 'high',
                message: `${analysis.conflicts.length} version conflicts detected`,
                action: 'Review and resolve version conflicts'
            });
        }

        // Unused dependency recommendations
        if (analysis.unused.length > 0) {
            recommendations.push({
                type: 'cleanup',
                priority: 'medium',
                message: `${analysis.unused.length} unused dependencies found`,
                action: 'Consider removing unused dependencies'
            });
        }

        // Security recommendations
        if (security.vulnerabilities && security.vulnerabilities.length > 0) {
            const highSeverity = security.vulnerabilities.filter(v => v.severity === 'high');
            if (highSeverity.length > 0) {
                recommendations.push({
                    type: 'security',
                    priority: 'critical',
                    message: `${highSeverity.length} high-severity vulnerabilities found`,
                    action: 'Update vulnerable packages immediately'
                });
            }
        }

        return recommendations;
    }

    /**
     * Utility methods
     */
    async fileExists(filePath) {
        try {
            await fs.access(filePath);
            return true;
        } catch {
            return false;
        }
    }

    async getPackageSize(filePath) {
        try {
            if (await this.fileExists(filePath)) {
                const stats = await fs.stat(filePath);
                return stats.size;
            }
        } catch (error) {
            return 0;
        }
        return 0;
    }

    async generateChecksum(filePath) {
        try {
            if (await this.fileExists(filePath)) {
                const fileBuffer = await fs.readFile(filePath);
                return crypto.createHash('sha256').update(fileBuffer).digest('hex');
            }
        } catch (error) {
            return null;
        }
        return null;
    }

    /**
     * Export dependency graph in various formats
     */
    async exportDependencyGraph(format = 'json') {
        const graph = {
            nodes: Object.entries(this.dependencies).map(([id, dep]) => ({
                id,
                name: dep.name,
                version: dep.version,
                registry: dep.registry,
                size: dep.size,
                lastUsed: dep.lastUsed
            })),
            edges: [], // Would be populated with actual dependency relationships
            metadata: {
                generatedAt: new Date().toISOString(),
                format,
                totalNodes: Object.keys(this.dependencies).length
            }
        };

        const outputPath = path.join(__dirname, `../dependency-graph.${format}`);
        
        if (format === 'json') {
            await fs.writeFile(outputPath, JSON.stringify(graph, null, 2));
        } else if (format === 'dot') {
            // Generate DOT format for Graphviz
            let dotContent = 'digraph dependencies {\n';
            graph.nodes.forEach(node => {
                dotContent += `  "${node.id}" [label="${node.name}\\n${node.version}"];\n`;
            });
            dotContent += '}\n';
            await fs.writeFile(outputPath, dotContent);
        }

        console.log(`Dependency graph exported to: ${outputPath}`);
        return outputPath;
    }
}

// CLI interface
if (require.main === module) {
    const tracker = new DependencyTracker();
    
    async function main() {
        const args = process.argv.slice(2);
        
        if (args.length === 0) {
            console.log('Usage: node dependency-tracker.js <command> [options]');
            console.log('Commands:');
            console.log('  analyze                    - Analyze dependencies');
            console.log('  security                   - Generate security report');
            console.log('  cleanup [days]             - Clean up unused dependencies');
            console.log('  export [format]            - Export dependency graph');
            console.log('  track <name> <version>     - Track a dependency');
            return;
        }

        await tracker.initialize();

        const command = args[0];
        
        switch (command) {
            case 'analyze':
                const analysis = await tracker.generateAnalysis();
                console.log('Dependency Analysis:', JSON.stringify(analysis, null, 2));
                break;
                
            case 'security':
                const security = await tracker.generateSecurityReport();
                console.log('Security Report:', JSON.stringify(security, null, 2));
                break;
                
            case 'cleanup':
                const days = parseInt(args[1]) || 30;
                await tracker.cleanupUnused(days);
                break;
                
            case 'export':
                const format = args[1] || 'json';
                await tracker.exportDependencyGraph(format);
                break;
                
            case 'track':
                if (args.length < 3) {
                    console.error('Package name and version required');
                    return;
                }
                await tracker.trackDependency(args[1], args[2], 'manual', '');
                break;
                
            default:
                console.error(`Unknown command: ${command}`);
        }
    }

    main().catch(console.error);
}

module.exports = DependencyTracker;
