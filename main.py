from fastapi import FastAPI, File, UploadFile
from PIL import Image
import numpy as np
import io
import os

app = FastAPI()

path = 'test_images'

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))
    image_resized = image.resize((28, 28))
    image_matrix = np.array(image_resized)
    save_path = os.path.join(path, f"last_image")
    image_resized.save(save_path)
