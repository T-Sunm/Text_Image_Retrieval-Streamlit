import streamlit as st
import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
from utils.resetquery import reset_query
from utils.get_files_path import get_image_cache
from utils.text_retrieval.rw_text_cache import get_text_cache
from chromadb.utils import embedding_functions
def init_image_retrieval():
  db_path = r"D:\Asus\AIO\Project\Text_Image_Retrieval-Streamlit\database\database_image"

  image_loader = ImageLoader()
  client = chromadb.PersistentClient(path=db_path)
  embedding_function = OpenCLIPEmbeddingFunction()
  collection = client.get_or_create_collection(
      name='multimodal_collection',
      embedding_function=embedding_function,
      data_loader=image_loader,
      metadata={"hnsw:space": "cosine"}
  )
  files_path = get_image_cache()
# ------- init state
  if 'open_state' not in st.session_state:
    st.session_state.open_state = None
  if 'last_state' not in st.session_state:
    st.session_state.last_state = None

  return (collection, files_path)


def init_text_retrieval():
  db_path = r"D:\Asus\AIO\Project\Text_Image_Retrieval-Streamlit\database\database_text"

  embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
      model_name="all-MiniLM-L6-v2")
  client = chromadb.PersistentClient(path=db_path)

  collection_text = client.get_or_create_collection(
      name='text_collection',
      embedding_function=embedding_function,
      metadata={"hnsw:space": "cosine"}
  )

  corpus = get_text_cache()

  # ------- init state
  if 'query' not in st.session_state:
    st.session_state.query = 0

  return (collection_text, corpus)


def init_text_retrieval_advance():
  db_path = r"D:\Asus\AIO\Project\Text_Image_Retrieval-Streamlit\database\database_text_advance"

  embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
      model_name="all-MiniLM-L6-v2")
  client = chromadb.PersistentClient(path=db_path)

  collection_text = client.get_or_create_collection(
      name='text_collection_advance',
      embedding_function=embedding_function,
      metadata={"hnsw:space": "cosine"}
  )

  # ------- init state
  if 'query' not in st.session_state:
    st.session_state.query = 0

  return collection_text
