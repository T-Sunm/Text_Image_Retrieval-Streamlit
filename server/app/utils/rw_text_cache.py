import os
import json

def create_text_cache(corpus: list, cache_file=r"D:\Asus\AIO\Project\Text_Image_Retrieval-Streamlit\caches\texts_cache.json"):
  # lưu vào file
  with open(cache_file, 'w') as f:
    json.dump(corpus, f)
    print("Saved corpus to cache.")


def get_text_cache(cache_file=r"D:\Asus\AIO\Project\Text_Image_Retrieval-Streamlit\caches\texts_cache.json"):
  if os.path.exists(cache_file):
    with open(cache_file, 'r') as f:
      corpus = json.load(f)
      print("Loaded corpus from cache.")
      return corpus


def get_texts_by_ids(corpus, ids: list):
  files_paths = [corpus[int(id.split('_')[1])] for id in ids]
  return files_paths
