# AI Engineering Team - Multi-Agent Software Development System

This project demonstrates a multi-agent software development system built with **CrewAI**. It simulates an engineering team where each AI agent has a defined role, working together to design, implement, test, and build interfaces for software applications starting from high-level requirements.

---

## Overview

The system models a standard development workflow using four specialized agents:

* **Engineering Lead**: Creates technical designs from requirements
* **Backend Engineer**: Implements the core functionality in Python
* **Frontend Engineer**: Builds Gradio-based user interfaces
* **Test Engineer**: Writes unit tests for coverage and reliability

---

## Features

* Multi-agent orchestration with defined roles
* End-to-end workflow: requirements → design → backend → frontend → tests
* Automated code generation and UI creation
* Configurable architecture via YAML files
* Outputs include design docs, Python modules, UIs, and test suites

---

## Architecture

**Workflow**

```
Requirements → Engineering Lead → Backend Engineer → Frontend Engineer → Test Engineer
                     ↓                    ↓                   ↓                ↓
               Design Document      Python Module        Gradio UI        Unit Tests
```

**Agent Responsibilities**

1. **Engineering Lead**

   * Analyzes requirements
   * Produces design documents with class structures, methods, and approach

2. **Backend Engineer**

   * Implements production-ready Python modules
   * Adheres to design specifications

3. **Frontend Engineer**

   * Builds simple Gradio-based interfaces
   * Connects UI to backend functions

4. **Test Engineer**

   * Generates test cases and test suites
   * Ensures coverage of edge cases and core functionality

---

## Project Structure

```
7_project/
├── src/engineering_team/
│   ├── config/
│   │   ├── agents.yaml          # Agent configurations
│   │   └── tasks.yaml           # Task definitions
│   ├── tools/                   # Custom tools for agents
│   ├── crew.py                  # Crew definition
│   └── main.py                  # Entry point
├── output/                      # Generated outputs
├── example_output_*/            # Example generated projects
├── knowledge/                   # Knowledge base (if used)
├── pyproject.toml               # Project config
├── uv.lock                      # Dependency lock
└── README.md                    # Documentation
```

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/omjambhale/7_project.git
   cd 7_project
   ```

2. Install dependencies:

   ```bash
   # Using uv (recommended)
   uv sync

   # Or using pip
   pip install -e .
   ```

3. Set up environment variables:

   ```bash
   cp env_template.txt .env
   # Add your API keys to .env
   ```

---

## Usage

### Run the default example

```bash
# Using the installed script
engineering_team

# Or directly
python src/engineering_team/main.py
```

### Custom projects

Modify the `requirements` variable in `main.py`:

```python
requirements = """
Your project requirements here
"""
module_name = "your_module.py"
class_name = "YourClass"
```

### Commands

```bash
uv run engineering_team   # Run main workflow
uv run run_crew           # Same as above
uv run train              # Training mode
uv run replay             # Replay a previous run
uv run test               # Test mode
```

---

## Example Output

For the default trading simulation project, the system produces:

* `accounts.py`: Python module for account and portfolio management
* `app.py`: Gradio interface for interaction
* `test_accounts.py`: Unit tests with edge case coverage
* `accounts.py_design.md`: Design document describing implementation

---

## Configuration

* **`agents.yaml`** – Defines each agent’s role, model, and configuration
* **`tasks.yaml`** – Defines task descriptions, expected outputs, dependencies, and file outputs

---

## Use Cases

* Prototyping applications from requirements
* Exploring AI-driven software workflows
* Educational demos of multi-agent systems
* Automating boilerplate implementations

