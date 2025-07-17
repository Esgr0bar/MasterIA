# Contributing to MasterIA

We welcome contributions to improve this project! Whether you want to report a bug, suggest an enhancement, submit code, or improve documentation, your help is appreciated.

## 🤝 How to Contribute

### 1. Fork the Repository
- Fork the project on GitHub to your account
- Clone your fork locally:
  ```bash
  git clone https://github.com/your-username/MasterIA.git
  cd MasterIA
  ```

### 2. Set Up Development Environment
- Create a virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```

- Install dependencies:
  ```bash
  pip install -r requirements.txt
  pip install -r requirements-dev.txt  # Development dependencies
  ```

### 3. Create a New Branch
- Create a branch for your changes:
  ```bash
  git checkout -b feature/my-feature
  # or
  git checkout -b fix/bug-description
  # or
  git checkout -b docs/documentation-update
  ```

### 4. Make Your Changes
- Implement your changes or additions
- Follow the coding standards (see below)
- Add tests for new functionality
- Update documentation if necessary

### 5. Test Your Changes
- Run the test suite:
  ```bash
  pytest tests/
  ```

- Run linting:
  ```bash
  flake8 src/
  black src/
  ```

- Test documentation build:
  ```bash
  mkdocs build
  ```

### 6. Commit and Push
- Stage your changes:
  ```bash
  git add .
  ```

- Commit with a descriptive message:
  ```bash
  git commit -m "Add feature: description of changes"
  ```

- Push to your fork:
  ```bash
  git push origin feature/my-feature
  ```

### 7. Create a Pull Request
- Go to the original repository on GitHub
- Click "New Pull Request"
- Select your branch and provide a clear description
- Reference any related issues

## 📋 Types of Contributions

### 🐛 Bug Reports
Help us improve by reporting bugs:

**Before reporting:**
- Check existing issues to avoid duplicates
- Try the latest version
- Test with minimal reproduction case

**Include in your report:**
- System information (OS, Python version, library versions)
- Steps to reproduce the issue
- Expected vs actual behavior
- Error messages and stack traces
- Sample audio files (if relevant)

**Template:**
```markdown
## Bug Description
Brief description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## System Information
- OS: [e.g., Ubuntu 20.04]
- Python: [e.g., 3.8.5]
- MasterIA: [e.g., 0.2.0]
- Dependencies: [paste output of pip freeze]

## Additional Context
Any other relevant information
```

### 💡 Feature Requests
Suggest new features or improvements:

**Before suggesting:**
- Check if the feature already exists
- Search existing feature requests
- Consider if it fits the project scope

**Include in your request:**
- Clear description of the feature
- Use cases and benefits
- Possible implementation approaches
- Examples or mockups (if applicable)

### 🔧 Code Contributions
Contribute code improvements:

**Types of code contributions:**
- Bug fixes
- New features
- Performance improvements
- Code refactoring
- Test improvements

**Guidelines:**
- Follow the existing code style
- Add appropriate tests
- Update documentation
- Keep changes focused and atomic

### 📝 Documentation Contributions
Help improve documentation:

**Types of documentation:**
- API documentation
- Usage examples
- Tutorials and guides
- README improvements
- Code comments

**Guidelines:**
- Use clear, concise language
- Include practical examples
- Test all code examples
- Follow existing documentation structure

## 📏 Coding Standards

### Python Style Guide
We follow PEP 8 with some modifications:

- **Line length**: 88 characters (Black default)
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings
- **Naming**: snake_case for functions and variables

### Code Formatting
We use automated formatting tools:

```bash
# Format code
black src/

# Sort imports
isort src/

# Lint code
flake8 src/
```

### Docstring Format
Use Google-style docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    """Brief description of the function.

    Longer description if needed. Explain what the function does,
    its purpose, and any important details.

    Args:
        param1 (str): Description of the first parameter.
        param2 (int): Description of the second parameter.

    Returns:
        bool: Description of the return value.

    Raises:
        ValueError: Description of when this exception is raised.

    Example:
        >>> result = example_function("hello", 42)
        >>> print(result)
        True
    """
    # Implementation here
    return True
```

