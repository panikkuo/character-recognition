from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from typing import List
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Создаем объект приложения FastAPI
app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MatrixRequest(BaseModel):
    matrix: List[List[int]]


# @app.options("/upload-image")
# async def options_handler():
#     return JSONResponse(
#         content={"success": "200"},
#         headers={
#             "Access-Control-Allow-Origin": "*",
#             "Access-Control-Allow-Methods": "*",
#             "Access-Control-Allow-Headers": "*",
#         },
#     )


@app.post("/upload-image")
async def upload_image(request: MatrixRequest):
    matrix = request.matrix
    print("Received matrix:", matrix)
    return {"message": "Matrix received successfully."}

#uvicorn main:app  --reload --host 127.0.0.1 --port 8080