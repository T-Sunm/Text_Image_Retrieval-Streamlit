from utils.initialize_models import init_image_retrieval
import json
from utils.preprocessing.image_embedding import get_single_image_embeddings
import numpy as np
from PIL import Image
import io

def image_query(file_content):
  collection = init_image_retrieval()
  image = Image.open(io.BytesIO(file_content))
  query = np.array(image).astype(np.uint8)

  embeddings = get_single_image_embeddings(query)
  results = collection.query(
      query_embeddings=[embeddings.tolist()], n_results=5, include=["distances"])

  return results
