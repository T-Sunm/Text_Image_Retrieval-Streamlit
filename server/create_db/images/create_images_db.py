from PIL import Image
import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
import numpy as np
from tqdm import tqdm
import os
from preprocessing.image_embedding import get_single_image_embeddings
from preprocessing.rw_image_cache import create_image_cache


def get_files_path(folder_path):
  """Lấy tất cả đường dẫn file ảnh từ thư mục gốc."""
  files_path = []
  for class_name in os.listdir(folder_path):
    path_class_name = os.path.join(folder_path, class_name)
    for img_name in os.listdir(path_class_name):
      files_path.append(os.path.join(path_class_name, img_name))
  return files_path


def add_images_to_collection(collection: chromadb.Collection, files_path):
  """Thêm ảnh và embeddings của chúng vào collection ChromaDB."""
  ids_path = []
  embeddings = []
  for idx, file_path in tqdm(enumerate(files_path), desc="Creating Image Embeddings and Adding to DB"):
    try:
      img_np = np.array(Image.open(file_path)).astype(np.uint8)
      embedding_img = get_single_image_embeddings(img_np)
      ids_path.append(f"id_{idx}")
      embeddings.append(embedding_img.tolist())
    except Exception as e:
      print(f"Error processing {file_path}: {e}")

  collection.add(ids=ids_path, embeddings=embeddings)


def main():
  """Hàm chính thực hiện xử lý lưu ảnh vào ChromaDB."""
  # Đường dẫn database
  db_path = "../../database/database_image"

  # Kiểm tra xem database đã tồn tại chưa
  if os.path.exists(db_path):
    print(f"Database already exists at {db_path}. Skipping creation.")
    return

  # Tạo client ChromaDB với đường dẫn lưu trữ
  client = chromadb.PersistentClient(path=db_path)
  image_loader = ImageLoader()
  embedding_function = OpenCLIPEmbeddingFunction()

  # Tạo collection nếu chưa tồn tại
  collection = client.get_or_create_collection(
      name='image_collection',
      embedding_function=embedding_function,
      data_loader=image_loader
  )

  # Đường dẫn đến thư mục chứa ảnh
  ROOTS = "../../data/data_image/train"

  # Lấy đường dẫn các file ảnh
  files_path = get_files_path(ROOTS)

  # Tạo cache cho ảnh
  create_image_cache(file_paths=files_path)

  # Thêm ảnh và embeddings vào collection
  add_images_to_collection(collection, files_path)
  print("Images and embeddings have been successfully added to the collection.")


if __name__ == "__main__":
  main()
