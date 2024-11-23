from fastapi import FastAPI
import uvicorn
from router.image_retrieval import image_retrival_router
from router.text_retrieval import text_retrival_router
from router.multimodal_retrieval import multimodal_retrieval_router
app = FastAPI()

@app.get("/")
def read_root():
  return {"message": "Hello World"}


app.include_router(image_retrival_router, prefix="/image",
                   tags=["image retrieval"])

app.include_router(text_retrival_router, prefix="/text",
                   tags=["text retrieval"])
app.include_router(multimodal_retrieval_router, prefix="/multimodal",
                   tags=["multimodal retrieval"])
if __name__ == "__main__":
  uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
