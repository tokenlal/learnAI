def chunk_text(text: str, chunk_size: int = 500, overlap: int = 0):
    chunks = []
    start = 0
    text_length = len(text)
    while start < text_length:
        chunk = text[start:start + chunk_size]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks
