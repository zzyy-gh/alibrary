import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestBuildEmbedText:
    def test_all_fields(self):
        from embeddings import _build_embed_text
        result = _build_embed_text({"title": "T", "summary": "S"}, "Body")
        assert result == "T\nS\nBody"

    def test_no_title(self):
        from embeddings import _build_embed_text
        result = _build_embed_text({}, "Body")
        assert result == "Body"

    def test_no_summary(self):
        from embeddings import _build_embed_text
        result = _build_embed_text({"title": "T"}, "Body")
        assert result == "T\nBody"


class TestGetProvider:
    @patch.dict("os.environ", {"EMBEDDING_PROVIDER": "gemini"})
    def test_gemini(self):
        from embeddings import _get_provider
        assert _get_provider() == "gemini"

    @patch.dict("os.environ", {"EMBEDDING_PROVIDER": "openai"})
    def test_openai(self):
        from embeddings import _get_provider
        assert _get_provider() == "openai"

    @patch.dict("os.environ", {"EMBEDDING_PROVIDER": "bogus"})
    def test_invalid(self):
        from embeddings import _get_provider
        with pytest.raises(SystemExit):
            _get_provider()


class TestGenerateEmbedding:
    @patch.dict("os.environ", {"EMBEDDING_PROVIDER": "gemini"})
    def test_dispatches_to_gemini(self):
        import embeddings
        mock_fn = MagicMock(return_value=[0.1] * 768)
        with patch.dict(embeddings.PROVIDERS, {"gemini": mock_fn}):
            result = embeddings.generate_embedding("test text")
        mock_fn.assert_called_once_with("test text")
        assert len(result) == 768

    @patch.dict("os.environ", {"EMBEDDING_PROVIDER": "openai"})
    def test_dispatches_to_openai(self):
        import embeddings
        mock_fn = MagicMock(return_value=[0.2] * 1536)
        with patch.dict(embeddings.PROVIDERS, {"openai": mock_fn}):
            result = embeddings.generate_embedding("test text")
        mock_fn.assert_called_once_with("test text")
        assert len(result) == 1536


class TestSearchSimilar:
    @patch("embeddings.generate_embedding", return_value=[0.1] * 768)
    @patch("embeddings._get_chroma_collection")
    def test_returns_ids_and_scores(self, mock_collection_fn, mock_embed):
        mock_collection = MagicMock()
        mock_collection.query.return_value = {
            "ids": [["id1", "id2"]],
            "distances": [[0.3, 0.7]],
        }
        mock_collection_fn.return_value = mock_collection

        from embeddings import search_similar
        results = search_similar("query", n_results=5)
        assert len(results) == 2
        assert results[0]["id"] == "id1"
        assert results[0]["relevance_score"] == pytest.approx(0.7)
        assert results[1]["relevance_score"] == pytest.approx(0.3)

    @patch("embeddings.generate_embedding", return_value=[0.1] * 768)
    @patch("embeddings._get_chroma_collection")
    def test_empty_collection(self, mock_collection_fn, mock_embed):
        mock_collection = MagicMock()
        mock_collection.query.side_effect = Exception("empty")
        mock_collection_fn.return_value = mock_collection

        from embeddings import search_similar
        results = search_similar("query")
        assert results == []
