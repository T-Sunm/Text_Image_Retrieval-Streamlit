import json

def decode_escaped_strings(encoded_list):
  decoded_list = []
  for item in encoded_list:
    # Giải mã chuỗi nếu nó là chuỗi escape JSON
    decoded_string = json.loads(item) if isinstance(item, str) else item
    decoded_list.append(decoded_string)
  return decoded_list
 