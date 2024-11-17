import os
import json

def create_image_cache(file_paths: list, cache_file=r"D:\Asus\AIO\Project\Text_Image_Retrieval-Streamlit\caches\file_paths_cache.json"):
   # lưu vào file
  with open(cache_file, 'w') as f:
    json.dump(file_paths, f)
    print("Saved file paths to cache.")
