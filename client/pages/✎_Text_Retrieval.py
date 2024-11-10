from components.UI import display_header, display_result_text, display_text_results_advance
import streamlit as st
from api.text_retrieval import text_to_text_basics, text_to_text_advanced

def main():

  display_header("CONTENT BASED TEXT RETRIEVAL")

  if 'query' not in st.session_state:
    st.session_state.query = 0
  if 'selected_document' not in st.session_state:
    st.session_state.selected_document = {}
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
          st.session_state.results = text_to_text_basics(
              st.session_state.query)
        else:
          st.warning("Please enter a search query.")

    with button2:
      if st.button('TEXT SEARCH ADVANCE'):
        if st.session_state.query.strip():  # Kiểm tra xem query có trống không
          st.session_state.open_state = 'search_text_advance'
          st.session_state.results = text_to_text_advanced(
              st.session_state.query)
        else:
          st.warning("Please enter a search query.")

  if st.session_state.results is not None:
    if st.session_state.open_state == 'search_text_basic':
      display_result_text(st.session_state.results['documents'])
    elif st.session_state.open_state == 'search_text_advance':
      display_text_results_advance(st.session_state.results)


if __name__ == "__main__":
  main()
