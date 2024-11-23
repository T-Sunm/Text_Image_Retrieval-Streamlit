import streamlit as st
from utils.resetquery import reset_query
from components.init import init_image_retrieval
from components.UI import display_header, display_search_button, display_result, search_input
from utils.rw_image_cache import get_files_paths_by_ids
from api.image_retrieval import image_to_image
from api.multimodal_retrieval import text_to_image
# Cấu hình trang với tiêu đề tùy chỉnh
st.set_page_config(page_title="Main Page Title", page_icon=":rocket:")

def main():
  files_path, files_path_multimodal = init_image_retrieval()

  # --------- UI ----------------
  display_header("CONTENT BASED IMAGE RETRIEVAL")
  display_search_button()

  # Reset trạng thái nếu chế độ tìm kiếm thay đổi
  if st.session_state.open_state != st.session_state.last_state:
    reset_query()
  st.session_state.last_state = st.session_state.open_state

  st.divider()

  search_input()
  # Initialize results variable
  results = None

  # Khi nhấn nút SEARCH
  if st.button('SEARCH'):
    if st.session_state.query is not None:
      if st.session_state.open_state == "search_text":
        # Xử lý tìm kiếm theo text
        query_text = st.session_state.query
        results = text_to_image(query_text)
      elif st.session_state.open_state == "search_image":
        # Xử lý tìm kiếm theo image
        image = st.session_state.query["image"]
        image_name = st.session_state.query["image_name"]
        results = image_to_image(image, image_name)

  # Kiểm tra nếu kết quả truy vấn trả về là None
  if results is None:
    st.warning("No results found.")
    return  # Nếu không có kết quả thì không thực hiện tiếp

  # Kiểm tra nếu 'ids' có trong kết quả
  if 'ids' not in results:
    st.error("Invalid response format from query.")
    return

  # Cá nhân hóa logic hiển thị kết quả
  if st.session_state.open_state == "search_text":
    files_path_results = get_files_paths_by_ids(
        files_path_multimodal, results['ids'][0]
    )
    display_result(files_path_results, is_image=False,
                   captions=results['documents'])
  elif st.session_state.open_state == "search_image":
    files_path_results = get_files_paths_by_ids(
        files_path, results['ids'][0]
    )
    display_result(files_path_results, is_image=True)


if __name__ == "__main__":
  main()
