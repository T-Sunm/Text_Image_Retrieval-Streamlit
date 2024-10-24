from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
import numpy as np

def get_single_image_embeddings(image):
  embedding_function = OpenCLIPEmbeddingFunction()
  embedding_img = embedding_function._encode_image(image=image)
  return np.array(embedding_img)
