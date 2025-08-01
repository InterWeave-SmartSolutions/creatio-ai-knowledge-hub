#!/bin/bash

# Creatio Installation Helper Script
# This script helps with the Creatio platform installation process

echo "==================================="
echo "Creatio Platform Installation Helper"
echo "==================================="
echo ""

# Check if installer file is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <creatio_installer_file>"
    echo ""
    echo "Please download the Creatio installer from:"
    echo "1. Log in to https://www.creatio.com with your credentials"
    echo "2. Navigate to the Downloads section"
    echo "3. Download the Linux installer (usually a .tar.gz or .zip file)"
    echo "4. Run this script with the downloaded file as an argument"
    exit 1
fi

INSTALLER_FILE="$1"

# Check if file exists
if [ ! -f "$INSTALLER_FILE" ]; then
    echo "Error: File '$INSTALLER_FILE' not found!"
    exit 1
fi

# Create installation directory
INSTALL_DIR="$HOME/creatio"
echo "Creating installation directory at: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

# Detect file type and extract
echo "Detecting installer file type..."
if [[ "$INSTALLER_FILE" == *.tar.gz ]]; then
    echo "Extracting tar.gz archive..."
    tar -xzf "$INSTALLER_FILE" -C "$INSTALL_DIR"
elif [[ "$INSTALLER_FILE" == *.zip ]]; then
    echo "Extracting zip archive..."
    unzip -q "$INSTALLER_FILE" -d "$INSTALL_DIR"
else
    echo "Error: Unsupported file type. Expected .tar.gz or .zip"
    exit 1
fi

echo ""
echo "Extraction complete. Checking installation contents..."
cd "$INSTALL_DIR"

# Look for common Creatio installation files
if [ -f "install.sh" ]; then
    echo "Found installation script: install.sh"
    echo ""
    echo "To continue installation:"
    echo "1. cd $INSTALL_DIR"
    echo "2. sudo ./install.sh"
elif [ -f "setup.sh" ]; then
    echo "Found setup script: setup.sh"
    echo ""
    echo "To continue installation:"
    echo "1. cd $INSTALL_DIR"
    echo "2. sudo ./setup.sh"
elif [ -d "bin" ] && [ -f "bin/creatio" ]; then
    echo "Found Creatio binaries in bin directory"
    echo ""
    echo "To continue installation:"
    echo "1. cd $INSTALL_DIR"
    echo "2. Configure according to documentation"
else
    echo "Installation files found in: $INSTALL_DIR"
    echo "Please check the documentation for installation instructions."
    ls -la
fi

echo ""
echo "==================================="
echo "Pre-installation checklist:"
echo "==================================="
echo "✓ Ensure you have at least 4GB of RAM"
echo "✓ Ensure you have at least 20GB of free disk space"
echo "✓ PostgreSQL or MS SQL Server should be installed (for production)"
echo "✓ .NET Core runtime should be installed"
echo ""

# Check for .NET Core
if command -v dotnet &> /dev/null; then
    echo "✓ .NET Core detected: $(dotnet --version)"
else
    echo "⚠ .NET Core not detected. You may need to install it:"
    echo "  wget https://dot.net/v1/dotnet-install.sh"
    echo "  chmod +x dotnet-install.sh"
    echo "  ./dotnet-install.sh"
fi

echo ""
echo "Next steps:"
echo "1. Navigate to the installation directory"
echo "2. Run the installation script with sudo privileges"
echo "3. Select 'Development/Trial' license option when prompted"
echo "4. Configure installation paths as needed"
echo "5. Wait for the installation to complete (typically 15-20 minutes)"
