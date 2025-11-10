# Contributing to Functions-SDK for Python

Thank you for your interest in contributing to the Functions-SDK for Python! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Code Quality](#code-quality)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Project Structure](#project-structure)

## Getting Started

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Git

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/functions-sdk-python.git
   cd functions-sdk-python
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/cslab/functions-sdk-python.git
   ```

## Development Setup

### Using uv (Recommended)

This project uses [uv](https://github.com/astral-sh/uv) for dependency management:

```bash
# Install dependencies
uv sync

# Activate the virtual environment
source .venv/bin/activate  # On Linux/macOS
# or
.venv\Scripts\activate  # On Windows
```

### Using pip

Alternatively, you can use pip:

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Linux/macOS

# Install the package in editable mode with dev dependencies
pip install -e ".[dev,test]"
```

### Install Pre-commit Hooks

We use pre-commit hooks to ensure code quality:

```bash
# Install pre-commit
pip install pre-commit

# Set up the git hooks
pre-commit install
```

The hooks will run automatically on every commit. You can also run them manually:

```bash
pre-commit run --all-files
```

## Development Workflow

### Creating a Branch

Create a feature branch for your changes:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### Making Changes

1. Make your changes in your feature branch
2. Write or update tests as needed
3. Update documentation if you're changing functionality
4. Ensure all tests pass
5. Commit your changes with clear, descriptive commit messages

### Commit Messages

Follow these guidelines for commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Start with a type prefix:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation changes
  - `test:` for test changes
  - `chore:` for maintenance tasks
  - `refactor:` for code refactoring

Example:
```
feat: Add support for workflow task triggers

- Implement WorkflowTaskTriggerEvent class
- Add event handler documentation
- Include usage examples
```

## Code Quality

This project uses several tools to maintain code quality:

### Ruff

We use [Ruff](https://github.com/astral-sh/ruff) for linting and formatting:

```bash
# Run linter
ruff check .

# Run linter with auto-fix
ruff check --fix .

# Run formatter
ruff format .
```

### MyPy

We use [MyPy](https://mypy-lang.org/) for static type checking:

```bash
mypy csfunctions
```

### Bandit

We use [Bandit](https://bandit.readthedocs.io/) for security linting:

```bash
bandit -r csfunctions
```

All these checks run automatically via pre-commit hooks.

### Code Style Guidelines

- Line length: 120 characters
- Use type hints for all function parameters and return values
- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- Add docstrings to public classes and functions

## Testing

### Running Tests

Run the test suite using pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=csfunctions

# Run specific test file
pytest tests/test_handler.py

# Run specific test
pytest tests/test_handler.py::test_specific_function
```

### Writing Tests

- Write tests for all new features and bug fixes
- Place tests in the `tests/` directory
- Use descriptive test names that explain what is being tested
- Follow the existing test structure and patterns
- Aim for high test coverage

## Documentation

### Building Documentation

The project uses [MkDocs](https://www.mkdocs.org/) with Material theme:

```bash
# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build
```

Visit http://127.0.0.1:8000 to view the documentation locally.

### Updating Documentation

- Update relevant documentation in the `docs/` directory when changing functionality
- Include examples for new features
- Keep the API reference up to date
- Update the release notes for significant changes

### Generating Schemas

If you modify request/response structures, regenerate the JSON schemas:

```bash
python -m csfunctions.tools.write_schema
```

### Generating Tables

Update the documentation tables:

```bash
python -m tools.mdtable
```

## Submitting Changes

### Before Submitting

1. Ensure all tests pass: `pytest`
2. Ensure code quality checks pass: `pre-commit run --all-files`
3. Update documentation as needed
4. Update or add tests for your changes
5. Rebase your branch on the latest upstream main:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

### Creating a Pull Request

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Create a pull request on GitHub with:
   - A clear title describing the change
   - A detailed description of what changed and why
   - References to any related issues
   - Screenshots or examples if applicable

3. Wait for review and address any feedback

### Pull Request Guidelines

- Keep pull requests focused on a single feature or fix
- Ensure CI checks pass
- Respond to review comments in a timely manner
- Be open to feedback and suggestions
- Update your PR based on feedback

## Project Structure

```
functions-sdk-python/
├── csfunctions/           # Main package
│   ├── actions/          # Action implementations
│   ├── events/           # Event type definitions
│   ├── objects/          # Object models (Part, Document, etc.)
│   ├── service/          # Service implementations
│   └── tools/            # Development tools
├── tests/                # Test suite
├── docs/                 # Documentation source
├── json_schemas/         # JSON schema definitions
├── tools/                # Development utilities
├── pyproject.toml        # Project configuration
├── Makefile              # Build commands
└── mkdocs.yml           # Documentation configuration
```

## Questions or Problems?

If you have questions or run into problems:

- Check the [documentation](https://cslab.github.io/functions-sdk-python/)
- Open an issue on GitHub
- Review existing issues and pull requests

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🎉
