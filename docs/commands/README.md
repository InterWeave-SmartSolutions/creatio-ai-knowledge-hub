# Command Reference

This document provides a complete reference to the commands available within the Creatio AI Knowledge Hub. Use this guide to understand the available functionality, command syntax, and examples.

## Categories

### General Commands

- **Run Complete Processing Pipeline**
  - **Command**: `./run_complete_pipeline.sh run`
  - **Description**: Processes all content from start to finish, including crawling, downloading, transcribing, indexing, and reporting.
  - **Usage**:
    ```bash
    ./run_complete_pipeline.sh run
    ```

- **Check Pipeline Status**
  - **Command**: `./run_complete_pipeline.sh status`
  - **Description**: Retrieves the current status of the content processing pipeline.
  - **Usage**:
    ```bash
    ./run_complete_pipeline.sh status
    ```

- **Check Dependencies**
  - **Command**: `./run_complete_pipeline.sh check`
  - **Description**: Checks that all necessary dependencies for running the pipeline are installed and configured.
  - **Usage**:
    ```bash
    ./run_complete_pipeline.sh check
    ```

- **Clean Cache**
  - **Command**: `./run_complete_pipeline.sh clean`
  - **Description**: Cleans temporary files and cached data to free up space and ensure fresh processing.
  - **Usage**:
    ```bash
    ./run_complete_pipeline.sh clean
    ```

- **Start MCP Server**
  - **Command**: `python ai_knowledge_hub/enhanced_mcp_server.py`
  - **Description**: Starts the MCP server for real-time AI agent integration and search.
  - **Usage**:
    ```bash
    python ai_knowledge_hub/enhanced_mcp_server.py
    ```

### Video Processing Commands

- **Process All Videos**
  - **Command**: `python scripts/utilities/transcription_processor.py`
  - **Description**: Transcribes all videos in the specified directory using the Whisper AI model.
  - **Usage**:
    ```bash
    python scripts/utilities/transcription_processor.py
    ```

- **Download Video Content**
  - **Command**: `./run_download.sh start`
  - **Description**: Initiates the video download process using the defined sources and configuration options.
  - **Usage**:
    ```bash
    ./run_download.sh start
    ```

### Troubleshooting Commands

- **Diagnose System**
  - **Command**: `bash diagnose.sh`
  - **Description**: Runs a set of diagnostic checks to identify common issues with system setup and configuration.
  - **Usage**:
    ```bash
    bash diagnose.sh
    ```

- **Health Check**
  - **Command**: `python health_check.py`
  - **Description**: Checks the health of the MCP server, database, and search capabilities.
  - **Usage**:
    ```bash
    python health_check.py
    ```

- **Reset System**
  - **Command**: `bash reset_system.sh`
  - **Description**: Completely resets the system, clearing databases, caches, and logs.
  - **Usage**:
    ```bash
    bash reset_system.sh
    ```

---

## Common Aliases

You can define these shortcuts in your shell to streamline command usage:

```bash
alias mcp-run='./run_complete_pipeline.sh run'
alias mcp-status='./run_complete_pipeline.sh status'
alias mcp-clean='./run_complete_pipeline.sh clean'
alias mcp-start='python ai_knowledge_hub/enhanced_mcp_server.py'
```

## Command Structure

Every command follows consistent syntax rules for easy understanding and execution:
- **Structure**: `<script> <action> <options>`
- **Help**: Access any command's help by using the `--help` option

## Troubleshooting

For any command-related issues, refer to the [Troubleshooting Guide](../setup/troubleshooting.md).

