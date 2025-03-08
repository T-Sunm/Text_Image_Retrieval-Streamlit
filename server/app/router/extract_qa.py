from fastapi import APIRouter, status, HTTPException, Query

from controller.extract_qa import e2e_extractive_question_answering, extractive_question_answering
extract_question_answering_router = APIRouter()

@extract_question_answering_router.post(
    "/e2e_question_answering",
    status_code=status.HTTP_200_OK,
    summary="E2E Question Answering",
    description="Endpoint chạy pipeline Question Answering toàn diện từ đầu đến cuối",
    tags=["E2E QA"]   # bạn có thể gán 1 tag khác nếu muốn tách riêng
)
async def e2e_question_answering(query: str = Query(...)):
  print(query)
  try:
    answers = e2e_extractive_question_answering(query)

    return answers

  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@extract_question_answering_router.post(
    "/question_answering",
    status_code=status.HTTP_200_OK,
    summary="Extract Question Answering",
    description="Endpoint nhận query và context, trả về kết quả QA",
    tags=["QA with Context"]  # gán 1 tag khác nếu muốn tách riêng
)
async def extract_question_answering(query: str, context: str):
  print("query: ", query)
  print("context: ", context)
  try:
    answers = extractive_question_answering(query, context)

    return answers

  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
