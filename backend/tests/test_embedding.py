from unittest.mock import MagicMock, patch

from app.embedding import EmbeddingModel, embed_query, get_embedding_model


def test_embed_returns_vector_per_chunk() -> None:
    fake_model = MagicMock()
    fake_model.encode.return_value.tolist.return_value = [[0.1, 0.2], [0.3, 0.4]]

    with patch("sentence_transformers.SentenceTransformer", return_value=fake_model):
        embedding_model = EmbeddingModel()
        vectors = embedding_model.embed(["first chunk", "second chunk"])

    assert vectors == [[0.1, 0.2], [0.3, 0.4]]
    fake_model.encode.assert_called_once_with(
        ["first chunk", "second chunk"], convert_to_numpy=True
    )


def test_embed_returns_empty_list_for_no_chunks() -> None:
    fake_model = MagicMock()

    with patch("sentence_transformers.SentenceTransformer", return_value=fake_model):
        embedding_model = EmbeddingModel()
        vectors = embedding_model.embed([])

    assert vectors == []
    fake_model.encode.assert_not_called()


def test_get_embedding_model_is_cached() -> None:
    get_embedding_model.cache_clear()
    fake_model = MagicMock()

    with patch("sentence_transformers.SentenceTransformer", return_value=fake_model):
        first = get_embedding_model()
        second = get_embedding_model()

    assert first is second
    get_embedding_model.cache_clear()


def test_embed_query_returns_single_vector() -> None:
    get_embedding_model.cache_clear()
    fake_model = MagicMock()
    fake_model.encode.return_value.tolist.return_value = [[0.1, 0.2]]

    with patch("sentence_transformers.SentenceTransformer", return_value=fake_model):
        vector = embed_query("what is this document about?")

    assert vector == [0.1, 0.2]
    get_embedding_model.cache_clear()
