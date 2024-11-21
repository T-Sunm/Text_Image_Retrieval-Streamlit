from transformers import CLIPProcessor, CLIPModel, CLIPTokenizer
import chromadb
import os
from tqdm import tqdm
from preprocessing.get_dataset import get_data
from preprocessing.pre_processing import get_img, get_single_text_embedding, get_single_image_embedding
import pandas as pd
import torch

def get_model_info(model_id, device):

  # Save the model to device
  model = CLIPModel.from_pretrained(model_id).to(device)
  # Get the processor
  processor = CLIPProcessor.from_pretrained(model_id)
  # Get the tokenizer
  tokenizer = CLIPTokenizer.from_pretrained(model_id)
  # Return model, processor & tokenizer
  return model, processor, tokenizer


def main():

  db_path = os.path.abspath(
      os.path.join(os.path.dirname(__file__), "../../database/database_multimodal"))
  cache_path = os.path.abspath(
      os.path.join(os.path.dirname(__file__), "../../../client/caches/multimodal_db.csv"))

#   Kiểm tra xem database đã tồn tại chưa
  if os.path.exists(db_path):
    print(f"Database already exists at {db_path}. Skipping creation.")
    return
  client = chromadb.PersistentClient(path=db_path)

  df_data_train, _ = get_data()
  df_data_train = df_data_train.loc[df_data_train['is_valid'] == True].reset_index(
      drop=True)
  df_data_train['image'] = df_data_train['image_path'].apply(get_img)
  df_data_train.to_csv(
      cache_path, index=False)

  device = "cuda" if torch.cuda.is_available() else "cpu"
  model_id = "openai/clip-vit-base-patch32"
  model, processor, tokenizer = get_model_info(model_id, device)

  tqdm.pandas(desc="Embedding Text")
  df_data_train["text_embeddings"] = df_data_train['caption'].progress_apply(
      lambda x: get_single_text_embedding(tokenizer, model, x))

  tqdm.pandas(desc="Embedding Images")
  df_data_train["img_embeddings"] = df_data_train['image'].progress_apply(
      lambda x: get_single_image_embedding(processor, model, x))

  ids = [f"id_{i}" for i in df_data_train.index]

  text_embeddings = df_data_train['text_embeddings'].to_list()
  img_embeddings = df_data_train['img_embeddings'].to_list()
  cations = df_data_train['caption'].to_list()

  # Tạo collection cho image embeddings
  text_to_image_collection = client.get_or_create_collection(
      name='text_to_image_collection', metadata={"hnsw:space": "cosine"}
  )

  # Thêm image embeddings vào image collection
  text_to_image_collection.add(
      ids=ids,
      embeddings=img_embeddings,
      metadatas=[{"caption": caption} for caption in cations]
  )

  # Tạo collection cho text embeddings
  image_to_text_collection = client.get_or_create_collection(
      name='image_to_text_collection', metadata={"hnsw:space": "cosine"}
  )

  # Thêm text embeddings vào text collection
  image_to_text_collection.add(
      ids=ids,
      embeddings=text_embeddings,
      metadatas=[{"caption": caption} for caption in cations]
  )


if __name__ == "__main__":
  main()
