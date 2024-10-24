import os
import json


def create_text_cache(corpus: list, cache_file=r"../../../../../caches/texts_cache.json"):
  # lưu vào file
  with open(cache_file, 'w') as f:
    json.dump(corpus, f)
    print("Saved corpus to cache.")
