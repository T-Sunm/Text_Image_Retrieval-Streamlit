from datasets import load_dataset
import pandas as pd
import os
from preprocessing.pre_processing import save_images_to_folder
def get_data():
  image_data_train = load_dataset("conceptual_captions", split="train")
  image_data_test = load_dataset("conceptual_captions", split="validation")

  df_data_train = pd.DataFrame(image_data_train)
  df_data_test = pd.DataFrame(image_data_test)

  # train_dir = 'client/data/data_multimodal/train'
  # test_dir = 'client/data/data_multimodal/test'

  dataset_path = os.path.abspath(
      os.path.join(os.path.dirname(__file__), "../../../../client/data/data_multimodal"))

  if os.path.exists(dataset_path):
    print(f"Database already exists at {dataset_path}. Skipping creation.")
    return
  train_path = ''
  test_path = ''
  # Tạo thư mục nếu chưa tồn tại

  train_path = os.path.join(dataset_path, 'train')
  test_path = os.path.join(dataset_path, 'test')
  os.makedirs(train_path)
  os.makedirs(test_path)

  df_data_train = save_images_to_folder(
      df_data_train, train_path, 'train')
  df_data_test = save_images_to_folder(
      df_data_test, test_path, 'test')

  print("Images have been saved to train and test directories.")

  return df_data_train, df_data_test
