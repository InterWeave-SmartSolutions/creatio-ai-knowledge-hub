#!/bin/bash

# Clio Quick Setup Script
# =======================

set -e  # Exit on any error

echo "🚀 Clio Quick Setup Script"
echo "=========================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Clio is installed
check_clio_installation() {
    print_status "Checking Clio installation..."
    if command -v clio &> /dev/null; then
        CLIO_VERSION=$(clio --version 2>/dev/null || echo "Unknown")
        print_success "Clio is installed (Version: $CLIO_VERSION)"
        return 0
    else
        print_error "Clio is not installed or not in PATH"
        return 1
    fi
}

# Install Clio globally
install_clio() {
    print_status "Installing Clio globally via npm..."
    if npm install -g clio; then
        print_success "Clio installed successfully"
    else
        print_error "Failed to install Clio"
        exit 1
    fi
}

# Setup mkpdev-interweave environment
setup_mkpdev_environment() {
    print_status "Setting up mkpdev-interweave environment..."
    
    # Register the environment without credentials first
    if clio reg-web-app mkpdev-interweave -u https://mkpdev-interweave.creatio.com; then
        print_success "mkpdev-interweave environment registered"
    else
        print_warning "Environment might already be registered"
    fi
    
    print_warning "⚠️  Authentication Setup Required:"
    echo "To complete the setup, you need to add authentication credentials:"
    echo "1. Run: clio reg-web-app mkpdev-interweave -u https://mkpdev-interweave.creatio.com -l YOUR_USERNAME -p YOUR_PASSWORD --checkLogin"
    echo "2. Or set up OAuth if using modern authentication"
    echo ""
}

# Setup local development environment
setup_local_environment() {
    print_status "Setting up local development environment..."
    
    read -p "Do you have a local Creatio instance? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter local URL (default: http://localhost): " LOCAL_URL
        LOCAL_URL=${LOCAL_URL:-http://localhost}
        
        read -p "Enter username (default: Supervisor): " LOCAL_USER
        LOCAL_USER=${LOCAL_USER:-Supervisor}
        
        read -p "Enter password (default: Supervisor): " LOCAL_PASS
        LOCAL_PASS=${LOCAL_PASS:-Supervisor}
        
        if clio reg-web-app local -u "$LOCAL_URL" -l "$LOCAL_USER" -p "$LOCAL_PASS" --checkLogin; then
            print_success "Local environment registered and tested"
        else
            print_error "Failed to register local environment"
        fi
    else
        print_status "Skipping local environment setup"
    fi
}

# Create directory structure
create_directory_structure() {
    print_status "Creating directory structure..."
    
    # Create directories
    mkdir -p ~/creatio-projects/{packages,workspaces,scripts,sql-scripts,manifests}
    
    # Create .gitignore for Creatio projects
    cat > ~/creatio-projects/.gitignore << 'EOF'
# Creatio specific
*.log
*.tmp
bin/
obj/
Packages/
Terrasoft.Configuration/
Terrasoft.Core/
Terrasoft.Web.Common/

# Node modules
node_modules/

# VS Code
.vscode/

# IDE
.idea/
*.suo
*.user

# OS
.DS_Store
Thumbs.db
EOF

    # Create README
    cat > ~/creatio-projects/README.md << 'EOF'
# Creatio Projects

This directory contains your Creatio development projects.

## Structure
- `packages/` - Individual Creatio packages
- `workspaces/` - Clio workspaces
- `scripts/` - Custom scripts and automation
- `sql-scripts/` - SQL scripts for database operations
- `manifests/` - Deployment manifests

## Getting Started
1. Source the Clio templates: `source /path/to/clio-templates.sh`
2. Use the helper functions for common operations
3. Check the CLIO_WORKFLOWS.md for detailed documentation

## Quick Commands
- `list_environments` - Show all registered environments
- `create_package MyPackage` - Create a new package
- `push_package MyPackage env-name` - Deploy package to environment
EOF

    print_success "Directory structure created at ~/creatio-projects"
}

# Create useful aliases
create_aliases() {
    print_status "Creating useful aliases..."
    
    ALIAS_FILE="$HOME/.clio_aliases"
    
    cat > "$ALIAS_FILE" << 'EOF'
# Clio Aliases
alias clio-envs='clio show-web-app-list'
alias clio-ping='clio ping-app'
alias clio-packages='clio get-pkg-list'
alias clio-dev='clio set-dev-mode'
alias clio-open='clio open-web-app'
alias clio-restart='clio restart-web-app'
alias clio-push='clio push-pkg'
alias clio-pull='clio pull-pkg'
alias clio-create='clio new-pkg'
alias clio-workspace='clio create-workspace'
alias clio-sql='clio execute-sql-script'

# Quick environment switching
alias clio-local='clio reg-web-app local -a'
alias clio-mkp='clio reg-web-app mkpdev-interweave -a'

# Common operations
alias clio-status='clio ping-app && clio get-pkg-list'
EOF

    # Add to shell profile if not already present
    for profile in ~/.bashrc ~/.zshrc ~/.profile; do
        if [[ -f "$profile" ]]; then
            if ! grep -q "source.*clio_aliases" "$profile"; then
                echo "" >> "$profile"
                echo "# Clio aliases" >> "$profile"
                echo "if [[ -f ~/.clio_aliases ]]; then" >> "$profile"
                echo "    source ~/.clio_aliases" >> "$profile"
                echo "fi" >> "$profile"
                print_success "Added aliases to $profile"
            fi
            break
        fi
    done
    
    print_success "Aliases created at $ALIAS_FILE"
}

# Main setup function
main() {
    echo "This script will help you set up Clio for Creatio development."
    echo ""
    
    # Check if Clio is already installed
    if ! check_clio_installation; then
        read -p "Would you like to install Clio now? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            install_clio
        else
            print_error "Clio is required for this setup. Exiting."
            exit 1
        fi
    fi
    
    # Setup environments
    print_status "Setting up environments..."
    setup_mkpdev_environment
    setup_local_environment
    
    # Create directory structure
    read -p "Create recommended directory structure at ~/creatio-projects? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        create_directory_structure
    fi
    
    # Create aliases
    read -p "Create useful Clio aliases? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        create_aliases
    fi
    
    # Final instructions
    echo ""
    print_success "🎉 Clio setup completed!"
    echo ""
    echo "Next steps:"
    echo "1. Complete authentication setup for mkpdev-interweave:"
    echo "   clio reg-web-app mkpdev-interweave -u https://mkpdev-interweave.creatio.com -l YOUR_USERNAME -p YOUR_PASSWORD --checkLogin"
    echo ""
    echo "2. Source the templates file:"
    echo "   source $(dirname "${BASH_SOURCE[0]}")/clio-templates.sh"
    echo ""
    echo "3. Test your setup:"
    echo "   clio show-web-app-list"
    echo "   clio ping-app -e mkpdev-interweave"
    echo ""
    echo "4. Check the documentation:"
    echo "   cat $(dirname "${BASH_SOURCE[0]}")/CLIO_WORKFLOWS.md"
    echo ""
    echo "5. Restart your terminal or source your profile to load aliases"
    echo ""
    print_warning "Remember to keep your credentials secure!"
}

# Run main function
main "$@"
