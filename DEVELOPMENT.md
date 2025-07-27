# Creatio Development Environment

This document provides comprehensive setup and usage instructions for the
Creatio development environment.

## 🚀 Quick Start

1. **Clone and Setup**

   ```bash
   git clone <repository-url>
   cd creatio-ai-knowledge-hub
   chmod +x scripts/setup-dev.sh
   ./scripts/setup-dev.sh
   ```

2. **Open in VS Code**

   ```bash
   code .
   ```

3. **Install Recommended Extensions**
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Extensions: Show Recommended Extensions"
   - Install all recommended extensions

## 📁 Project Structure

```
creatio-ai-knowledge-hub/
├── .vscode/                 # VS Code configuration
│   ├── extensions.json      # Recommended extensions
│   ├── settings.json        # Editor settings
│   └── launch.json          # Debug configurations
├── src/                     # Source files
│   ├── types/              # TypeScript definitions
│   ├── utils/              # Utility functions
│   ├── schemas/            # Creatio schemas
│   └── modules/            # Client modules
├── templates/              # Project templates
│   ├── client-modules/     # Client schema templates
│   ├── entity-schemas/     # Entity schema templates
│   └── business-processes/ # Business process templates
├── scripts/                # Development scripts
├── tests/                  # Test files
└── docs/                   # Documentation
```

## 🛠️ Development Tools

### Available Scripts

```bash
# Linting and formatting
npm run lint              # Fix linting issues
npm run lint:check        # Check for linting issues
npm run format            # Format code with Prettier
npm run format:check      # Check code formatting

# TypeScript
npm run type-check        # Type checking without compilation
npm run build             # Compile TypeScript
npm run dev               # Watch mode compilation

# Testing
npm run test              # Run tests
npm run test:watch        # Run tests in watch mode
npm run test:coverage     # Run tests with coverage

# Validation
npm run validate          # Run all checks (lint, format, type-check)
```

### VS Code Extensions

The following extensions are automatically recommended:

#### Essential Extensions

- **TypeScript**: Enhanced TypeScript support
- **ESLint**: Code linting
- **Prettier**: Code formatting
- **TailwindCSS**: CSS utilities

#### Creatio-Specific Extensions

- **XML Tools**: For Creatio schemas
- **C# Support**: For server-side development
- **REST Client**: For API testing

#### Development Tools

- **GitLens**: Enhanced Git integration
- **Path Intellisense**: Autocomplete for file paths
- **Auto Rename Tag**: Automatically rename paired tags

## 🔧 Configuration Files

### ESLint Configuration (`.eslintrc.js`)

- Configured for TypeScript and JavaScript
- Creatio-specific naming conventions
- Import/export rules
- Code quality rules

### Prettier Configuration (`.prettierrc.js`)

- Consistent code formatting
- File-specific overrides
- Creatio-friendly settings

### TypeScript Configuration (`tsconfig.json`)

- AMD module system (Creatio compatible)
- Path mapping for clean imports
- Strict type checking
- Source maps for debugging

## 🐛 Debugging

### Client-Side Debugging

1. **Attach to Chrome**

   ```json
   "name": "Attach to Chrome (Creatio Client)"
   ```

   - Start Chrome with debugging: `chrome --remote-debugging-port=9222`
   - Use this configuration to attach to running Chrome instance

2. **Launch Chrome**

   ```json
   "name": "Launch Chrome (Creatio Client)"
   ```

   - Automatically launches Chrome with debugging enabled
   - Update the URL in `.vscode/launch.json`

### Server-Side Debugging

1. **Attach to .NET Process**

   ```json
   "name": "Attach to .NET Process"
   ```

   - Attach to running IIS process
   - Debug C# server-side code

### Testing Debugging

1. **Debug Jest Tests**

   ```json
   "name": "Debug Jest Tests"
   ```

   - Debug individual test files
   - Set breakpoints in test code

## 📋 Code Templates

### Client Schema Template

Location: `templates/client-modules/ClientSchemaTemplate.js`

Features:

- Standard Creatio schema structure
- Predefined methods (init, onEntityInitialized, onSaved)
- Attributes configuration
- Diff array structure

### Entity Schema Template

Location: `templates/entity-schemas/EntitySchemaTemplate.cs`

Features:

- Entity event listener pattern
- CRUD event handlers
- Validation methods
- Business logic placeholders

## 🎯 Best Practices

### Code Style

- Use TypeScript for new development
- Follow ESLint rules
- Use Prettier for formatting
- Write JSDoc comments

### Git Workflow

- Pre-commit hooks validate code quality
- Conventional commit messages
- Feature branch workflow

### Testing

- Write unit tests for business logic
- Use integration tests for workflows
- Maintain test coverage > 80%

### Debugging

- Use source maps for accurate debugging
- Set breakpoints in TypeScript source
- Use Chrome DevTools for client debugging

## 🔍 Troubleshooting

### Common Issues

1. **ESLint Errors**

   ```bash
   npm run lint:check  # Check issues
   npm run lint        # Auto-fix issues
   ```

2. **TypeScript Errors**

   ```bash
   npm run type-check  # Check type issues
   ```

3. **Formatting Issues**

   ```bash
   npm run format:check  # Check formatting
   npm run format        # Fix formatting
   ```

4. **Git Hooks Not Working**
   ```bash
   npx husky install     # Reinstall hooks
   chmod +x .husky/*     # Make hooks executable
   ```

### VS Code Issues

1. **Extensions Not Loading**
   - Restart VS Code
   - Check extension compatibility
   - Update VS Code to latest version

2. **IntelliSense Not Working**
   - Reload window: `Ctrl+Shift+P` → "Developer: Reload Window"
   - Check TypeScript version
   - Verify tsconfig.json paths

## 📚 Additional Resources

- [Creatio Documentation](https://academy.creatio.com/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [ESLint Rules](https://eslint.org/docs/rules/)
- [Prettier Configuration](https://prettier.io/docs/en/configuration.html)

## 🤝 Contributing

1. Follow the established code style
2. Write tests for new features
3. Update documentation
4. Use conventional commit messages
5. Submit pull requests with detailed descriptions

## 📝 Notes

- Always update the Creatio instance URL in debug configurations
- Use feature branches for development
- Keep dependencies up to date
- Regular code reviews ensure quality
