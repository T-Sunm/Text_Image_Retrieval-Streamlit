import streamlit as st
import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
from utils.resetquery import reset_query
from utils.get_files_path import get_files_path

def init():
  db_path = r"D:\Asus\AIO\Project\Text_Image_Retrieval-Streamlit\database"
  folderdata_path = r"D:\Asus\AIO\Project\Text_Image_Retrieval-Streamlit\data\train"
  image_loader = ImageLoader()
  client = chromadb.PersistentClient(path=db_path)
  embedding_function = OpenCLIPEmbeddingFunction()
  collection = client.get_or_create_collection(
      name='multimodal_collection',
      embedding_function=embedding_function,
      data_loader=image_loader
  )
  files_path = get_files_path(folder_path=folderdata_path)
# ------- init state
  if 'open_state' not in st.session_state:
    st.session_state.open_state = None
  if 'last_state' not in st.session_state:
    st.session_state.last_state = None

  return (collection, files_path)
