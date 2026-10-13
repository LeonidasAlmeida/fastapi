from fastapi import FastAPI
from util import Utill
import uvicorn

app = FastAPI()
op = Utill()


@app.get("/listar")
def retornar_json():
    return op.listar()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
