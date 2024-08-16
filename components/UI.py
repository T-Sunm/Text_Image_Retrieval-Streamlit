import streamlit as st
from PIL import Image
import numpy as np
from utils.image_embedding import get_single_image_embeddings
from utils.get_files_path import get_files_paths_by_ids
from PIL import Image
def display_header():
  st.markdown('''
        <div style="text-align: center;">
            <h1>
                CONTENT BASED IMAGE RETRIEVAL
            </h1>
        </div>
    ''', unsafe_allow_html=True)


def display_search_button():
    # Tạo 2 cột để chứa nút và căn giữa chúng
  _, col2, _ = st.columns([1, 2, 1])

  with col2:
      # Tạo 2 nút
    button1, button2 = st.columns(2)

    with button1:
      if st.button('IMAGE SEARCH'):
        st.session_state.open_state = 'search_image'
    with button2:
      if st.button('TEXT SEARCH'):
        st.session_state.open_state = 'search_text'

def search_input():
  if st.session_state.open_state == "search_text":
    st.session_state.query = st.text_input("Enter your search query:")
  elif st.session_state.open_state == "search_image":
    query = st.file_uploader(
        "Choose an image", type=['jpg', 'png', 'jpeg'])
    if query is not None:  # Ensure a file is uploaded before processing
      image = Image.open(query)
      query = np.array(image).astype(np.uint8)
      st.session_state.query = get_single_image_embeddings(query)
      st.image(image, caption='Uploaded Image.')


def display_result(results, files_path):
    #
    # Giả sử bạn có 6 ảnh, và bạn muốn sắp xếp chúng vào 3 cột:
    # Ảnh 1 (i=0): 0 % 3 = 0 (cột 1)
    # Ảnh 2 (i=1): 1 % 3 = 1 (cột 2)
    # Ảnh 3 (i=2): 2 % 3 = 2 (cột 3)
    # Ảnh 4 (i=3): 3 % 3 = 0 (cột 1)
    # Ảnh 5 (i=4): 4 % 3 = 1 (cột 2)
    # Ảnh 6 (i=5): 5 % 3 = 2 (cột 3)
    #
  if results is not None:
    colors = ['orange', 'green', 'red', 'gray', 'blue']

    result_cols = st.columns(3)
    files_path_results = get_files_paths_by_ids(
        files_path, results['ids'][0])
    for i, image_path in enumerate(files_path_results):
      col = result_cols[i % 3]
      col.markdown(f"""
      <span style="color:white;background-color:{colors[i]};padding:5px;border-radius:5px;">Rank {i + 1}</span>  
      """, unsafe_allow_html=True)
      col.image(image_path, use_column_width=True)
      col.divider()
