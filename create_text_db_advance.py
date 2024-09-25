from datasets import load_from_disk
from tqdm import tqdm
import chromadb
from chromadb.utils import embedding_functions
import numpy as np
from utils.text_retrieval_advance.create_corpus_advance import create_corpus_queries
from utils.text_retrieval.text_embedding import get_single_text_embeddings
import json

def add_texts_to_collection(collection: chromadb.Collection, queries: list, queries_infos: list, batch_size=40000):

  ids_path = []
  embeddings = []
  documents = []

  for id, text in tqdm(enumerate(queries), total=len(queries)):
    try:
      embedding_text = get_single_text_embeddings(text)
      ids_path.append(f"id_{id}")
      embeddings.append(embedding_text.tolist())

      # Tạo metadata với từng thông tin riêng lẻ từ query_info
      query_info = queries_infos[id]
      document = {
          "query_id": query_info['query_id'],
          "answer": query_info['answer'],
          "relevant_docs": query_info['relevant_docs'],
      }

      # 2 option :
      # tạo DB riêng để lưu
      # lưu cùng với chromadb + sqlite
      documents.append(json.dumps(document))

      # Kiểm tra nếu số lượng dữ liệu đã đạt đến batch_size
      if len(ids_path) >= batch_size:
        collection.add(
            ids=ids_path, embeddings=embeddings, documents=documents)
        ids_path = []  # Reset lại danh sách sau khi thêm vào collection
        embeddings = []
        documents = []
    except Exception as e:
      print(f"Error processing in corpus {id}: {e}")

  # Thêm batch cuối cùng nếu còn dữ liệu
  if ids_path:
    collection.add(ids=ids_path, embeddings=embeddings,
                   documents=documents)

  print(f"Finished adding {len(queries)} texts to the collection.")


db_path = r"D:\Asus\AIO\Project\Text_Image_Retrieval-Streamlit\database\database_text_advance"
ds = load_from_disk('./data/ms_marco_v1.1')
subset = ds['train'].to_list()

embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=db_path)

collection_text_advance = client.get_or_create_collection(
    name='text_collection_advance',
    embedding_function=embedding_function,
    metadata={"hnsw:space": "cosine"}
)

queries, queries_infos = create_corpus_queries(subset)

add_texts_to_collection(collection_text_advance, queries=queries,
                        queries_infos=queries_infos)
