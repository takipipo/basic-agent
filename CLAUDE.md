# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an agentic application that integrates with local LLMs via Ollama. The agent accepts user input, processes it using the LLM to determine which tool to use, and then executes the appropriate tool.

## Architecture

The codebase follows a simple modular structure:

1. **Agent System**: Processes user input, coordinates with the LLM, and dispatches work to tools
2. **LLM Integration**: Interfaces with Ollama to access local language models
3. **Tools Framework**: Provides a mechanism to register and execute tools

### Key Components

- **Agent**: The main orchestrator that processes user input using the LLM and executes tools
- **ToolBox**: Manages tool registration and provides tool descriptions to the agent
- **OllamaModel**: Interfaces with the Ollama API to generate text using local models

## Development Environment Setup

### Prerequisites

1. Install [Ollama](https://ollama.ai/)
2. Pull the Mistral model:
   ```
   ollama pull mistral
   ```
3. Start the Ollama server:
   ```
   ollama serve
   ```

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd agentic

# Install dependencies
pip install -r requirements.txt
```

## Running the Application

```bash
# Run the main application
python main.py
```

This starts an interactive session where you can input prompts. The agent will process them and execute the appropriate tool.

## Implementation Details

- The agent uses a system prompt template with tool descriptions to instruct the LLM
- Tools currently implemented:
  - `basic_calculator`: Performs mathematical operations
  - `reverse_string`: Reverses input text
- The LLM is configured to output responses in JSON format with tool choice and input

## Extending the Codebase

### Adding New Tools

1. Create a function with proper docstring in `tools.py`
2. Add the tool to the tools list in `main.py`
3. Update the system prompt in `agent.py` if needed

### Integrating Different LLMs

Implement a new class similar to `OllamaModel` that follows the same interface:
- Initialize with model name, system prompt, and parameters
- Implement `generate_text(prompt)` method

### Future Code Organization

The empty directories in `src/` suggest a planned reorganization:
- `src/agent/`: Agent implementation
- `src/config/`: Configuration management
- `src/llm/`: LLM interface implementations
- `src/tools/`: Tool implementations