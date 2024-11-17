import os
import json

def get_image_cache(cache_file="../caches/file_paths_cache.json"):
  cache_file_abs = os.path.normpath(os.path.join(
      os.path.dirname(__file__), cache_file))

  if os.path.exists(cache_file_abs):
    with open(cache_file_abs, 'r') as f:
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