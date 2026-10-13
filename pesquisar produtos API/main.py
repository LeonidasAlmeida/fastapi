from fastapi import FastAPI
from util import Utill
import uvicorn

app = FastAPI()
op = Utill()


@app.get("/listar_nome_prod")
def retornar_json():
    return op.listar_por_nome_produto()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
