#!/bin/bash

# Clio Command Templates and Scripts
# =================================

# Environment Management
# ----------------------

# List all registered environments
list_environments() {
    echo "📋 Listing all registered environments:"
    clio show-web-app-list
}

# Set active environment
set_active_env() {
    local env_name="$1"
    if [ -z "$env_name" ]; then
        echo "❌ Usage: set_active_env <environment_name>"
        return 1
    fi
    echo "🔄 Setting active environment to: $env_name"
    clio reg-web-app "$env_name" -a
}

# Test connection to environment
test_connection() {
    local env_name="$1"
    if [ -z "$env_name" ]; then
        echo "❌ Usage: test_connection <environment_name>"
        return 1
    fi
    echo "🔍 Testing connection to: $env_name"
    clio ping-app -e "$env_name"
}

# Package Management
# ------------------

# Create new package
create_package() {
    local pkg_name="$1"
    if [ -z "$pkg_name" ]; then
        echo "❌ Usage: create_package <package_name>"
        return 1
    fi
    echo "📦 Creating new package: $pkg_name"
    clio new-pkg "$pkg_name"
}

# Push package to environment
push_package() {
    local pkg_name="$1"
    local env_name="$2"
    if [ -z "$pkg_name" ] || [ -z "$env_name" ]; then
        echo "❌ Usage: push_package <package_name> <environment_name>"
        return 1
    fi
    echo "⬆️ Pushing package $pkg_name to $env_name"
    clio push-pkg "$pkg_name" -e "$env_name"
}

# Pull package from environment
pull_package() {
    local pkg_name="$1"
    local env_name="$2"
    if [ -z "$pkg_name" ] || [ -z "$env_name" ]; then
        echo "❌ Usage: pull_package <package_name> <environment_name>"
        return 1
    fi
    echo "⬇️ Pulling package $pkg_name from $env_name"
    clio pull-pkg "$pkg_name" -e "$env_name"
}

# List packages in environment
list_packages() {
    local env_name="$1"
    if [ -z "$env_name" ]; then
        echo "❌ Usage: list_packages <environment_name>"
        return 1
    fi
    echo "📋 Listing packages in: $env_name"
    clio get-pkg-list -e "$env_name"
}

# Delete package from environment
delete_package() {
    local pkg_name="$1"
    local env_name="$2"
    if [ -z "$pkg_name" ] || [ -z "$env_name" ]; then
        echo "❌ Usage: delete_package <package_name> <environment_name>"
        return 1
    fi
    echo "🗑️ Deleting package $pkg_name from $env_name"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        clio delete-pkg-remote "$pkg_name" -e "$env_name"
    else
        echo "❌ Operation cancelled"
    fi
}

# Workspace Management
# -------------------

# Create workspace
create_workspace() {
    local workspace_name="$1"
    if [ -z "$workspace_name" ]; then
        echo "❌ Usage: create_workspace <workspace_name>"
        return 1
    fi
    echo "🏗️ Creating workspace: $workspace_name"
    clio create-workspace "$workspace_name"
}

# Push workspace to environment
push_workspace() {
    local env_name="$1"
    if [ -z "$env_name" ]; then
        echo "❌ Usage: push_workspace <environment_name>"
        return 1
    fi
    echo "⬆️ Pushing workspace to: $env_name"
    clio push-workspace -e "$env_name"
}

# Restore workspace
restore_workspace() {
    echo "🔄 Restoring workspace"
    clio restore-workspace
}

# Development Tools
# ----------------

# Set developer mode
set_dev_mode() {
    local env_name="$1"
    local mode="${2:-true}"
    if [ -z "$env_name" ]; then
        echo "❌ Usage: set_dev_mode <environment_name> [true|false]"
        return 1
    fi
    echo "🔧 Setting developer mode to $mode for: $env_name"
    clio set-dev-mode -e "$env_name"
}

# Execute SQL script
execute_sql() {
    local script_file="$1"
    local env_name="$2"
    if [ -z "$script_file" ] || [ -z "$env_name" ]; then
        echo "❌ Usage: execute_sql <script_file> <environment_name>"
        return 1
    fi
    echo "📝 Executing SQL script $script_file on $env_name"
    clio execute-sql-script "$script_file" -e "$env_name"
}

# Set system setting
set_system_setting() {
    local setting_name="$1"
    local setting_value="$2"
    local env_name="$3"
    if [ -z "$setting_name" ] || [ -z "$setting_value" ] || [ -z "$env_name" ]; then
        echo "❌ Usage: set_system_setting <setting_name> <setting_value> <environment_name>"
        return 1
    fi
    echo "⚙️ Setting $setting_name to $setting_value on $env_name"
    clio set-syssetting "$setting_name" "$setting_value" -e "$env_name"
}

# Set feature state
set_feature() {
    local feature_name="$1"
    local feature_state="$2"
    local env_name="$3"
    if [ -z "$feature_name" ] || [ -z "$feature_state" ] || [ -z "$env_name" ]; then
        echo "❌ Usage: set_feature <feature_name> <feature_state> <environment_name>"
        return 1
    fi
    echo "🎛️ Setting feature $feature_name to $feature_state on $env_name"
    clio set-feature "$feature_name" "$feature_state" -e "$env_name"
}

# Open web application
open_app() {
    local env_name="$1"
    if [ -z "$env_name" ]; then
        echo "❌ Usage: open_app <environment_name>"
        return 1
    fi
    echo "🌐 Opening web application: $env_name"
    clio open-web-app -e "$env_name"
}

# Restart web application
restart_app() {
    local env_name="$1"
    if [ -z "$env_name" ]; then
        echo "❌ Usage: restart_app <environment_name>"
        return 1
    fi
    echo "🔄 Restarting web application: $env_name"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        clio restart-web-app -e "$env_name"
    else
        echo "❌ Operation cancelled"
    fi
}

# Utility Functions
# ----------------

# Show help
show_help() {
    echo "🔧 Clio Command Templates Help"
    echo "=============================="
    echo ""
    echo "Environment Management:"
    echo "  list_environments              - List all registered environments"
    echo "  set_active_env <env>           - Set active environment"
    echo "  test_connection <env>          - Test connection to environment"
    echo ""
    echo "Package Management:"
    echo "  create_package <name>          - Create new package"
    echo "  push_package <pkg> <env>       - Push package to environment"
    echo "  pull_package <pkg> <env>       - Pull package from environment"
    echo "  list_packages <env>            - List packages in environment"
    echo "  delete_package <pkg> <env>     - Delete package from environment"
    echo ""
    echo "Workspace Management:"
    echo "  create_workspace <name>        - Create workspace"
    echo "  push_workspace <env>           - Push workspace to environment"
    echo "  restore_workspace              - Restore workspace"
    echo ""
    echo "Development Tools:"
    echo "  set_dev_mode <env> [true|false] - Set developer mode"
    echo "  execute_sql <file> <env>       - Execute SQL script"
    echo "  set_system_setting <name> <value> <env> - Set system setting"
    echo "  set_feature <name> <state> <env> - Set feature state"
    echo "  open_app <env>                 - Open web application"
    echo "  restart_app <env>              - Restart web application"
    echo ""
    echo "Usage: source clio-templates.sh and then call functions directly"
}

# Export functions for use
export -f list_environments set_active_env test_connection
export -f create_package push_package pull_package list_packages delete_package
export -f create_workspace push_workspace restore_workspace
export -f set_dev_mode execute_sql set_system_setting set_feature
export -f open_app restart_app show_help

echo "✅ Clio templates loaded! Use 'show_help' for available commands."
