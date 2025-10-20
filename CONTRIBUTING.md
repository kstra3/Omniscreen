# Contributing to OmniScreen

Thank you for considering contributing to OmniScreen! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help create a welcoming environment

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Use the bug report template
3. Include:
   - Your OS and Python version
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Log files

### Suggesting Features

1. Check if the feature has been requested
2. Explain the use case
3. Provide examples
4. Consider backward compatibility

### Code Contributions

1. **Fork the repository**

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Follow coding standards**
   - PEP 8 style guide
   - Type hints where appropriate
   - Docstrings for functions and classes
   - Comments for complex logic

4. **Write tests**
   - Unit tests for new functions
   - Integration tests for features
   - Maintain or improve code coverage

5. **Update documentation**
   - Update README.md if needed
   - Add docstrings
   - Update INSTALLATION.md for new dependencies

6. **Commit changes**
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

7. **Push and create pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Pull Request Process

1. Update documentation
2. Add tests
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers
6. Address feedback

## Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/OmniScreen.git
cd OmniScreen

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy

# Run tests
python -m pytest tests/ -v

# Check code style
black --check .
flake8 .
mypy .
```

## Code Style

### Python Style Guide

- Follow PEP 8
- Use meaningful variable names
- Keep functions focused and small
- Maximum line length: 100 characters
- Use type hints

### Example

```python
def capture_screenshot(
    mode: CaptureMode,
    window_name: Optional[str] = None
) -> Tuple[Image.Image, Optional[str]]:
    """
    Capture a screenshot with the specified mode.
    
    Args:
        mode: Capture mode (fullscreen, window, or region)
        window_name: Name of window to capture (for window mode)
    
    Returns:
        Tuple of (captured image, window name)
    
    Raises:
        ValueError: If invalid mode or parameters
        CaptureError: If capture fails
    """
    # Implementation
    pass
```

### Documentation

- Use docstrings for all public functions and classes
- Include Args, Returns, and Raises sections
- Add inline comments for complex logic
- Keep Greek theme references in comments

### Testing

- Write unit tests for new functions
- Use mocks for external dependencies
- Test edge cases and error conditions
- Aim for >80% code coverage

```python
def test_capture_fullscreen(self):
    """Test fullscreen capture functionality."""
    capture = ScreenCapture()
    image, window_name = capture.capture_fullscreen()
    
    self.assertIsInstance(image, Image.Image)
    self.assertIsNone(window_name)
```

## Greek Theme Guidelines

When adding UI elements or documentation:

- Use pastel colors from the theme palette
- Reference Greek mythology or philosophy in comments
- Maintain the classical aesthetic
- Use Greek letters or phrases tastefully

## Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Example:
```
feat: Add multi-monitor selection in region capture

- Allow users to select which monitor to capture from
- Add monitor detection in region selector
- Update UI to show monitor boundaries

Closes #123
```

## Questions?

- Open an issue for discussion
- Join our community chat (if available)
- Email maintainers

---

*Εὐχαριστῶ! (Thank you!)*
