import os
import requests
import io
from utils.preprocessing.decoding_text import decode_escaped_strings
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def extract_qa_basics(query: str, context: str):

  url = f"{BACKEND_URL}/eqa/question_answering"
  params = {"query": query, "context": context}
  headers = {'accept': 'application/json'}
  response = requests.post(url, headers=headers, params=params, timeout=30)

  if response.status_code == 200:
    # Lấy JSON từ phản hồi
    json_results = response.json()

    return json_results
  else:
    return f"Error: status_code = {response.status_code}", None


def extract_qa_advanced(text: str):

  url = f"{BACKEND_URL}/eqa/e2e_question_answering"
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
