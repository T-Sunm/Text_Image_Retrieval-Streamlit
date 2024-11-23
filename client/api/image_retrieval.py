import os
import requests
import io
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")


def image_to_image(image, image_name):

  # Chuyển ảnh thành byte để gửi qua API
  img_byte_arr = io.BytesIO()
  image.save(img_byte_arr, format='PNG')  # Chuyển ảnh thành byte stream
  img_byte_arr = img_byte_arr.getvalue()  # Lấy giá trị byte

  url = f"{BACKEND_URL}/image/retrieval"
  files = {'file_upload': (image_name, img_byte_arr,
                           'application/octet-stream')}
  headers = {'accept': 'application/json'}

  response = requests.post(url, headers=headers, files=files, timeout=10)

  if response.status_code == 200:
    # Lấy JSON từ phản hồi
    json_results = response.json()

    # Truy cập vào các trường `ids` và `distances`
    ids = json_results.get("ids", [])
    distances = json_results.get("distances", [])

    return {"ids": ids, "distances": distances}
  else:
    return "Error: API request failed.", None
