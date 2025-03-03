from transformers import AutoTokenizer
from transformers import AutoModel, AutoTokenizer
import torch


device = torch.device(
    "cuda") if torch.cuda.is_available() else torch.device("cpu")

MODEL_NAME = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME).to(device)

def cls_pooling(model_output):
  return model_output.last_hidden_state[:, 0]

def get_single_text_embeddings(question):
  encoded_input = tokenizer(
      question,
      padding=True,
      truncation=True,
      return_tensors='pt'
  )
  encoded_input = {k: v.to(device) for k, v in encoded_input.items()}
  model_output = model(**encoded_input)

  return cls_pooling(model_output)
