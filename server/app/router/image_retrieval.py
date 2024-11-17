from fastapi import APIRouter, UploadFile, File, Form, status, HTTPException
from controller.image_retrieval import image_query
image_retrival_router = APIRouter()

@image_retrival_router.post("/retrieval", status_code=status.HTTP_200_OK)
async def retrieval_image(file_upload: UploadFile = File(...)):
  try:
    # Đọc file upload
    file_name = file_upload.filename
    file_content = await file_upload.read()
    print(file_content)
    # Gọi hàm xử lý image_query
    results = image_query(file_content)

    return results

  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
