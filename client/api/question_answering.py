import os
import requests
import io
from utils.preprocessing.decoding_text import decode_escaped_strings
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def extract_qa_basics(text: str):

  url = f"{BACKEND_URL}/text/retrieval_basic"
  params = {"query": text}
  headers = {'accept': 'application/json'}
  response = requests.post(url, headers=headers, params=params, timeout=10)

  if response.status_code == 200:
    # Lấy JSON từ phản hồi
    json_results = response.json()

    # Truy cập vào các trường `ids` và `distances`
    ids = json_results.get("ids", [])
    distances = json_results.get("distances", [])
    documents = json_results.get("documents", [])

    decoded_documents = decode_escaped_strings(documents[0])
    return {"ids": ids, "distances": distances, "documents": decoded_documents}
  else:
    return "Error: API request failed.", None


def extract_qa_advanced(text: str):

  url = f"{BACKEND_URL}/eqa/extract_question_answering"
  params = {"query": text}
  headers = {'accept': 'application/json'}
  response = requests.post(url, headers=headers, params=params, timeout=10)

  if response.status_code == 200:
    # Lấy JSON từ phản hồi
    json_results = response.json()
  # Trả về list các dict
    return json_results
  else:
    return f"Error: status_code = {response.status_code}", None
