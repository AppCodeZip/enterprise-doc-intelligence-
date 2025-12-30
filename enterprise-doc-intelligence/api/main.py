""" import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from ingestion.loaders import load_document
from ingestion.chunker import chunk_documents
from vector_embeddings.embedder import Embedder
from vectorstore.faiss_store import FAISSStore
from rag.retriever import Retriever
from rag.qa_chain import QAChain



if __name__ == "__main__":
    print("🚀 App started")
    file_path = "/Users/skumar/Downloads/Holiday Calendar List.pdf"  # Replace with the path to your file
    try:
        # 1️⃣ Load document
        pages = load_document(file_path)
        # for doc in pages:
        #     print(doc["text"])  # This will print the extracted text
            
        print(f"Loaded {len(pages)} pages")

        # 2️⃣ Chunk document
        print("Chunking document...")
        chunked_docs = chunk_documents(pages)
        print(f"🧩 Created {len(chunked_docs)} chunks")


        # Print first chunk as a sanity check
        # print("\nSample Chunk:\n")
        # print(chunked_docs[0]["text"])
        # print("\nchunked_docs:\n",chunked_docs[0]["metadata"])

        # 3️⃣ Generate embeddings
        print("Generating embeddings...")
        texts = [doc["text"] for doc in chunked_docs]
        embedder = Embedder()
        embeddings = embedder.embed(texts)
        print(f"Generated {len(embeddings)} embeddings")

        # DEBUG: embedding dimension
        dim = len(embeddings[0])
        print("\ndim result--:", dim)

        # 4️⃣ Store in FAISS
        vector_store = FAISSStore(dim)
        vector_store.add(embeddings, chunked_docs)
        print("📦 Stored embeddings in FAISS")



        # 5️⃣ Create retriever
        retriever = Retriever(embedder, vector_store)

        # 6️⃣ Ask a question
        question = "What are the mandatory holidays in Hyderabad?"
        print(f"\n❓ Question: {question}")

        context_docs = retriever.retrieve(question, top_k=3)
        print(f"🔎 Retrieved {len(context_docs)} relevant chunks")

        # 7️⃣ Run QA Chain (LLM call)
        qa_chain = QAChain()
        response = qa_chain.run(context_docs, question)

        # 8️⃣ Print answer
        print("\n🧠 Answer:")
        print(response["answer"])

        print("\n📚 Sources:")
        for src in response["sources"]:
            print("-", src)

    except Exception as e:
        print(f"Error: {e}")

        """




# FastAPI Backend Implement------

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

from ingestion.loaders import load_document
from ingestion.chunker import chunk_documents
from vector_embeddings.embedder import Embedder
from vectorstore.faiss_store import FAISSStore
from rag.retriever import Retriever
from rag.qa_chain import QAChain

from fastapi.responses import StreamingResponse


# ------------------------
# App Initialization
# ------------------------
app = FastAPI(title="Enterprise Document Intelligence")

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ------------------------
# Global Objects (Loaded Once)
# ------------------------
embedder = Embedder()
vector_store = None
retriever = None
qa_chain = QAChain()

# ------------------------
# Health Check
# ------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# ------------------------
# Upload & Index Document
# ------------------------
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    global vector_store, retriever

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 1️⃣ Load document
    pages = load_document(file_path)

    # 2️⃣ Chunk document
    chunked_docs = chunk_documents(pages)

    # 3️⃣ Generate embeddings
    texts = [doc["text"] for doc in chunked_docs]
    embeddings = embedder.embed(texts)

    # 4️⃣ Create FAISS store (only once)
    if vector_store is None:
        dim = len(embeddings[0])
        vector_store = FAISSStore(dim)

    vector_store.add(embeddings, chunked_docs)

    # 5️⃣ Create retriever
    retriever = Retriever(embedder, vector_store)

    return {
        "message": "Document indexed successfully",
        "pages": len(pages),
        "chunks": len(chunked_docs)
    }

# ------------------------
# Query Documents
# ------------------------
@app.post("/query")
async def query_document(question: str, top_k: int = 3):
    if retriever is None:
        return JSONResponse(
            status_code=400,
            content={"error": "No documents indexed yet"}
        )

    # 6️⃣ Retrieve relevant chunks
    context_docs = retriever.retrieve(question, top_k=top_k)

    if not context_docs:
        return {
            "answer": "I don't have enough information from the documents.",
            "sources": []
        }

    # 7️⃣ Run QA Chain
    response = qa_chain.run(context_docs, question)

    return response

# Implement Stream------
@app.post(
    "/query/stream",
    summary="Stream LLM response token-by-token",
    description="Streams the answer as it is generated by the LLM"
)
async def query_stream(question: str, top_k: int = 3):

    if not question.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Question cannot be empty"}
        )

    if retriever is None:
        return JSONResponse(
            status_code=400,
            content={"error": "No documents indexed yet"}
        )

    context_docs = retriever.retrieve(question, top_k=top_k)

    if not context_docs:
        return StreamingResponse(
            iter(["I don't have enough information from the documents."]),
            media_type="text/plain"
        )

    def token_generator():
        try:
            for token in qa_chain.run_stream(context_docs, question):
                yield token
        except Exception:
            yield "\n[ERROR] LLM generation failed."

    return StreamingResponse(
        token_generator(),
        media_type="text/plain"
    )



# uvicorn api.main:app --reload