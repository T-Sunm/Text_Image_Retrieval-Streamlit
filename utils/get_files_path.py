import os
import json

def create_image_cache(file_paths: list, cache_file=r"D:\Asus\AIO\Project\Text_Image_Retrieval-Streamlit\caches\file_paths_cache.json"):
   # lưu vào file
  with open(cache_file, 'w') as f:
    json.dump(file_paths, f)
    print("Saved file paths to cache.")


def get_image_cache(cache_file=r"D:\Asus\AIO\Project\Text_Image_Retrieval-Streamlit\caches\file_paths_cache.json"):
  if os.path.exists(cache_file):
    with open(cache_file, 'r') as f:
      file_paths = json.load(f)
      print("Loaded file paths from cache.")
      return file_paths

def get_files_paths_by_ids(files_path, ids: list):
  files_paths = [files_path[int(id.split('_')[1])] for id in ids]
  return files_paths
