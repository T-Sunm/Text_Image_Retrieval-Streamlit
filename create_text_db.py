from datasets import load_from_disk
from tqdm import tqdm
import chromadb
from chromadb.utils import embedding_functions
import numpy as np
from utils.text_retrieval.create_corpus_q import create_corpus_queries
from utils.text_retrieval.text_embedding import get_single_text_embeddings
from utils.text_retrieval.rw_text_cache import create_text_cache

def add_texts_to_collection(collection: chromadb.Collection, corpus: list, batch_size=40000):
  ids_path = []
  embeddings = []

  for id, text in tqdm(enumerate(corpus), total=len(corpus)):
    try:
      embedding_text = get_single_text_embeddings(text)
      ids_path.append(f"id_{id}")
      embeddings.append(embedding_text.tolist())

      # Kiểm tra nếu số lượng dữ liệu đã đạt đến batch_size
      if len(ids_path) >= batch_size:
        collection.add(ids=ids_path, embeddings=embeddings)
        ids_path = []  # Reset lại danh sách sau khi thêm vào collection
        embeddings = []
    except Exception as e:
      print(f"Error processing in corpus {id}: {e}")

  # Thêm batch cuối cùng nếu còn dữ liệu
  if ids_path:
    collection.add(ids=ids_path, embeddings=embeddings)

  print(f"Finished adding {len(corpus)} texts to the collection.")


db_path = r"D:\Asus\AIO\Project\Text_Image_Retrieval-Streamlit\database\database_text"
ds = load_from_disk('./data/ms_marco_v1.1')
subset = ds['train'].to_list()

embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=db_path)

collection_text = client.get_or_create_collection(
    name='text_collection',
    embedding_function=embedding_function,
    metadata={"hnsw:space": "cosine"}
)

queries_infos, queries, corpus = create_corpus_queries(subset)

create_text_cache(corpus=corpus)

add_texts_to_collection(collection_text, corpus)
