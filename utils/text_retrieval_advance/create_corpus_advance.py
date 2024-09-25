from tqdm import tqdm

def create_corpus_queries(subset):

    # Khai báo danh sách chứa tập câu truy vấn và tài liệu có liên quan:
  queries_infos = []
  queries = []

  for sample in tqdm(subset, desc="Processing get data in dataset"):

    query_type = sample['query_type']
    if query_type != 'entity':
      continue
    answer = sample['answers']
    query_str = sample['query']
    query_id = sample['query_id']
    passages_dict = sample['passages']
    is_selected_lst = passages_dict["is_selected"]
    passage_text_lst = passages_dict["passage_text"]
    query_info = {
        'query_id': query_id,
        'answer': answer,
        'relevant_docs': []
    }

    for idx in range(len(is_selected_lst)):
      if is_selected_lst[idx] == 1:
        query_info['relevant_docs'].append(idx)

#     sample nào kh có câu trả lời đúng thì loại ra
    if query_info['relevant_docs'] == []:
      continue

    passage_text_lst_filter = [passage_text_lst[idx]
                               for idx in query_info['relevant_docs']]

    # thay thế mảng số bằng mảng chữ
    query_info['relevant_docs'] = passage_text_lst_filter

    queries_infos.append(query_info)
    queries.append(query_str)

  return queries, queries_infos
