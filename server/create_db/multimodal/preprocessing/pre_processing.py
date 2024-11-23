import torch
import requests
import pandas as pd
from PIL import Image
from io import BytesIO
from tqdm import tqdm
import os
import numpy as np
def check_valid_urls(image_url):
  try:
    response = requests.get(image_url, timeout=20)
    Image.open(BytesIO(response.content))
    return True
  except Exception as e:
    print(f"Unexpected error: {e}")
    return False

def save_images_to_folder(df, folder, type):
  thresholds = {'train': 2000, 'test': 100}
  df_copy = df.copy()
  counter = 0
  for idx, row in df_copy.iterrows():
    if type in thresholds and counter >= thresholds[type]:
      break

    image_url = row['image_url']

    if not check_valid_urls(image_url):
      df_copy.loc[idx, 'image_path'] = None
      df_copy.loc[idx, 'is_valid'] = False
      continue

    try:
      response = requests.get(image_url)
      # nhớ phải chuyển về RGB
      img = Image.open(BytesIO(response.content)).convert("RGB")
      image_path = os.path.join(folder, f"{type}_{counter}.png")
      img.save(image_path)

      df_copy.loc[idx, 'image_path'] = image_path

      print(f"Image {counter} saved successfully.")
      counter += 1
      df_copy.loc[idx, 'is_valid'] = True
    except Exception as e:
      print(f"Error saving image {image_url}: {e}")
      # Cập nhật nếu có lỗi trong việc lưu ảnh
      df_copy.loc[idx, 'image_path'] = None
      df_copy.loc[idx, 'is_valid'] = False
  return df_copy

def get_img(file_path):
  try:
    # Mở ảnh từ tệp
    image = Image.open(file_path)
    return image
  except Exception as e:
    print(f"Error occurred: {e}")
    return False

def get_single_text_embedding(tokenizer, model, text):
    # trả về là 1 tensor
  inputs = tokenizer(text, return_tensors='pt')
  text_embeddings = model.get_text_features(**inputs)
  # convert the embeddings to numpy array
  embedding_as_np = text_embeddings.cpu().detach().numpy()
  return embedding_as_np[0].tolist()


def get_single_image_embedding(processor, model, img):
    # trả về là 1 tensor
  device = "cuda" if torch.cuda.is_available() else "cpu"
  inputs = processor(images=img, return_tensors="pt")[
      'pixel_values'].to(device)
  text_embeddings = model.get_image_features(inputs)
  # convert the embeddings to numpy array
  embedding_as_np = text_embeddings.cpu().detach().numpy()
  return embedding_as_np[0].tolist()
