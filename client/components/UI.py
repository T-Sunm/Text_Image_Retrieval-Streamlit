import streamlit as st
from PIL import Image
import numpy as np
from server.create_db.images.preprocessing.image_embedding import get_single_image_embeddings
import json
from PIL import Image


def display_header(content: str):
  st.markdown(f'''
        <div style="text-align: center;">
            <h1>
              {content}
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


def display_result(results, is_image=False, is_text=False):
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

    for i, res in enumerate(results):
      col = result_cols[i % 3]
      col.markdown(f"""
      <span style="color:white;background-color:{colors[i]};padding:5px;border-radius:5px;">Rank {i + 1}</span>
      """, unsafe_allow_html=True)
      if is_image == True:
        col.image(res, use_column_width=True)

      if is_text == True:
        col.write(res)

      col.divider()


def display_result_text(results: list):
  if results:
    colors = ['orange', 'green', 'red', 'gray', 'blue']

    # Tạo một container có chiều cao cố định
    with st.container(height=600):
      for i, res in enumerate(results):
        print(res)
        st.markdown(f"""
                <div style="margin-bottom: 20px;">
                    <span class="result-rank" style="background-color:{colors[i % len(colors)]}; padding: 5px 10px; padding-horizontal: 10px; border-radius: 5px; margin-bottom:5px; display: inline-block;">
                        Rank {i + 1}
                    </span>
                    <div class="result-text" style="border: 1px solid #888888; color: black; padding: 15px; height: 200px; width: 100%; border-radius: 5px; ">
                        {res}
                    </div>
                </div>
                """, unsafe_allow_html=True)

def display_text_results_advance(texts_result):
  documents = []
  for doc in texts_result['documents'][0]:
    document = json.loads(doc)
    formatted_doc = {
        "query_id": document['query_id'],
        "title": document['answer'][0],
        "content": document['relevant_docs']
    }
    documents.append(formatted_doc)

  colors = ['orange', 'green', 'red', 'gray', 'blue']

  # Tạo cột
  col1, col2 = st.columns([3, 5])

  with col1:
    for i, doc in enumerate(documents):
      # Hiển thị tiêu đề như markdown với giao diện tùy chỉnh
      st.markdown(
          f"""
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
                    <span style="
                        display: inline-block;
                        padding: 3px 8px;
                        border-radius: 12px;
                        font-size: 12px;
                        color: white;
                        background-color: {colors[i % len(colors)]};
                        vertical-align: middle;">Rank {i + 1}
                    </span>
                    <div style="
                        display: inline-block;
                        padding: 10px;
                        width: 200px;
                        border: 1px solid black;
                        border-radius: 5px;
                        text-align: center;
                        white-space: nowrap;
                        overflow: hidden;
                        text-overflow: ellipsis;">{doc['title']}
                    </div>
                </div>
                """, unsafe_allow_html=True
      )
      # Căn giữa nút 'Choose' bằng cách đặt nó vào một `st.columns()` khác
      button_col1, button_col2, button_col3, button_col4 = st.columns([
                                                                      0.5, 0.5, 1, 0.5])
      with button_col3:  # Căn giữa nút 'Choose'
        if st.button("Choose", key=f"button_{i}"):
          st.session_state.selected_document = {
              "title": doc["title"], "document_relevant": doc["content"]}

      # Thêm ngăn cách giữa các nút
      st.markdown('<hr style="margin: 5px 0;">', unsafe_allow_html=True)

  # Cột bên phải: hiển thị nội dung chi tiết của tài liệu được chọn

  with col2:
    st.markdown(
        f"""
    <div style="margin-bottom: 20px;">
        <strong>Answer</strong> <span style="font-weight: normal;">{st.session_state.selected_document['title']}</span>
    </div>
    """,
        unsafe_allow_html=True
    )
    if "selected_document" in st.session_state and isinstance(st.session_state.selected_document, dict):
      with st.container(height=600):
        for i, doc in enumerate(st.session_state.selected_document['document_relevant']):
          st.markdown(f"#### **Relevant document {i + 1}**")
          st.write(doc)
          st.markdown("---")

    else:
      st.write("Please select a document to view the content.")


def display_search_button_retrievaltext():
  pass
