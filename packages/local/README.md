# Local Package Repository

This directory contains locally developed packages and modules for the Creatio AI Knowledge Hub.

## Structure

```
local/
├── core/               # Core system packages
├── plugins/            # Plugin packages
├── utilities/          # Utility packages
├── themes/             # UI themes and styling
├── templates/          # Template packages
└── integrations/       # Integration packages
```

## Package Structure

Each package should follow this structure:
```
package-name/
├── package.json        # Package metadata
├── src/               # Source code
├── dist/              # Built/compiled code
├── tests/             # Test files
├── docs/              # Documentation
└── README.md          # Package documentation
```

## Development Guidelines

1. All packages must include proper version numbers
2. Dependencies must be explicitly declared
3. Include comprehensive tests
4. Document all public APIs
5. Follow semantic versioning (semver)
