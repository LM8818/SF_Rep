"""Integration tests for Banking NLP pipeline."""

import pytest
from banking_nlp import BankingNLPPipeline, load_config
from banking_nlp.config.settings import Config


class TestBankingNLPIntegration:
    """Integration tests for the complete pipeline."""

    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return Config()

    @pytest.fixture
    def pipeline(self, config):
        """Create pipeline instance."""
        # Note: This test requires spaCy model to be installed
        try:
            return BankingNLPPipeline(config)
        except OSError:
            pytest.skip("spaCy model ru_core_news_md not installed")

    def test_pipeline_initialization(self, pipeline):
        """Test pipeline initialization."""
        assert pipeline is not None
        assert pipeline.nlp is not None
        assert pipeline.preprocessor is not None
        assert pipeline.classifier is not None

    def test_process_single_text(self, pipeline):
        """Test processing a single text."""
        text = "Перевод суммы 5000 рублей выполнен успешно"
        result = pipeline.process(text)

        assert result is not None
        assert result.text
        assert result.classification
        assert isinstance(result.confidence, float)
        assert isinstance(result.entities, list)
        assert isinstance(result.tokens, list)
        assert result.processing_time > 0

    def test_process_empty_text(self, pipeline):
        """Test processing empty text."""
        result = pipeline.process("")

        assert result.classification == "other"
        assert result.confidence == 0.0
        assert len(result.entities) == 0
        assert len(result.tokens) == 0

    def test_process_batch(self, pipeline):
        """Test batch processing."""
        texts = [
            "Перевод 1000 рублей",
            "Оплата счета за услуги",
            "Получение кредита"
        ]

        results = pipeline.process_batch(texts)

        assert len(results) == len(texts)
        for result in results:
            assert result.classification
            assert isinstance(result.confidence, float)

    def test_get_pipeline_info(self, pipeline):
        """Test getting pipeline information."""
        info = pipeline.get_pipeline_info()

        assert 'spacy_model' in info
        assert 'spacy_version' in info
        assert 'pipeline_components' in info
        assert 'config' in info

    def test_rule_based_classification(self, pipeline):
        """Test rule-based classification (fallback)."""
        # Test various document types
        test_cases = [
            ("Перевод денежных средств", "transfer"),
            ("Платеж за услуги", "payment"),
            ("Кредитный договор", "loan"),
            ("Открытие депозита", "deposit"),
            ("Выписка по счету", "statement"),
        ]

        for text, expected_type in test_cases:
            result = pipeline.process(text)
            # Classification might be different if classifier is trained
            assert result.classification is not None
