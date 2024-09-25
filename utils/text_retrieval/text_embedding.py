from chromadb.utils import embedding_functions
import numpy as np
def get_single_text_embeddings(text: str):
  embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
      model_name="all-MiniLM-L6-v2", normalize_embeddings=True,)

  embedding_text = embedding_function([text])[0]
  return np.array(embedding_text)
