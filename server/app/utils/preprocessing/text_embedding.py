from transformers import CLIPProcessor, CLIPModel, CLIPTokenizer
import torch

# Load the model, processor, and tokenizer once
device = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_ID = "openai/clip-vit-base-patch32"
MODEL = CLIPModel.from_pretrained(MODEL_ID).to(device)
PROCESSOR = CLIPProcessor.from_pretrained(MODEL_ID)
TOKENIZER = CLIPTokenizer.from_pretrained(MODEL_ID)

def get_single_text_embedding_multimodal(text):
  # Reuse the loaded model, processor, and tokenizer
  inputs = TOKENIZER(text, return_tensors='pt').to(device)
  text_embeddings = MODEL.get_text_features(**inputs)
  # Convert the embeddings to numpy array
  embedding_as_np = text_embeddings.cpu().detach().numpy()
  return embedding_as_np[0].tolist()
