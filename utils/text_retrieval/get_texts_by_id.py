def get_texts_by_ids(corpus, ids: list):
  files_paths = [corpus[int(id.split('_')[1])] for id in ids]
  return files_paths
