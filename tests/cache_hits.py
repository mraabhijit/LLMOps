import time
from pipeline.embeddings import get_embedding_model

model = get_embedding_model()

# Run 1
start = time.time()
model.embed_query("chicken")
print(f"Run 1: {(time.time() - start) * 1000:.2f}ms")

# Run 2 (Should be near 0ms if cached)
start = time.time()
model.embed_query("chicken")
print(f"Run 2: {(time.time() - start) * 1000:.2f}ms")
