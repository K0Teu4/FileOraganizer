# Contributing to File Organizer

Thank you for your interest in contributing! 🎉

## How to Contribute

### Reporting Bugs

If you found a bug, please open an issue using the **Bug Report** template and include:

- A clear description of the problem
- Steps to reproduce
- Expected vs. actual behavior
- Your Python version and operating system
- Any relevant log output

### Suggesting Features

Have an idea? Use the **Feature Request** template and describe:

- The problem your feature solves
- A proposed solution or API change
- Alternatives you considered

### Pull Requests

1. **Fork** the repository and create your branch from `main`.
2. **Follow** the existing code style (PEP 8, type hints, docstrings).
3. **Write** or update tests if you add new logic.
4. **Update** `README.md` if your change affects user-facing behavior.
5. **Open** a Pull Request and fill out the template.

## Development Setup

```bash
git clone https://github.com/yourusername/file-organizer.git
cd file-organizer

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Run the app
python main.py
```

## Code Style

- Python 3.10+ with type hints
- Docstrings for every public function (Google style)
- Maximum line length: 100 characters
- Use `pathlib.Path` for filesystem operations

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
