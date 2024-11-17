import streamlit as st
from utils.resetquery import reset_query
from utils.rw_image_cache import get_image_cache

def init_image_retrieval():

  files_path = get_image_cache()
# ------- init state
  if 'open_state' not in st.session_state:
    st.session_state.open_state = None
  if 'last_state' not in st.session_state:
    st.session_state.last_state = None

  return (files_path)
