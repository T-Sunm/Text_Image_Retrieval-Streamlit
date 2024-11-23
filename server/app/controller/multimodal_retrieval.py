from utils.initialize_models import init_text_retrieval_img
import json
from utils.preprocessing.text_embedding import get_single_text_embedding_multimodal


def text_retrieval_img_query(str):
  collection = init_text_retrieval_img()
  embedding = get_single_text_embedding_multimodal(str)

  results = collection.query(
      query_embeddings=embedding,
      n_results=5,
      include=['metadatas', 'distances']
  )
  return results

def img_retrieval_text_query(str):
  collection = init_text_retrieval_img()
  embedding = get_single_text_embedding_multimodal(str)

  results = collection.query(
      query_embeddings=embedding,
      n_results=5,
      include=['metadatas', 'distances']
  )
  return results
