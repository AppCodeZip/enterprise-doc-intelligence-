# Why Use Embedding Generator?

# The Embedding Generator is responsible for converting raw text data into 
# dense vector representations (embeddings) that can be used for downstream 
# tasks like semantic search, clustering, classification, or recommendations. 
# Here's why it's important:

# Convert Text into Numerical Form:
# Text data, which is inherently unstructured, needs to be converted into 
# a structured numerical format so that machine learning algorithms can process it. 
# Embeddings serve this purpose, representing the meaning of text in a form 
# that algorithms can work with.

# Model Efficiency:===
# The use of pre-trained models like SentenceTransformer (which is based on 
# BERT or similar architectures) helps in generating high-quality embeddings 
# efficiently. These models capture the semantic meaning of text, which makes 
# them useful for a wide range of NLP tasks.

# Handling Large Texts:====
# Models like the one used in the Embedder (all-MiniLM-L6-v2) are specifically 
# optimized for processing larger sets of texts quickly and generating embeddings 
# in a consistent manner.

# Optimization:===
# The Embedder class integrates with the caching mechanism to avoid recalculating 
# embeddings for the same text, improving overall performance in real-world applications.



# Alternatives/Other Techniques for Embedding Generation:====>

# Other Embedding Models:
'''Instead of using SentenceTransformer, other models like OpenAI's GPT, T5, 
BERT, or FastText could be used depending on your application and the 
trade-offs in terms of quality and speed.

1-GloVe (Global Vectors for Word Representation)-:Use case: When you need fast and lightweight embeddings for word-level tasks, 
such as text classification with limited resources. import numpy as np
2-FastText (facebook)-:When you need faster embedding generation or you're working with limited resources and don't require the full semantic richness of transformer models.
3. SentenceTransformers (based on BERT, RoBERTa, etc.):-Use case: When you need high-quality semantic representations for tasks like search, clustering, and ranking.
4. BERT (directly using Hugging Face Transformers):-Use case: When you need contextualized word or sentence embeddings, and you're fine with trading off speed for qu
'''

# Lazy Embedding Generation:
'''Instead of immediately generating embeddings for all texts, you could 
implement a lazy approach where embeddings are generated only when required. 
This way, you don't store embeddings for texts that are never queried again.'''

# Dimensionality Reduction:
'''If the embeddings are too large, you could use techniques like PCA 
(Principal Component Analysis) or t-SNE to reduce their dimensionality 
before storing them, optimizing both storage and retrieval performance.'''

from sentence_transformers import SentenceTransformer
from vector_embeddings.cache import EmbeddingCache


class Embedder:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.cache = EmbeddingCache()

    def embed(self, texts):
        embeddings = []
        for text in texts:
            cached = self.cache.get(text)
            if cached is not None:
                embeddings.append(cached)
            else:
                emb = self.model.encode(text)
                self.cache.set(text, emb)
                embeddings.append(emb)
        return embeddings
