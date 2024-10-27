# retrieval_models.py
import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
from chromadb.utils import embedding_functions
import os
def init_image_retrieval():
  # Đường dẫn đến thư mục chứa file Python hiện tại
  project_root = os.path.abspath(
      os.path.join(os.path.dirname(__file__), "..", ".."))
  db_path = os.path.join(project_root, "database", "database_image")
  print(db_path)
  try:
    image_loader = ImageLoader()
    client = chromadb.PersistentClient(path=db_path)
    embedding_function = OpenCLIPEmbeddingFunction()
    collection = client.get_or_create_collection(
        name='image_collection',
        embedding_function=embedding_function,
        data_loader=image_loader,
        metadata={"hnsw:space": "cosine"}
    )
    print("Image retrieval model initialized successfully!")
    return collection
  except Exception as e:
    print(f"Failed to initialize image retrieval model: {e}")
    return None

def init_text_retrieval():
  project_root = os.path.abspath(
      os.path.join(os.path.dirname(__file__), "..", ".."))
  db_path = os.path.join(project_root, "database", "database_text")
  try:
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path=db_path)
    collection_text = client.get_or_create_collection(
        name='text_collection',
        embedding_function=embedding_function,
        metadata={"hnsw:space": "cosine"}
    )
    print("Text retrieval model initialized successfully!")
    return collection_text
  except Exception as e:
    print(f"Failed to initialize text retrieval model: {e}")
    return None

def init_text_retrieval_advance():
  project_root = os.path.abspath(
      os.path.join(os.path.dirname(__file__), "..", ".."))
  db_path = os.path.join(project_root, "database", "database_text_advance")
  try:
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path=db_path)
    collection_text_advance = client.get_or_create_collection(
        name='text_collection_advance',
        embedding_function=embedding_function,
        metadata={"hnsw:space": "cosine"}
    )
    print("Advanced text retrieval model initialized successfully!")
    return collection_text_advance
  except Exception as e:
    print(f"Failed to initialize advanced text retrieval model: {e}")
    return None
