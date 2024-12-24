import os

import numpy as np
import torch
import nbimporter
import torch.nn.functional as F

from typing import List
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from model_v1 import Net


load_dotenv()


MODEL_PATH = os.environ.get('MODEL_PATH')


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
            if number[i // 10, j // 10] > 255:
                number[i // 10, j // 10] = 255

    number = prepare_number(number)
    number_tensor = torch.tensor(number, dtype=torch.float32)

    with torch.no_grad():
        output = net(number_tensor)

    # Получаем предсказание
    predicted_class = torch.argmax(output, dim=1).item()
    probabilities = F.softmax(output, dim=1).numpy()
    pr_srt = [f"{prob:.5f}" for prob in probabilities[0]]
    
    return {
        "predicted_class": predicted_class,
        "probabilities" : pr_srt
    }
