import os
from functools import lru_cache

import psycopg
from pgvector.psycopg import register_vector

EMBEDDING_DIMENSION = 384


def get_database_url() -> str:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable is not set")
    return database_url


@lru_cache(maxsize=1)
def get_connection() -> psycopg.Connection:
    connection = psycopg.connect(get_database_url(), autocommit=True)
    connection.execute("CREATE EXTENSION IF NOT EXISTS vector")
    register_vector(connection)
    _create_schema(connection)
    return connection


def _create_schema(connection: psycopg.Connection) -> None:
    connection.execute(
        f"""
        CREATE TABLE IF NOT EXISTS document_chunks (
            id SERIAL PRIMARY KEY,
            filename TEXT NOT NULL,
            content TEXT NOT NULL,
            embedding VECTOR({EMBEDDING_DIMENSION}) NOT NULL
        )
        """
    )


def store_chunks(filename: str, chunks: list[str], embeddings: list[list[float]]) -> None:
    if len(chunks) != len(embeddings):
        raise ValueError("chunks and embeddings must have the same length")
    if not chunks:
        return

    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.executemany(
            "INSERT INTO document_chunks (filename, content, embedding) VALUES (%s, %s, %s)",
            [(filename, chunk, embedding) for chunk, embedding in zip(chunks, embeddings)],
        )
