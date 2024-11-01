import streamlit as st
import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
from utils.resetquery import reset_query
from utils.get_data_in_caches import get_image_cache
from utils.get_data_in_caches import get_text_cache
from chromadb.utils import embedding_functions
def init_image_retrieval():

  files_path = get_image_cache()
# ------- init state
  if 'open_state' not in st.session_state:
    st.session_state.open_state = None
  if 'last_state' not in st.session_state:
    st.session_state.last_state = None

  return (files_path)


def init_text_retrieval():

  corpus = get_text_cache()

  # ------- init state
  if 'query' not in st.session_state:
    st.session_state.query = 0

  return (corpus)


def init_text_retrieval_advance():

  # ------- init state
  if 'query' not in st.session_state:
    st.session_state.query = 0

  pass
