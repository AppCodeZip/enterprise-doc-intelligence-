import faiss
import numpy as np

class FAISSStore:
    
    def __init__(self,dim):
        self.index = faiss.IndexFlatL2(dim)
        self.documents = []
        print("FAISSStore calling")

        # dim = embedding dimension (e.g. 384 for MiniLM)
        # IndexFlatL2 = exact nearest-neighbor search using Euclidean distance

    def add(self, embeddings, docs):
        self.index.add(np.array(embeddings).astype("float32")) 
        self.documents.extend(docs)
        # FAISS requires: NumPy array, dtype = float32

    def search(self, query_embedding, top_k=5):
        distances, indices = self.index.search(
            np.array([query_embedding]).astype("float32"), top_k
        )
        results = []
        for idx in indices[0]:
            if idx < len(self.documents):
                results.append(self.documents[idx])
        return results

        # query_embedding → vector of the user question
        # top_k → how many similar results to return
    







# Why FAISS? Why not other vector DBs? Which is the best vector DB?
""" 
🧠 Why do we need a Vector DB at all?
After embeddings, you have this:
[
  [0.12, -0.33, 0.91, ...],   # chunk 0
  [0.44,  0.07, -0.21, ...],  # chunk 1
  ...
]
Now you want to answer:
“Which chunks are most similar to my question?”
That requires:
Fast nearest-neighbor search
On high-dimensional vectors (384–1536 dims)
At scale
A normal SQL DB ❌
A list loop ❌
Vector DB / Vector Index ✅
---------------------------
🔹 Why FAISS? (Your current choice)
FAISS = Facebook AI Similarity Search
What FAISS is best at--
    Extremely fast vector search
    In-memory
    Simple
    Battle-tested
    
✅# Why FAISS is PERFECT for you right now
| Reason            | Explanation         |
| ----------------- | ------------------- |
| Local development | No server needed    |
| Speed             | Blazing fast        |
| Learning RAG      | Minimal abstraction |
| Cost              | Free                |
| Control           | Full ownership      |

faiss.IndexFlatL2(dim)

Your class:--- faiss.IndexFlatL2(dim)
means:
    Exact nearest-neighbor search
    L2 (Euclidean) distance
    No approximation (accurate)
    👉 Best choice for small–medium datasets

---------------------------
🔍 Why not use “other DBs” immediately?

🧱 1️⃣ FAISS (what you’re using)
Pros
✅ Fast
✅ Simple
✅ Offline
✅ Perfect for <1M vectors
✅ Great for research & POCs
Cons
❌ No persistence (unless you save index)
❌ No metadata filtering
❌ Single-machine only
Best for
    Local RAG
    Learning
    Small enterprise docs
    Offline apps
---------------------------
🧠 2️⃣ ChromaDB
Pros
✅ Persistent storage
✅ Built-in metadata filtering
✅ Very popular in LangChain
✅ Easy to use
Cons
❌ Slower than FAISS
❌ Not ideal for very large scale
Best for
    RAG apps
    Medium datasets
    Metadata-heavy retrieval
---------------------------

☁️ 3️⃣ Pinecone (Cloud)
Pros
✅ Fully managed
✅ Auto-scaling
✅ Production-grade
✅ Metadata filtering
Cons
❌ Paid
❌ Internet required
❌ Vendor lock-in
Best for
    Production SaaS
    Large scale
    Teams without infra skills
---------------------------

🐳 4️⃣ Weaviate
Pros
✅ Hybrid search (text + vector)
✅ GraphQL API
✅ Open source + cloud
Cons
❌ More complex
❌ Needs server
Best for
    Advanced search
    Knowledge graphs
---------------------------

🧩 5️⃣ Milvus
Pros
✅ Massive scale
✅ Highly optimized
✅ Open-source
Cons
❌ Heavy
❌ Requires Kubernetes for best use
Best for
    Billions of vectors
    Enterprise infra teams
---------------------------

🧮 6️⃣ Qdrant (🔥 very popular)
Pros
✅ Fast
✅ Persistent
✅ Metadata filtering
✅ Rust-based (very fast)
✅ Open-source
Cons
❌ Requires server (or Docker)
Best for
    Production RAG
    Self-hosted systems
---------------------------

🏆 So… which Vector DB is BEST?
❗ There is no single “best” — it depends on scale & use case
Here’s the practical recommendation 👇

| Stage                    | Best Vector DB     |
| ------------------------ | ------------------ |
| Learning / Local         | **FAISS** ✅        |
| RAG Prototype            | **FAISS / Chroma** |
| Production (Self-hosted) | **Qdrant**         |
| Production (Cloud)       | **Pinecone**       |
| Very Large Scale         | **Milvus**         |

"""