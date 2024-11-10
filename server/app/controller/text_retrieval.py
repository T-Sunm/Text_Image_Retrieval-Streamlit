from utils.initialize_models import init_text_retrieval, init_text_retrieval_advance


def text_basic_query(query: str):
  collection_text_basic = init_text_retrieval()

  results = collection_text_basic.query(
      query_texts=[query], n_results=5, include=["distances", "documents"])
  return results

def text_advanced_query(query: str):
  collection_text_advance = init_text_retrieval_advance()
  results = collection_text_advance.query(
      query_texts=[query], n_results=5, include=["distances", "documents"])
  return results
