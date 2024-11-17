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

  # Xác định đường dẫn tuyệt đối đến thư mục 'client'
  client_root_path = os.path.abspath(os.path.join(
      os.path.dirname(__file__), "../../../client"))

  """Lấy tất cả đường dẫn file ảnh từ thư mục gốc và trả về cả đường dẫn tuyệt đối và tương đối."""
  absolute_paths = []
  relative_paths = []

  for class_name in os.listdir(folder_path):
    path_class_name = os.path.join(folder_path, class_name)
    for img_name in os.listdir(path_class_name):
      # Tạo đường dẫn tuyệt đối và chuẩn hóa
      absolute_path = os.path.normpath(
          os.path.join(path_class_name, img_name))
      absolute_paths.append(absolute_path)

      # Tạo đường dẫn tương đối bắt đầu từ client_root_path và chuẩn hóa
      relative_path = os.path.normpath(
          os.path.relpath(absolute_path, start=client_root_path))
      relative_paths.append(relative_path)

  return absolute_paths, relative_paths


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

  # Lấy đường dẫn đến thư mục cha của dự án (thư mục gốc chứa database)
  image_data_path = os.path.abspath(
      os.path.join(os.path.dirname(__file__), "../../../client/data/data_image/train"))

  print("Database Path:", image_data_path)

  # Lấy đường dẫn các file ảnh
  absolute_paths, relative_paths = get_files_path(image_data_path)

  # Tạo cache cho ảnh
  create_image_cache(file_paths=relative_paths)

  # Thêm ảnh và embeddings vào collection
  add_images_to_collection(collection, absolute_paths)
  print("Images and embeddings have been successfully added to the collection.")


if __name__ == "__main__":
  main()
