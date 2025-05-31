import os
import requests
import io
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def text_to_image(text):

  url = f"{BACKEND_URL}/multimodal/text_retrieval_img"
  params = {"query": text}
  headers = {'accept': 'application/json'}
  response = requests.post(url, headers=headers, params=params, timeout=30)

  if response.status_code == 200:
    # Lấy JSON từ phản hồi
    json_results = response.json()

    # Truy cập vào các trường `ids` và `distances`
    ids = json_results.get("ids", [])
    distances = json_results.get("distances", [])
    documents = json_results.get("metadatas", [])
    return {"ids": ids, "distances": distances, "documents": documents[0]}
  else:
    return "Error: API request failed.", None
