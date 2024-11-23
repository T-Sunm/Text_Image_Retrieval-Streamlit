from fastapi import APIRouter, File, Form, status, HTTPException, Query

from controller.multimodal_retrieval import text_retrieval_img_query
multimodal_retrieval_router = APIRouter()


@multimodal_retrieval_router.post("/text_retrieval_img", status_code=status.HTTP_200_OK)
async def retrieval_text_basic(query: str = Query(...)):
  print(query)
  try:
    results = text_retrieval_img_query(query)

    return results

  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
