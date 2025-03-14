import streamlit as st
from PIL import Image
import numpy as np
import json
import os
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
    query = st.file_uploader("Choose an image", type=[
                             'jpg', 'png', 'jpeg'])

    if query is not None:
      image = Image.open(query)
      image_name = query.name  # Lấy tên của ảnh

      # Lưu tên ảnh và embedding vào dictionary trong session_state.query
      st.session_state.query = {
          "image_name": image_name,
          "image": image
      }

      # Display uploaded image and name
      st.image(image, caption=f'Uploaded Image: {image_name}')

def highlight_answer(context: str, location, color) -> str:
  if "start" in location and "end" in location:
    start = location["start"]
    end = location["end"]
    # Kiểm tra điều kiện để tránh lỗi nếu location vượt quá độ dài context
    if 0 <= start < end <= len(context):
      prefix = context[:start]
      highlight = context[start:end]
      suffix = context[end:]
      # Tô màu nền cho đoạn được highlight (có thể tùy chỉnh màu sắc)
      formatted_context = f"{prefix}<span style='background-color: {color};'>{highlight}</span>{suffix}"
    else:
      formatted_context = context
  else:
    formatted_context = context

  st.markdown(formatted_context, unsafe_allow_html=True)


def display_result(results, is_image=False, captions=None):
  """
    Hiển thị một hình ảnh trong giao diện Streamlit.

    Các bước thực hiện:
    1. Chuyển đổi dấu phân cách trong đường dẫn từ '\\' (Windows) sang '/' để chuẩn hóa đường dẫn.
    2. Chuyển đường dẫn thành đường dẫn tuyệt đối để đảm bảo chính xác vị trí của tệp.
    3. Sử dụng `col.image` trong Streamlit để hiển thị ảnh với chiều rộng tự động phù hợp với cột giao diện.

    Args:
        res (str): Đường dẫn tới tệp ảnh,là đường dẫn tương đối bắt đầu = data\\....

    Returns:
        None
  """
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
      if is_image == False:
        # Hiển thị nhãn
        col.markdown(f"""
              <div style="
                  display: inline-block;
                  background-color: #f0f0f0;
                  padding: 10px 15px;
                  border-radius: 10px;
                  margin-top: 5px;
                  font-size: 13px;
                  font-family: Arial, sans-serif;
                  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                  color: #333;
              ">
                  {captions[i]['caption']}
              </div>
        """, unsafe_allow_html=True)

      fixed_path = res.replace("\\", "/")
      absolute_path = os.path.abspath(fixed_path)
      col.image(absolute_path, use_column_width=True)

      # Divider trong cùng cột
      col.divider()


def display_result_text(results: list):
  if results:
    colors = ['orange', 'green', 'red', 'gray', 'blue']

    # Tạo một container có chiều cao cố định
    with st.container(height=600):
      for i, res in enumerate(results):
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
  for doc in texts_result['documents']:
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
      _, _, button_col3, _ = st.columns([
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
        <strong>Answer</strong> <span style="font-weight: normal;">{st.session_state.selected_document.get('title', '')}</span>
    </div>
    """,
        unsafe_allow_html=True
    )

    relevant_docs = st.session_state.selected_document.get(
        'document_relevant', [])
    if relevant_docs:
      with st.container(height=600):
        for i, doc in enumerate(relevant_docs):
          st.markdown(f"#### **Relevant document {i + 1}**")
          st.write(doc)
          st.markdown("---")
    else:
      st.write("Please select a document to view the content.")


def display_UI_EQA_basic(question_answering_func):
  st.write(
      "Paste your text in the context field and type a question to get an answer from the text!")

  with st.container():
    # Ô nhập context
    context_text = st.text_area(
        label="Context",
        placeholder="Paste your context here...",
        value="The Amazon rainforest is also known in English as the Amazon Jungle.",
        height=150
    )

    # Nút xử lý
    if st.button("Get Answer"):
      # Xử lý loading spinner
      with st.spinner("Thinking..."):
        if st.session_state.query.strip():
          # Gọi hàm QA logic
          result = question_answering_func(
              st.session_state.query, context_text)
          st.session_state.qa_result = result
        else:
          st.warning("Please enter a question before submitting.")

  if "qa_result" in st.session_state and st.session_state.qa_result is not None:
    result = st.session_state.qa_result
    with st.container():
      st.subheader("Output")
      # Lấy các thông tin quan trọng
      answer = result.get("answer", "")
      score = result.get("score_answer", 0.0)
      location = result.get("location", {})

      # Hiển thị answer
      st.write(f"**Answer**: {answer}")
      st.write(f"**Confidence score**: {score:.3f}")

      # Gọi hàm highlight_answer để highlight câu trả lời trong context
      highlight_answer(context_text, location, "orange")
      with st.expander("See raw result JSON"):
          st.json(result)

def display_UI_EQA_advanced(results_qa):
  # Chuyển data_list (list dict) thành danh sách documents định dạng UI mong muốn
  documents = []
  for i, item in enumerate(results_qa):
    formatted_doc = {
        "query_id": i,  # Sử dụng index làm query_id nếu không có field riêng
        "title": item.get("answer", ""),
        "content": item.get("context", ""),
        "question": item.get("question", ""),
        "score_answer": item.get("score_answer", 0.0),
        "score_similarity_question": item.get("score_similarity_question", 0.0),
        "location": item.get('location', {})
    }
    documents.append(formatted_doc)
  colors = ['orange', 'green', 'red', 'gray', 'blue']

  # Tạo layout: cột bên trái (3) hiển thị danh sách document, cột bên phải (5) hiển thị chi tiết document được chọn
  col1, col2 = st.columns([3, 5])

  with col1:
    for i, doc in enumerate(documents):
      # Hiển thị Rank và Title của từng document với style tùy chỉnh
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
      # Tạo nút 'Choose' căn giữa bằng cách chia cột nhỏ
      _, _, button_col, _ = st.columns([0.5, 0.5, 1, 0.5])
      with button_col:
        if st.button("Choose", key=f"button_{i}"):
          st.session_state.selected_document = {
              "id": i,
              "title": doc["title"],
              "content": doc["content"],
              "question": doc["question"],
              "score_answer": doc["score_answer"],
              "score_similarity_question": doc["score_similarity_question"],
              "location": doc["location"]
          }
      # Ngăn cách giữa các document
      st.markdown('<hr style="margin: 5px 0;">', unsafe_allow_html=True)

  with col2:
    selected_doc = st.session_state.get("selected_document", None)
    if selected_doc:
      # Hiển thị tiêu đề (Answer) của document được chọn
      st.markdown(
          f"""
                <div style="margin-bottom: 20px;">
                    <strong>Answer:</strong> <span style="font-weight: normal;">{selected_doc.get('title', '')}</span>
                </div>
                """, unsafe_allow_html=True
      )
      # Hiển thị câu hỏi gốc và các điểm số
      st.markdown(f"**Question:** {selected_doc.get('question', '')}")
      st.markdown(
          f"**Score Answer:** {selected_doc.get('score_answer', 0.0)}")
      st.markdown(
          f"**Score Similarity:** {selected_doc.get('score_similarity_question', 0.0)}")
      st.markdown("### Context")

      context_text = selected_doc.get('content', '')
      location = selected_doc.get('location', None)
      highlight_answer(context_text, location,
                       colors[selected_doc['id'] % len(colors)])

    else:
      st.write("Please select a document to view the content.")
