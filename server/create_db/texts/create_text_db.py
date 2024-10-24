from datasets import load_from_disk
from tqdm import tqdm
import chromadb
from chromadb.utils import embedding_functions
import numpy as np
from preprocessing.text_retrieval.create_corpus_q import create_corpus_queries
from preprocessing.text_retrieval.text_embedding import get_single_text_embeddings
from preprocessing.text_retrieval.rw_text_cache import create_text_cache
import os


def add_texts_to_collection(collection: chromadb.Collection, corpus: list, batch_size=40000):
  """Thêm văn bản và embeddings của chúng vào collection ChromaDB."""
  ids_path = []
  embeddings = []

  for idx, text in tqdm(enumerate(corpus), total=len(corpus)):
    try:
      embedding_text = get_single_text_embeddings(text)
      ids_path.append(f"id_{idx}")
      embeddings.append(embedding_text.tolist())

      # Kiểm tra nếu số lượng dữ liệu đã đạt đến batch_size
      if len(ids_path) >= batch_size:
        collection.add(ids=ids_path, embeddings=embeddings)
        ids_path = []  # Reset lại danh sách sau khi thêm vào collection
        embeddings = []
    except Exception as e:
      print(f"Error processing in corpus {idx}: {e}")

  # Thêm batch cuối cùng nếu còn dữ liệu
  if ids_path:
    collection.add(ids=ids_path, embeddings=embeddings)

  print(f"Finished adding {len(corpus)} texts to the collection.")


def main():
  """Hàm chính để kiểm tra và thêm văn bản vào database."""
  # Đường dẫn database
  db_path = r"../../database/database_text"

  # Kiểm tra xem database đã tồn tại chưa
  if os.path.exists(db_path):
    print(f"Database already exists at {db_path}. Skipping creation.")
    return
  else:
    print("chưa có dcmmm")

  # Tạo client ChromaDB với đường dẫn lưu trữ
  client = chromadb.PersistentClient(path=db_path)

  # Tải dataset
  ds = load_from_disk('../../data/ms_marco_v1.1')
  subset = ds['train'].to_list()

  # Tạo hàm nhúng văn bản
  embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
      model_name="all-MiniLM-L6-v2"
  )

  # Tạo hoặc lấy collection nếu chưa tồn tại
  collection_text = client.get_or_create_collection(
      name='text_collection',
      embedding_function=embedding_function,
      metadata={"hnsw:space": "cosine"}
  )

  # Tạo corpus và queries
  queries_infos, queries, corpus = create_corpus_queries(subset)

  # Tạo cache cho văn bản
  create_text_cache(corpus=corpus)

  # Thêm văn bản vào collection
  add_texts_to_collection(collection_text, corpus)


if __name__ == "__main__":
  main()
