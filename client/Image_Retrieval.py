import streamlit as st
from utils.resetquery import reset_query
from components.init import init_image_retrieval
from components.UI import display_header, display_search_button, display_result, search_input
from utils.get_data_in_caches import get_files_paths_by_ids
from api.image_retrieval import image_to_image
# Cấu hình trang với tiêu đề tùy chỉnh
st.set_page_config(page_title="Main Page Title", page_icon=":rocket:")

def main():
  files_path = init_image_retrieval()
# --------- UI ----------------
  display_header("CONTENT BASED IMAGE RETRIEVAL")
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
        results = None
      elif st.session_state.open_state == "search_image":
        # Lấy name và embedding từ session_state.query
        image = st.session_state.query["image"]
        image_name = st.session_state.query["image_name"]

        # Gọi hàm image_to_image với embedding và name
        results = image_to_image(image, image_name)

  # Kiểm tra nếu kết quả truy vấn trả về là None
  if results is None:
    st.warning("No results found.")
    return  # Nếu không có kết quả thì không thực hiện tiếp

    # Kiểm tra nếu 'ids' có trong kết quả
  if 'ids' not in results:
    st.error("Invalid response format from query.")
    return

  files_path_results = get_files_paths_by_ids(
      files_path, results['ids'][0])
  display_result(files_path_results, is_image=True)


if __name__ == "__main__":
  main()
