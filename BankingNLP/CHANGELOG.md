# Changelog

All notable changes to Banking NLP Toolkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-06-17

### Added
- Initial release of Banking NLP Toolkit
- spaCy-based text processing pipeline for Russian banking documents
- Banking document classification with configurable labels
- Named entity recognition for banking-specific entities
- Text preprocessing with configurable options
- CLI interface for batch and single document processing
- Comprehensive configuration system using YAML
- Unit and integration test suite with pytest
- CI/CD pipeline with GitHub Actions
- Code quality tools (black, isort, flake8, mypy)
- Pre-commit hooks for code quality enforcement
- Comprehensive documentation and examples
- Support for custom classifier training
- Data loading utilities for JSON and CSV formats
- Banking-specific utility functions
- Docker support (coming soon)

### Features
- **Document Classification**: Classify banking documents into categories (transfer, payment, loan, deposit, statement, contract, other)
- **Named Entity Recognition**: Extract amounts, dates, account numbers, and other banking entities
- **Text Preprocessing**: Configurable text cleaning and normalization
- **Batch Processing**: Efficient processing of multiple documents
- **Configurable Pipeline**: YAML-based configuration for all components
- **Multi-format Support**: JSON and CSV data loading
- **Extensible Architecture**: Easy to add custom components and models

### Technical Details
- Python 3.8+ support
- spaCy 3.4+ integration with ru_core_news_md model
- scikit-learn for machine learning components
- Pydantic for configuration validation
- Click for CLI interface
- Loguru for structured logging
- Comprehensive test coverage (>80%)

### Documentation
- Detailed README with quick start guide
- API documentation with Sphinx
- Usage examples and tutorials
- Configuration reference
- Contributing guidelines
- Changelog and release notes

## [Unreleased]

### Planned Features
- Docker containerization
- REST API interface
- Additional language models support
- Enhanced entity recognition rules
- Model training GUI
- Performance optimizations
- Streaming processing for large files
- Integration with popular ML platforms

### Known Issues
- Large model files need to be downloaded separately
- Some entity recognition patterns may need fine-tuning
- Performance could be optimized for very large documents

### Contributing
We welcome contributions! Please see our contributing guidelines for details.

### License
This project is licensed under the MIT License - see the LICENSE file for details.
