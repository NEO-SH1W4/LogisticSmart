# Contributing to LogisticSmart 🤝

Thank you for your interest in contributing to LogisticSmart! This document outlines the contribution process and guidelines.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contribution Process](#contribution-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)

## 📜 Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Git
- Basic knowledge of Streamlit and pandas

### Types of Contributions

We welcome:
- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation improvements
- 🧪 Test improvements
- 🎨 UI/UX enhancements
- 🌍 Translations

## 🛠️ Development Setup

1. **Fork the repository**
```bash
# Click the "Fork" button on GitHub
```

2. **Clone your fork**
```bash
git clone https://github.com/YOUR_USERNAME/LogisticSmart.git
cd LogisticSmart
```

3. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

5. **Create a branch**
```bash
git checkout -b feature/your-feature-name
```

## 🔄 Contribution Process

1. **Check existing issues** or create a new one
2. **Discuss** your proposed changes
3. **Fork** the repository
4. **Create** a feature branch
5. **Make** your changes
6. **Test** thoroughly
7. **Submit** a pull request

## 📏 Coding Standards

### Python Style
- Follow **PEP 8** guidelines
- Use **Black** for code formatting
- Use **isort** for import sorting
- Use **flake8** for linting

```bash
# Format code
black .
isort .

# Check style
flake8 src/ tests/
```

### Code Structure
- Keep functions small and focused
- Use descriptive variable names
- Add docstrings for all functions and classes
- Follow existing project patterns

### Example
```python
def process_delivery_data(df: pd.DataFrame) -> pd.DataFrame:
    \"\"\"
    Process delivery data by cleaning and validating columns.
    
    Args:
        df: Raw delivery data DataFrame
        
    Returns:
        Processed and validated DataFrame
        
    Raises:
        ValueError: If required columns are missing
    \"\"\"
    # Implementation here
    pass
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_data_processor.py
```

### Writing Tests
- Write tests for all new functionality
- Maintain minimum 80% test coverage
- Use descriptive test names
- Include edge cases

### Test Example
```python
def test_process_delivery_data_with_valid_input():
    \"\"\"Test data processing with valid input data.\"\"\"
    # Arrange
    input_df = pd.DataFrame({
        'deliverer': ['John', 'Jane'],
        'status': ['delivered', 'pending']
    })
    
    # Act
    result = process_delivery_data(input_df)
    
    # Assert
    assert len(result) == 2
    assert 'deliverer' in result.columns
```

## 📝 Documentation

### Documentation Guidelines
- Update README.md for significant changes
- Add docstrings to all functions and classes
- Update CHANGELOG.md
- Include examples for new features

### Documentation Structure
```
docs/
├── en/                 # English documentation
├── pt-br/             # Portuguese documentation
├── api/               # API documentation
└── examples/          # Usage examples
```

## 🔃 Pull Request Process

### Before Submitting
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated
- [ ] No merge conflicts

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] New tests added (if applicable)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
```

### Review Process
1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Testing** in development environment
4. **Approval** and merge

## 🌍 Internationalization

### Adding Translations
- Create language-specific directories under `docs/`
- Follow the structure: `docs/{language-code}/`
- Translate all user-facing documentation

### Supported Languages
- 🇺🇸 English (primary)
- 🇧🇷 Portuguese (secondary)

## 🏷️ Issue Labels

| Label | Description |
|-------|-------------|
| `bug` | Something isn't working |
| `enhancement` | New feature or request |
| `documentation` | Improvements to documentation |
| `good first issue` | Good for newcomers |
| `help wanted` | Extra attention needed |

## 💬 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: For security issues

## 🎯 Development Priorities

### High Priority
- Bug fixes
- Security improvements
- Performance optimizations

### Medium Priority
- New features
- UI/UX improvements
- Documentation enhancements

### Low Priority
- Code refactoring
- Style improvements

## 📈 Release Process

1. **Version bump** in relevant files
2. **Update CHANGELOG.md**
3. **Create release branch**
4. **Final testing**
5. **Merge to main**
6. **Create GitHub release**
7. **Deploy to production**

## 🙏 Recognition

Contributors will be:
- Added to the contributors list
- Mentioned in release notes
- Credited in documentation

---

Thank you for contributing to LogisticSmart! Your efforts help make logistics management more efficient for everyone. 🚀

