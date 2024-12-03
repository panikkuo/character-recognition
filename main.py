from typing import Union
from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI()

@app.get("/")
async def read_root():
    return {"sosi chto?": "hui"}
    # return """<style>.someclass{font-size: 128px; color: red; text-align: center;}.someclass:hover { transform: translate(100px, 100px); transition-duration: 2000ms; opacity: 0}</style><h1 class=\"someclass\">Наведи на меня</h1>"""

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}