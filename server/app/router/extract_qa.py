from fastapi import APIRouter, status, HTTPException, Query

from controller.extract_qa import question_answering
extract_question_answering_router = APIRouter()

@extract_question_answering_router.post("/extract_question_answering", status_code=status.HTTP_200_OK)
async def extract_question_answering(query: str = Query(...)):
  print(query)
  try:
    answers = question_answering(query)

    return answers

  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
