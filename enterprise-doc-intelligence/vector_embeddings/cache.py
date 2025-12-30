#  Why Use Embedding Cache?

""" The embedding cache is used primarily to save and reuse embeddings that have already been generated, 
so that you don’t need to compute the same embeddings repeatedly. 
This approach offers several key benefits:

Reduce Computation Cost:
Faster Response Time:
Consistency-By caching the embeddings, you ensure that for the same input text, the output embedding is always the same.
Persistent Storage:The cache is saved to a file (e.g., embeddings_cache.pkl), so even if the program is restarted, previously computed embeddings can still be accessed.
"""


import hashlib
# generate a unique hash value for each text input or document, 
# which can then be stored or used as a key for caching or database lookups.
import pickle 
# You might use pickle to save embeddings 
# or other preprocessed data so that you don't need to recompute them every time you run your program.
import os


CACHE_PATH = "embeddings_cache.pkl"

class EmbeddingCache:
    def __init__(self):
        if os.path.exists(CACHE_PATH):
            with open(CACHE_PATH, "rb") as f:
                self.cache = pickle.load(f)
        else:
            self.cache = {}

    def _hash(self, text):
        return hashlib.md5(text.encode()).hexdigest()

    def get(self, text):
        return self.cache.get(self._hash(text))

    def set(self, text, embedding):
        self.cache[self._hash(text)] = embedding
        with open(CACHE_PATH, "wb") as f:
            pickle.dump(self.cache, f)