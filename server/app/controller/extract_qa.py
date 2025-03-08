from utils.initialize_models import init_extract_qa
from utils.preprocessing.text_embedding import get_single_text_embeddings_eqa
import json
def e2e_extractive_question_answering(query: str):
  answers = []
  collection_answer, question_answerer = init_extract_qa()
  query_embedding = get_single_text_embeddings_eqa(
      [query]).cpu().detach().numpy().tolist()[0]

  results = collection_answer.query(
      query_embeddings=[query_embedding],
      n_results=5
  )

  for idx, id_sample in enumerate(results['ids'][0]):
    context_str = results['documents'][0][idx]  # Đây là chuỗi JSON
    context_dict = json.loads(context_str)
    answer = question_answerer(
        question=query,
        context=context_dict['context']
    )
    answers.append({
        "answer": answer['answer'],
        "score_answer": answer['score'],
        "question": context_dict['question'],
        "context": context_dict['context'],
        "score_similarity_question": results["distances"][0][idx],
        "location": {"start": answer['start'], "end": answer['end']}
    })

  return answers


def extractive_question_answering(query: str, context: str):
  _, question_answerer = init_extract_qa()

  answer = question_answerer(
      question=query,
      context=context
  )
  answer = {
      "answer": answer['answer'],
      "score_answer": answer['score'],
      "question": query,
      "context": context,
      "score_similarity_question": 1,
      "location": {"start": answer['start'], "end": answer['end']}
  }

  return answer
