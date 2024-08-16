import streamlit as st
from utils.resetquery import reset_query
from components.init import init
from components.UI import display_header, display_search_button, display_result, search_input
def main():
  collection, files_path = init()
# --------- UI ----------------
  display_header()
  display_search_button()

  # Func : khi click vào loại search khác thì reset state và input_query
  if st.session_state.open_state != st.session_state.last_state:
    reset_query()
  st.session_state.last_state = st.session_state.open_state

  st.divider()

  search_input()
  # Initialize results variable
  results = None
  if st.button('SEARCH'):
    if st.session_state.query is not None:
      if st.session_state.open_state == "search_text":
        results = collection.query(
            query_texts=[st.session_state.query], n_results=5, include=["distances"])
      elif st.session_state.open_state == "search_image":
        results = collection.query(
            query_embeddings=[st.session_state.query.tolist()], n_results=5, include=["distances"])
    else:
      return

  display_result(results, files_path)


if __name__ == "__main__":
  main()
