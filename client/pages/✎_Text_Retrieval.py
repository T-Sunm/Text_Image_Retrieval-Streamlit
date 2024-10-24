from components.init import init_text_retrieval, init_text_retrieval_advance
from components.UI import display_header, display_result_text, display_text_results_advance
import streamlit as st
from utils.text_retrieval.get_texts_by_id import get_texts_by_ids
def main():
  collection_text_basic, corpus = init_text_retrieval()
  collection_text_advance = init_text_retrieval_advance()
  display_header("CONTENT BASED TEXT RETRIEVAL")

  st.divider()

  #  luôn tạo biến result trong session để khi nhấn nút thì re-render UI cx kh mất dữ liệu cũ
  if 'results' not in st.session_state:
    st.session_state.results = None

  st.session_state.query = st.text_input("Enter your search query:")

  _, col2, _ = st.columns([1, 3, 1])
  with col2:
    # Tạo 2 nút
    button1, button2 = st.columns(2)

    with button1:
      if st.button('TEXT SEARCH BASIC'):
        if st.session_state.query.strip():  # Kiểm tra xem query có trống không
          st.session_state.open_state = 'search_text_basic'
          st.session_state.results = collection_text_basic.query(
              query_texts=[st.session_state.query], n_results=5, include=["distances"])
        else:
          st.warning("Please enter a search query.")

    with button2:
      if st.button('TEXT SEARCH ADVANCE'):
        if st.session_state.query.strip():  # Kiểm tra xem query có trống không
          st.session_state.open_state = 'search_text_advance'
          st.session_state.results = collection_text_advance.query(
              query_texts=[st.session_state.query], n_results=5, include=["distances", "documents"])
        else:
          st.warning("Please enter a search query.")

  if st.session_state.results is not None:
    if st.session_state.open_state == 'search_text_basic':
      texts_result = get_texts_by_ids(
          corpus, st.session_state.results['ids'][0])
      display_result_text(texts_result)
    elif st.session_state.open_state == 'search_text_advance':
      display_text_results_advance(st.session_state.results)


if __name__ == "__main__":
  main()
