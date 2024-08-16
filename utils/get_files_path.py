import os
import json

def get_files_path(folder_path, cache_file=r"D:\Asus\AIO\Project\Text_Image_Retrieval-Streamlit\file_paths_cache.json"):

  if os.path.exists(cache_file):
    with open(cache_file, 'r') as f:
      file_paths = json.load(f)
      print("Loaded file paths from cache.")
      return file_paths

  #  nếu chưa có file_paths
  file_paths = []
  for class_name in os.listdir(folder_path):
    path_class_name = os.path.join(folder_path, class_name)
    for img_name in os.listdir(path_class_name):
      file_paths.append(os.path.join(path_class_name, img_name))

  # lưu vào file
  with open(cache_file, 'w') as f:
    json.dump(file_paths, f)
    print("Saved file paths to cache.")

  return file_paths


def get_files_paths_by_ids(files_path, ids: list):
  files_paths = [files_path[int(id.split('_')[1])] for id in ids]
  return files_paths
