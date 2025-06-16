"""Tests for text preprocessor."""

import pytest
from banking_nlp.data.preprocessor import TextPreprocessor
from banking_nlp.config.settings import ProcessingConfig


class TestTextPreprocessor:
    """Test text preprocessing functionality."""

    @pytest.fixture
    def preprocessor(self):
        """Create preprocessor with default config."""
        config = ProcessingConfig()
        return TextPreprocessor(config)

    @pytest.fixture
    def preprocessor_no_lowercase(self):
        """Create preprocessor without lowercasing."""
        config = ProcessingConfig(lowercase=False)
        return TextPreprocessor(config)

    def test_clean_text(self, preprocessor):
        """Test basic text cleaning."""
        text = "  Test   text\nwith\textra\rspaces  "
        cleaned = preprocessor.clean_text(text)
        assert cleaned == "Test text with extra spaces"

    def test_clean_text_empty(self, preprocessor):
        """Test cleaning empty text."""
        assert preprocessor.clean_text("") == ""
        assert preprocessor.clean_text("   ") == ""

    def test_extract_numbers(self, preprocessor):
        """Test number extraction."""
        text = "Сумма 1 500.50 рублей и 2,000 долларов"
        numbers = preprocessor.extract_numbers(text)
        assert len(numbers) >= 1  # Should find formatted numbers

    def test_extract_dates(self, preprocessor):
        """Test date extraction."""
        text = "Дата: 15.06.2025, также 01/12/2024 и 2025-12-31"
        dates = preprocessor.extract_dates(text)
        assert len(dates) >= 2

    def test_preprocess_text_lowercase(self, preprocessor):
        """Test text preprocessing with lowercase."""
        text = "TEST Text"
        result = preprocessor.preprocess_text(text)
        assert result.islower()

    def test_preprocess_text_no_lowercase(self, preprocessor_no_lowercase):
        """Test text preprocessing without lowercase."""
        text = "TEST Text"
        result = preprocessor_no_lowercase.preprocess_text(text)
        assert "TEST" in result  # Case should be preserved

    def test_extract_features(self, preprocessor):
        """Test feature extraction."""
        text = "Перевод 5000 рублей на счет 12345 от 15.06.2025"
        features = preprocessor.extract_features(text)

        assert features['char_count'] > 0
        assert features['word_count'] > 0
        assert features['has_currency'] is True
        assert features['has_account'] is True
        assert len(features['numbers']) > 0

    def test_stopwords_property(self, preprocessor):
        """Test stopwords property."""
        stopwords = preprocessor.stopwords
        assert isinstance(stopwords, set)
        assert 'и' in stopwords
        assert 'на' in stopwords
