from tqdm import tqdm

def create_corpus_queries(subset):

    # Khai báo danh sách chứa tập câu truy vấn và tài liệu có liên quan:
  queries_infos = []
  queries = []
  corpus = []

  for sample in tqdm(subset, desc="Processing get data in dataset"):

    query_type = sample['query_type']
    if query_type != 'entity':
      continue
    query_str = sample['query']
    query_id = sample['query_id']
    passages_dict = sample['passages']
    is_selected_lst = passages_dict["is_selected"]
    passage_text_lst = passages_dict["passage_text"]
    query_info = {
        'query_id': query_id,
        'query': query_str,
        'relevant_docs': []
    }

    length_of_corpus = len(corpus)
    for idx in range(len(is_selected_lst)):
      if is_selected_lst[idx] == 1:
        #  mình sẽ gộp tất cả các passage_text_lst theo thứ tự vào trong 1 corpus chứ kh chia ra như sample
        #  vì vậy khi mình lưu 1 câu doc có is_selected == 1 thì mình current_len_corpus + idx để sau này truy xuất đúng index của nó
        doc_idx = length_of_corpus + idx
        query_info['relevant_docs'].append(doc_idx)

#     sample nào kh có câu trả lời đúng thì loại ra
    if query_info['relevant_docs'] == []:
      continue

    queries.append(query_str)
    queries_infos.append(query_info)

#     thêm nhiều phần tử vào mảng
    corpus.extend(passage_text_lst)

  return queries_infos, queries, corpus
