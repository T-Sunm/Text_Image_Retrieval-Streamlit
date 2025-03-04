from components.UI import display_header, display_UI_EQA_basic, display_UI_EQA_advanced
import streamlit as st
from api.question_answering import extract_qa_basics, extract_qa_advanced

def main():
  # 1) Khởi tạo các biến session_state nếu chưa có
  if 'query' not in st.session_state:
    st.session_state.query = ""
  if 'results' not in st.session_state:
    st.session_state.results = None
  if 'open_state' not in st.session_state:
    st.session_state.open_state = None

  # 2) Hiển thị header
  display_header("EXTRACTIVE QUESTION ANSWERING")
  st.divider()

  # 3) Input cho query
  st.session_state.query = st.text_input("Enter your search query:")

  # 4) Bố trí nút BASIC và ADVANCE
  _, col2, _ = st.columns([1, 22, 1])
  with col2:
    button1, button2 = st.columns(2)

    with button1:
      if st.button('EXTRACTIVE QUESTION ANSWERING BASIC'):
        st.session_state.open_state = 'search_text_basic'

    with button2:
      if st.button('EXTRACTIVE QUESTION ANSWERING ADVANCE'):
        st.session_state.open_state = 'search_text_advance'
        st.session_state.results = extract_qa_advanced(
            st.session_state.query)

  if st.session_state.open_state == 'search_text_basic':
    display_UI_EQA_basic()
  elif st.session_state.open_state == 'search_text_advance':
    display_UI_EQA_advanced(st.session_state.results)
  else:
    st.warning("No results to display.")


if __name__ == "__main__":
  main()
