# 1. Create a virtual environment
python3 -m venv .venv

# 2. Activate it
source .venv/bin/activate

# Create your first Python file
touch main.py

# 3. Upgrade pip (optional but recommended)
pip install --upgrade pip


enterprise-doc-intelligence/
│
├── ingestion/
│   ├── loaders.py
│   ├── chunker.py
│
├── embeddings/
│   ├── embedder.py
│   ├── cache.py
│
├── vectorstore/
│   ├── faiss_store.py
│
├── rag/
│   ├── retriever.py
│   ├── prompt.py
│   ├── qa_chain.py
│
├── api/
│   ├── main.py
│
├── data/
│   ├── uploads/
│
├── README.md


# Code format
black your_file.py

# update library 
pip install -r requirements.txt
