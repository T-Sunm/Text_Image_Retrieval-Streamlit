import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


def lowercase(text: str):
  return text.lower()


def punctual_removal(text: str):
  translator = str.maketrans('', '', string.punctuation)

  return text.translate(translator)

def tokenizer(text: str):
  return text.split()

def remove_stopword(vocab_lst: list):
  stopword = stopwords.words('english')
  return [vocab for vocab in vocab_lst if vocab not in stopword]


def stemming(vocab_lst: list):
  # Khởi tạo PorterStemmer
  ps = PorterStemmer()
  return [ps.stem(vocab) for vocab in vocab_lst]

def preprocessing_text(text):
  text = lowercase(text)
  text = punctual_removal(text)
  vocabs = tokenizer(text)
  vocabs = remove_stopword(vocabs)
  vocabs = stemming(vocabs)

  return vocabs
