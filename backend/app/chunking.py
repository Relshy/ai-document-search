DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200


def chunk_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be non-negative and smaller than chunk_size")

    words = text.split()
    if not words:
        return []

    chunks = []
    start = 0
    while start < len(words):
        end = start + _word_count_for_chunk(words, start, chunk_size)
        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        if end >= len(words):
            break

        start = _word_count_for_chunk(words, start, chunk_size - chunk_overlap) + start

    return chunks


def _word_count_for_chunk(words: list[str], start: int, max_characters: int) -> int:
    length = 0
    count = 0
    for word in words[start:]:
        added_length = len(word) if count == 0 else length + 1 + len(word)
        if added_length > max_characters and count > 0:
            break
        length = added_length
        count += 1
    return count
