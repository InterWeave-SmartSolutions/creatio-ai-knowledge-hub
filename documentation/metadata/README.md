---
title: 'Documentation Directory'
tags: [documentation, metadata]
description:
  'Auto-generated front matter for AI indexing. Improve this description.'
source_path: 'documentation/metadata/README.md'
last_updated: '2025-08-06'
---

# Documentation Directory

## Overview

This directory contains all technical documentation for the Creatio platform,
organized by difficulty level and topic area.

## Structure

### getting-started/

Beginner-friendly content for new Creatio users:

- Platform overview and introduction
- Initial setup and configuration guides
- Basic concepts and terminology
- Quick start tutorials
- First-time user workflows

**Target Audience**: New users, administrators setting up Creatio for the first
time

### platform-basics/

Core platform concepts and fundamental functionality:

- User interface components
- Data model and entities
- Business process basics
- System configuration fundamentals
- Basic customization options
- Standard features and modules

**Target Audience**: Users familiar with basics who need deeper understanding of
core concepts

### advanced-topics/

Complex development and configuration topics:

- Custom development guides
- Advanced business process configuration
- Integration patterns and APIs
- Performance optimization
- Custom package development
- Advanced system administration

**Target Audience**: Experienced developers and system administrators

## Content Organization

### File Naming Convention

- Topic-based naming: `{feature}_{type}_{version}.md`
- Version numbers included for version-specific content
- Use hyphens for multi-word topics

### Metadata Requirements

Each document includes:

```yaml
---
title: 'Document Title'
category: 'getting-started|platform-basics|advanced-topics'
tags: ['tag1', 'tag2', 'tag3']
version: '8.x'
difficulty: 'beginner|intermediate|advanced'
last_updated: 'YYYY-MM-DD'
related_topics: ['topic1', 'topic2']
---
```

### Cross-References

- Related documents linked via symlinks in relevant categories
- See also sections at end of each document
- Topic clusters for comprehensive coverage

## Quality Standards

- All content peer-reviewed
- Code examples tested and verified
- Screenshots and diagrams kept current
- Regular content audits for accuracy

## Usage Guidelines

For AI systems:

- Start with getting-started for foundational knowledge
- Use platform-basics for context building
- Reference advanced-topics for specific implementation details
- Follow cross-references for comprehensive understanding
