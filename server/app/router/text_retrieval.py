from fastapi import APIRouter, UploadFile, File, Form, status, HTTPException
from controller.text_retrieval import text_advanced_query, text_basic_query
text_retrival_router = APIRouter()

@text_retrival_router.post("/retrieval_basic", status_code=status.HTTP_200_OK)
async def retrieval_text_basic(query: str):
  try:
    results = text_basic_query(query)

    return results

  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@text_retrival_router.post("/retrieval_advanced", status_code=status.HTTP_200_OK)
async def retrieval_text_advanced(query: str):
  try:
    results = text_advanced_query(query)

    return results

  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
