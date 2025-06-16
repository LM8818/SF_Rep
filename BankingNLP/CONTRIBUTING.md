# Contributing to Banking NLP Toolkit

Thank you for your interest in contributing to Banking NLP Toolkit! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists in [GitHub Issues](https://github.com/LM8818/SF_Rep/issues)
2. If not, create a new issue with:
   - Clear description of the problem/feature
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Environment details (Python version, OS, etc.)
   - Relevant code snippets or error messages

### Submitting Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/SF_Rep.git
   cd SF_Rep/BankingNLP
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up development environment**
   ```bash
   make install-dev
   ```

4. **Make your changes**
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation as needed

5. **Test your changes**
   ```bash
   make test
   make lint
   ```

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

7. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📋 Development Guidelines

### Code Style

We use several tools to maintain code quality:

- **Black** for code formatting (line length: 88)
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Run all checks:
```bash
make format
make lint
```

### Commit Messages

Use clear, descriptive commit messages:
```
Add feature: banking document entity extraction
Fix bug: handle empty text in preprocessor
Update docs: add configuration examples
```

### Testing

- Write tests for all new functionality
- Maintain test coverage above 80%
- Include both unit and integration tests
- Test edge cases and error conditions

```bash
# Run all tests
make test

# Run specific test types
make test-unit
make test-integration
```

### Documentation

- Update README if adding user-facing features
- Add docstrings to all public functions/classes
- Include type hints for all function parameters
- Add usage examples for new features

## 🏗️ Project Structure

```
BankingNLP/
├── banking_nlp/           # Main package
│   ├── config/           # Configuration management
│   ├── data/             # Data processing
│   ├── models/           # ML models and pipeline
│   └── utils/            # Utility functions
├── tests/                # Test suite
├── docs/                 # Documentation
├── scripts/              # Utility scripts
└── configs/              # Configuration files
```

## 🎯 Areas for Contribution

### High Priority
- [ ] Additional entity recognition patterns
- [ ] Performance optimizations
- [ ] More comprehensive tests
- [ ] Documentation improvements
- [ ] Error handling enhancements

### Medium Priority
- [ ] Support for additional file formats
- [ ] Custom model training improvements
- [ ] CLI enhancements
- [ ] Integration examples
- [ ] Benchmarking tools

### Future Features
- [ ] REST API interface
- [ ] Docker containerization
- [ ] Additional language support
- [ ] GUI for model training
- [ ] Streaming processing

## 🔍 Code Review Process

1. All PRs require at least one review
2. CI/CD checks must pass
3. Code coverage should not decrease
4. Documentation must be updated for user-facing changes
5. Breaking changes require major version bump

## 📦 Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create release tag
4. Build and publish to PyPI
5. Update documentation

## 🧪 Testing Strategy

### Unit Tests
- Test individual functions/classes
- Mock external dependencies
- Test edge cases and error conditions

### Integration Tests
- Test complete workflows
- Use real spaCy models (when available)
- Test configuration loading and validation

### Performance Tests
- Benchmark processing speed
- Memory usage validation
- Scalability testing

## 🏃‍♂️ Quick Start for Contributors

```bash
# 1. Fork and clone
git clone https://github.com/your-username/SF_Rep.git
cd SF_Rep/BankingNLP

# 2. Setup development environment
make install-dev

# 3. Run tests to ensure everything works
make test

# 4. Make your changes
# ... edit code ...

# 5. Test and lint
make test
make lint

# 6. Commit and push
git add .
git commit -m "Your changes"
git push origin your-branch

# 7. Create pull request
```

## 💬 Getting Help

- Join our discussions in GitHub Issues
- Check existing documentation
- Look at example usage in `scripts/`
- Ask questions in pull request comments

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be acknowledged in:
- Release notes
- README contributors section
- Project documentation

Thank you for helping make Banking NLP Toolkit better! 🚀
