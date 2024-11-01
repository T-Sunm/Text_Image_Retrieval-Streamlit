import os
import json

def get_text_cache(cache_file=r"D:\Asus\AIO\Project\Text_Image_Retrieval-Streamlit\caches\texts_cache.json"):
  if os.path.exists(cache_file):
    with open(cache_file, 'r') as f:
      corpus = json.load(f)
      print("Loaded corpus from cache.")
      return corpus


def get_texts_by_ids(corpus, ids: list):
  files_paths = [corpus[int(id.split('_')[1])] for id in ids]
  return files_paths


def get_image_cache(cache_file=r"D:\Asus\AIO\Project\Text_Image_Retrieval-Streamlit\caches\file_paths_cache.json"):
  if os.path.exists(cache_file):
    with open(cache_file, 'r') as f:
      file_paths = json.load(f)
      print("Loaded file paths from cache.")
      return file_paths

def get_files_paths_by_ids(files_path, ids):
  print(ids)
  results = []
  for id in ids:
    index = int(id.split("_")[1])
    results.append(files_path[index])

  return results
