def chunk_text_1(text,chunk_size=800,overlap= 150):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length :
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        # Prevent infinite loop
        if end >= text_length:
            break

        start = end - overlap

    return chunks

# 🔥 Improved chunk_text (newline-aware)
def chunk_text(text, chunk_size=800, overlap=150):
    if not text:
        return []

    paragraphs = text.split("\n")
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        if len(current_chunk) + len(para) <= chunk_size:
            current_chunk += para + "\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para + "\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def chunk_documents(pages):
    chunked_docs = []
    for page in pages:
        chunks = chunk_text(page["text"])
        for i, chunk in enumerate(chunks):
            chunked_docs.append({
                "text": chunk,
                "metadata": {
                    **page["metadata"],
                    "chunk": i
                }
            })
        # print("chunked_docs=====", chunked_docs)
    return chunked_docs