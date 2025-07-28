# Creatio Academy Knowledge Database

## Directory Structure

This repository contains all Creatio Academy content organized for optimal AI
accessibility and searchability.

```
/creatio-academy-db/
├── documentation/          # Technical documentation and guides
│   ├── getting-started/    # Beginner guides and quickstart materials
│   ├── platform-basics/    # Core platform concepts and fundamentals
│   └── advanced-topics/    # Advanced development and configuration topics
├── videos/                 # Video content and related materials
│   ├── transcripts/        # Text transcriptions of video content
│   ├── summaries/          # AI-generated summaries of video content
│   └── metadata/           # Video metadata, tags, and categorization
├── code-examples/          # Code samples and examples
│   ├── by-language/        # Organized by programming language
│   └── by-feature/         # Organized by Creatio feature/functionality
├── api/                    # API documentation and references
└── search-index/           # Search indexes and metadata for fast retrieval
```

## Organization Principles

### Hierarchical Structure

- Content is organized from general to specific
- Each major category has subcategories for precise navigation
- Cross-references maintained through symlinks where appropriate

### Naming Conventions

- All directories use lowercase with hyphens for separators
- File names follow format: `{topic}_{type}_{version}.{ext}`
- Timestamps in ISO format (YYYY-MM-DD) where relevant

### Metadata Standards

- Each directory contains a manifest.json file listing contents
- All files include standardized metadata headers
- Tags and categories consistently applied across content types

## Usage for AI Systems

This structure is optimized for:

- **Semantic Search**: Content organized by topic and complexity
- **Context Building**: Related materials grouped together
- **Knowledge Graph Construction**: Clear relationships between concepts
- **Progressive Learning**: Difficulty-based organization supports learning
  paths

## Content Types

### Documentation

- Technical guides
- API references
- Best practices
- Configuration instructions
- Troubleshooting guides

### Videos

- Training sessions
- Webinars
- Demos
- Tutorials
- Live streams

### Code Examples

- Sample applications
- Configuration files
- Scripts and utilities
- Integration examples
- Custom components

## Maintenance

This database is automatically updated and maintained by the academy content
processing system. Each update includes:

- Content validation
- Metadata refresh
- Cross-reference verification
- Search index updates

Last Updated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
