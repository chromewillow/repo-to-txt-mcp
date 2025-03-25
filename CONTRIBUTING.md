# Contributing to repo-to-txt-mcp

Thank you for your interest in contributing to repo-to-txt-mcp! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Please read and follow our [Code of Conduct](docs/CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs

If you find a bug, please report it by creating a new issue in the GitHub repository. When filing a bug report, please include:

- A clear, descriptive title
- A detailed description of the issue
- Steps to reproduce the problem
- Expected behavior and actual behavior
- Any relevant logs or error messages
- Your environment (OS, Python version, Node.js version, etc.)

### Suggesting Enhancements

We welcome suggestions for enhancements to the project. To suggest an enhancement:

1. Create a new issue in the GitHub repository
2. Use a clear and descriptive title
3. Provide a detailed description of the suggested enhancement
4. Explain why this enhancement would be useful
5. If possible, include examples or mockups

### Pull Requests

We actively welcome pull requests for bug fixes, enhancements, and documentation improvements. Here's how to submit a pull request:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes
4. Add or update tests as necessary
5. Ensure all tests pass
6. Update documentation if needed
7. Submit a pull request

#### Pull Request Guidelines

- Keep your changes focused. If you're fixing a bug, only include the bug fix
- Follow the existing code style
- Write clear commit messages
- If your PR fixes a specific issue, reference it in the PR description
- Update documentation if your changes affect user-facing features

## Development Setup

To set up the project for local development:

1. Clone the repository:
   ```bash
   git clone https://github.com/chromewillow/repo-to-txt-mcp.git
   cd repo-to-txt-mcp
   ```

2. Install the Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install the Node.js dependencies:
   ```bash
   npm install
   ```

4. Run the server locally:
   ```bash
   node smithery-wrapper.js
   ```

## Code Style

- For Python code, follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines
- For JavaScript code, follow the existing style in the repository
- Use meaningful variable and function names
- Write docstrings for all functions and classes
- Add comments for complex code sections

## Testing

When adding new features or fixing bugs, please add appropriate tests. To run the existing tests:

```bash
# Run Python tests
python -m unittest discover tests

# Run Node.js tests
npm test
```

## Documentation

Documentation is critical for this project. Please update or add documentation when making changes to:

- API endpoints
- Command-line interface
- Configuration options
- Installation procedures

## License

By contributing to this project, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).

## Questions

If you have any questions about contributing, please open an issue in the GitHub repository.