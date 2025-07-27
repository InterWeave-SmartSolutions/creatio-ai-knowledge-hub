# Package Versioning Strategy

This document outlines the versioning strategy for managing package versions in the Creatio AI Knowledge Hub project.

## Versioning Scheme

We follow the Semantic Versioning (SemVer) methodology:

- **MAJOR** version when you make incompatible API changes.
- **MINOR** version when you add functionality in a backwards-compatible manner.
- **PATCH** version when you make backwards-compatible bug fixes.

**Format:**
```
MAJOR.MINOR.PATCH
```

## Guidelines

1. **Backwards Compatibility:**
   - Interfaces or APIs that impact downstream dependencies should be carefully managed to minimize breaking changes.
   - Deprecate old APIs gradually with clear guidance on migration paths.

2. **Pre-Release Versions:**
   - We use identifiers like `-alpha`, `-beta`, `-rc` for pre-release versions to indicate instability and possible breaking changes:
     - `1.0.0-alpha`
     - `1.0.0-beta`
     - `1.0.0-rc`

3. **Labeling**:
   - Use metadata labels to provide additional build information as demonstrated below:
   ```
   1.0.0-alpha+001
   1.0.0+20191108141256
   ```
   - These labels are optional and provide information such as build date or specific build identifiers, enhancing traceability.

## Practical Usage

- **Releasing Updates:**
  - Ensure all changes are backward-compatible or well-documented if they break compatibility.
  - Major releases should be infrequent and involve stakeholder communication.

- **Commit Practices:**
  - Use meaningful commit messages reflecting changes or fixes made, aiding in the changelog generation and historical tracking.
  - Maintain concise and expressive release notes accompanying each version.

## Automation and Tooling

- **Dependency Management:** Automated scripts and tools will ensure versions are consistent across environments.
- **Continuous Integration:** Automated version increments can be achieved through the integration of CI/CD pipelines.

## Conclusion

By adhering to this strategy, our release cycle maintains clarity and consistency, offering users a structured roadmap with minimal disruption while encouraging innovation and progress.

