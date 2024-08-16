from PIL import Image
import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
import numpy as np
from tqdm import tqdm
import os
from utils.image_embedding import get_single_image_embeddings

def get_files_path(folder_path):
  files_path = []
  for class_name in os.listdir(folder_path):
    path_class_name = os.path.join(folder_path, class_name)
    for img_name in os.listdir(path_class_name):
      files_path.append(os.path.join(path_class_name, img_name))
  
  return files_path

def add_images_to_collection(collection: chromadb.Collection, files_path):

  ids_path = []
  embeddings = []
  for id, file_path in tqdm(enumerate(files_path), desc="Creating Image Embeddings and Adding to DB"):
    try:
      img_np = np.array(Image.open(file_path)).astype(np.uint8)
      embedding_img = get_single_image_embeddings(img_np)
      ids_path.append(f"id_{id}")
      embeddings.append(embedding_img.tolist())
    except Exception as e:
      print(f"Error processing {file_path}: {e}")

  collection.add(ids=ids_path, embeddings=embeddings)


db_path = r"D:\Asus\AIO\Project\Text_Image_Retrieval-Streamlit\database"
image_loader = ImageLoader()
client = chromadb.PersistentClient(path=db_path)
embedding_function = OpenCLIPEmbeddingFunction()
collection = client.get_or_create_collection(
    name='multimodal_collection',
    embedding_function=embedding_function,
    data_loader=image_loader
)
ROOTS = r"D:\Asus\AIO\Project\Text_Image_Retrieval-Streamlit\data\train"
files_path = get_files_path(ROOTS)

add_images_to_collection(collection, files_path)
