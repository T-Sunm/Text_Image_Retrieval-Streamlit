import os
import json

def create_text_cache(queries: list, queries_infos: list, cache_file=r"D:\Asus\AIO\Project\Text_Image_Retrieval-Streamlit\caches\texts_cache.json"):
  """
  Lưu cặp dữ liệu queries và queries_infos vào file JSON để dùng cho lần sau.
  """
  # Tạo thư mục chứa file cache nếu chưa tồn tại
  os.makedirs(os.path.dirname(cache_file), exist_ok=True)

  # Tạo dictionary chứa queries và queries_infos
  data = {
      'queries': queries,
      'queries_infos': queries_infos
  }

  # Lưu dữ liệu vào file JSON
  with open(cache_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Saved queries and queries_infos to cache at {cache_file}.")


def get_text_cache(cache_file=r"D:\Asus\AIO\Project\Text_Image_Retrieval-Streamlit\caches\texts_cache.json"):
  """
  Tải dữ liệu queries và queries_infos từ file JSON nếu tồn tại.
  Trả về None nếu file không tồn tại.
  """
  if os.path.exists(cache_file):
    with open(cache_file, 'r', encoding='utf-8') as f:
      data = json.load(f)
      queries = data.get('queries', [])
      queries_infos = data.get('queries_infos', [])
      print(
          f"Loaded queries and queries_infos from cache at {cache_file}.")
      return queries, queries_infos
  else:
    print(f"Cache file not found at {cache_file}.")
    return None, None
