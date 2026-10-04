from __future__ import annotations
from uuid import UUID

class ChunkService:
    def __init__(self, chunk_size: int = 1200, overlap: int = 200) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero.")

        if overlap < 0:
            raise ValueError("overlap cannot be negative.")

        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size.")

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, *, document_id: UUID, text: str) -> list[dict]:
        if not text:
            return []

        chunks: list[dict] = []

        start = 0
        chunk_index = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))

            chunks.append(
                {
                    "document_id": str(document_id),
                    "chunk_index": chunk_index,
                    "text": text[start:end],
                }
            )

            chunk_index += 1

            if end >= len(text):
                break

            start = end - self.overlap

        return chunks