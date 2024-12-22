from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from typing import List
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import numpy as np
import matplotlib.pyplot as plt
import torch
import nbimporter
from model_v1 import Net
import torch.nn.functional as F


MODEL_PATH = 'NET/net'

net = Net()
net.load_state_dict(torch.load(MODEL_PATH, weights_only=True))
net.eval()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MatrixRequest(BaseModel):
    matrix: List[List[int]]


def prepare_number(number):
    number = np.array(number, dtype='float32') / 255
    number = number.reshape(1, 1, 28, 28)
    return number


@app.post("/upload-image")
async def upload_image(request: MatrixRequest):
    matrix = np.array(request.matrix)
    matrix_n, matrix_m = matrix.shape
    number_n, number_m = 28, 28
    number = np.zeros((number_n, number_m))
    for i in range(0, matrix_n, 10):
        for j in range(0, matrix_m, 10):
            number[i // 10, j // 10] = np.sum(matrix[i : i + 10, j : j + 10]) / 100

    number = prepare_number(number)
    number_tensor = torch.tensor(number, dtype=torch.float32)

    with torch.no_grad():
        output = net(number_tensor)

    # Получаем предсказание
    predicted_class = torch.argmax(output, dim=1).item()
    probabilities = F.softmax(output, dim=1).numpy()
    print(probabilities)
    return {"message": "Matrix received successfully.", "predicted_class": predicted_class}



#uvicorn main:app  --reload --host 127.0.0.1 --port 8080
