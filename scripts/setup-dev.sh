#!/bin/bash

echo "🚀 Setting up Creatio Development Environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | sed 's/v//')
REQUIRED_VERSION="18.0.0"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$NODE_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    print_error "Node.js version $NODE_VERSION is not supported. Please upgrade to Node.js 18+."
    exit 1
fi

print_status "Node.js version $NODE_VERSION is compatible"

# Install dependencies
print_status "Installing dependencies..."
npm install

# Set up Git hooks
print_status "Setting up Git hooks..."
npx husky install

# Create pre-commit hook
echo '#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npm run pre-commit' > .husky/pre-commit

chmod +x .husky/pre-commit

# Run initial validation
print_status "Running initial validation..."
npm run validate

# Create src directory structure
print_status "Creating source directory structure..."
mkdir -p src/{types,utils,schemas,modules}
mkdir -p tests/{unit,integration}

# Create initial TypeScript types file
cat > src/types/creatio.d.ts << 'EOF'
/**
 * Creatio TypeScript type definitions
 */

declare namespace Terrasoft {
  export enum DataValueType {
    TEXT = 1,
    INTEGER = 4,
    FLOAT = 5,
    MONEY = 6,
    DATE_TIME = 7,
    DATE = 8,
    TIME = 9,
    LOOKUP = 10,
    ENUM = 11,
    BOOLEAN = 12,
    BLOB = 13,
    IMAGE = 14,
    IMAGELOOKUP = 15,
    COLOR = 16,
    GUID = 17,
    BINARY = 18,
    FILE = 19,
    MAPPING = 20,
    LOCALIZABLE_STRING = 21,
    ENTITY = 22,
    ENTITY_COLLECTION = 23,
    ENTITY_COLUMN_MAPPING_COLLECTION = 24,
    HASH_TEXT = 25,
    SECURE_TEXT = 26,
    LONG_TEXT = 27,
    MEDIUM_TEXT = 28,
    MAX_SIZE_TEXT = 29,
    RICH_TEXT = 30,
    FLOAT1 = 31,
    FLOAT2 = 32,
    FLOAT3 = 33,
    FLOAT4 = 34,
    FLOAT8 = 35,
    METADATA_TEXT = 36
  }

  export enum ViewModelColumnType {
    ENTITY_COLUMN = 0,
    CALCULATED_COLUMN = 1,
    VIRTUAL_COLUMN = 2
  }

  export interface BaseViewModel {
    init(): void;
    callParent(args: any[]): any;
    onEntityInitialized(): void;
    onSaved(): void;
  }

  export interface SchemaColumn {
    dataValueType: DataValueType;
    type: ViewModelColumnType;
    value?: any;
  }

  export interface SchemaAttributes {
    [key: string]: SchemaColumn;
  }
}
EOF

print_status "Created Creatio TypeScript definitions"

# Git commit initial setup
if [ -d ".git" ]; then
    print_status "Committing initial development environment setup..."
    git add .
    git commit -m "feat: setup complete Creatio development environment

- Configure VS Code extensions and settings
- Setup ESLint and Prettier with Creatio-specific rules
- Add TypeScript configuration
- Create project templates and boilerplate code
- Setup Git hooks and pre-commit validation
- Add debugging configurations for client and server
- Initialize development scripts and tools"
fi

echo ""
print_status "🎉 Creatio Development Environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Install recommended VS Code extensions: Ctrl+Shift+P -> 'Extensions: Show Recommended Extensions'"
echo "2. Update .vscode/launch.json with your Creatio instance URL"
echo "3. Start developing with 'npm run dev' for TypeScript watch mode"
echo "4. Run 'npm run lint' to check code quality"
echo "5. Run 'npm run test' to run tests"
echo ""
print_warning "Don't forget to update your Creatio instance URL in the debug configurations!"