## 🧪 Testing Guidelines

### Test Structure
Organize tests to mirror the source structure:

```
tests/
├── test_data_processing.py
├── test_feature_extraction.py
├── test_model_training.py
├── test_inference.py
└── fixtures/
    ├── sample_audio.wav
    └── sample_metadata.json
```

### Writing Tests
Follow these patterns:

```python
import pytest
import numpy as np
from src.data_processing import load_audio_files

class TestDataProcessing:
    """Test cases for data processing module."""
    
    def test_load_audio_files_success(self):
        """Test successful loading of audio files."""
        # Arrange
        directory = "tests/fixtures/audio/"
        
        # Act
        result = load_audio_files(directory)
        
        # Assert
        assert isinstance(result, dict)
        assert len(result) > 0
        assert all(isinstance(audio, np.ndarray) for audio in result.values())
```

## 📚 Documentation Guidelines

### Documentation Structure
Follow this structure for new documentation:

```markdown
# Title

Brief description of the topic.

## Overview
General overview and context.

## Usage
Basic usage examples.

## Examples
Practical examples with code.

## API Reference
Detailed function/class documentation.
```

### Code Examples
Include working code examples:

```python
# Always include imports
from src.data_processing import load_audio_files

# Provide complete, runnable examples
audio_data = load_audio_files("data/audio/")
print(f"Loaded {len(audio_data)} files")
```

## 🚀 Development Workflow

### Setting Up Development Environment

1. **Clone and setup:**
   ```bash
   git clone https://github.com/your-username/MasterIA.git
   cd MasterIA
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

2. **Run tests to ensure everything works:**
   ```bash
   pytest tests/
   ```

### Daily Development

1. **Pull latest changes:**
   ```bash
   git pull origin main
   ```

2. **Create feature branch:**
   ```bash
   git checkout -b feature/my-feature
   ```

3. **Make changes and test:**
   ```bash
   # Make your changes
   pytest tests/
   flake8 src/
   black src/
   ```

4. **Commit and push:**
   ```bash
   git add .
   git commit -m "Add feature: description"
   git push origin feature/my-feature
   ```

## 📊 Performance Considerations

### Code Performance
- Profile code before optimizing
- Use appropriate data structures
- Minimize memory allocation
- Cache expensive computations

### Audio Processing Performance
- Process audio in chunks for large files
- Use efficient audio libraries (LibROSA, scipy)
- Consider parallel processing for batch operations
- Optimize feature extraction algorithms

## 💡 Ideas for Contributions

### For Beginners
- Fix documentation typos
- Add code examples
- Improve error messages
- Add unit tests
- Update dependencies

### For Experienced Developers
- Implement new features
- Optimize performance
- Add advanced algorithms
- Improve architecture
- Add integration tests

### For Domain Experts
- Improve audio processing algorithms
- Add new feature extraction methods
- Enhance model architectures
- Validate algorithm accuracy
- Add domain-specific optimizations

## 📞 Getting Help

### Development Questions
- **GitHub Discussions**: Ask questions about development
- **Code Review**: Request feedback on your changes
- **Issue Tracker**: See what others are working on

### Resources
- **Project Documentation**: Complete API and usage documentation
- **Code Examples**: Working examples in notebooks/
- **Test Suite**: Examples of how to test your code

## 🏆 Recognition

### Contributors
All contributors are recognized in:
- GitHub contributors list
- Release notes
- Documentation credits
- Project README

### Types of Recognition
- **Code Contributors**: Direct code contributions
- **Documentation Contributors**: Documentation improvements
- **Community Contributors**: Help with issues and discussions
- **Bug Reporters**: Quality bug reports and testing

## 📜 Code of Conduct

### Our Pledge
We pledge to make participation in our project a harassment-free experience for everyone, regardless of background, experience level, or identity.

### Our Standards
- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other contributors

### Enforcement
Report any unacceptable behavior to the project maintainers. All complaints will be reviewed and investigated promptly.

---

Thank you for contributing to MasterIA! Your contributions help make this project better for everyone. 🎵🤖