"""Tests for configuration module."""

import pytest
import tempfile
from pathlib import Path
import yaml

from banking_nlp.config.settings import Config, load_config, create_default_config


class TestConfig:
    """Test configuration handling."""

    def test_default_config(self):
        """Test default configuration creation."""
        config = Config()

        assert config.model.name == "ru_core_news_md"
        assert config.classification.threshold == 0.7
        assert config.processing.lowercase is True
        assert config.logging.level == "INFO"

    def test_config_validation(self):
        """Test configuration validation."""
        # Valid config
        config_data = {
            "model": {"name": "test_model"},
            "classification": {"threshold": 0.8},
        }
        config = Config(**config_data)
        assert config.model.name == "test_model"
        assert config.classification.threshold == 0.8

    def test_invalid_threshold(self):
        """Test invalid threshold validation."""
        with pytest.raises(ValueError):
            Config(classification={"threshold": 1.5})  # > 1.0

        with pytest.raises(ValueError):
            Config(classification={"threshold": -0.1})  # < 0.0

    def test_load_config_from_file(self):
        """Test loading configuration from YAML file."""
        config_data = {
            "model": {"name": "custom_model", "batch_size": 50},
            "classification": {"threshold": 0.6, "labels": ["test1", "test2"]},
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = f.name

        try:
            config = load_config(temp_path)
            assert config.model.name == "custom_model"
            assert config.model.batch_size == 50
            assert config.classification.threshold == 0.6
            assert "test1" in config.classification.labels
        finally:
            Path(temp_path).unlink()

    def test_load_config_file_not_found(self):
        """Test loading non-existent config file."""
        with pytest.raises(FileNotFoundError):
            load_config("non_existent_file.yaml")

    def test_create_default_config(self):
        """Test creating default config file."""
        with tempfile.NamedTemporaryFile(suffix='.yaml', delete=False) as f:
            temp_path = f.name

        try:
            create_default_config(temp_path)
            assert Path(temp_path).exists()

            # Load and verify
            config = load_config(temp_path)
            assert config.model.name == "ru_core_news_md"
        finally:
            Path(temp_path).unlink()
