from datasets import load_dataset
from tqdm import tqdm
import torch
import chromadb
from preprocessing.text_embedding import get_single_text_embeddings
import json
import os
device = torch.device(
    "cuda") if torch.cuda.is_available() else torch.device("cpu")

def add_texts_to_collection(collection: chromadb.Collection, datasets, batch_size=40000):
  """Thêm văn bản và embeddings của chúng vào collection ChromaDB."""
  ids_path = []
  embeddings = []
  answers = []
  for text in tqdm(datasets, total=len(datasets)):
    try:
      embedding_question = get_single_text_embeddings(text['question'])
      ids_path.append(text['id'])
      embeddings.append(embedding_question.tolist()[0])

      # lưu thông tin
      selected_text = {
          'question': text['question'], 'context': text['context']}
      answers.append(json.dumps(selected_text))
      # Kiểm tra nếu số lượng dữ liệu đã đạt đến batch_size
      if len(ids_path) >= batch_size:

        collection.add(ids=ids_path, embeddings=embeddings, documents=answers)
        ids_path = []  # Reset lại danh sách sau khi thêm vào collection
        embeddings = []
        answers = []
    except Exception as e:
      print(f"Error processing in corpus {text['id']}: {e}")

  # Thêm batch cuối cùng nếu còn dữ liệu
  if ids_path:
    collection.add(ids=ids_path, embeddings=embeddings, documents=answers)

  print(f"Finished adding {len(datasets)} texts to the collection.")

def main():
  """Hàm chính để kiểm tra và thêm văn bản vào database."""
  # Đường dẫn database
  db_path = r"../../database/database_textqa"

  # Kiểm tra xem database đã tồn tại chưa
  if os.path.exists(db_path):
    print(f"Database already exists at {db_path}. Skipping creation.")
    return
  else:
    print("database not have")

  # Tạo client ChromaDB với đường dẫn lưu trữ
  client = chromadb.PersistentClient(path=db_path)

  DATASET_NAME = "squad"
  raw_datasets = load_dataset(DATASET_NAME)

  # Tạo hoặc lấy collection nếu chưa tồn tại
  collection_text = client.get_or_create_collection(
      name='textqa_collection',
      metadata={"hnsw:space": "cosine"}
  )


if __name__ == "__main__":
  main()
