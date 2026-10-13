from fastapi import FastAPI, Query
from util import Utill
import uvicorn

app = FastAPI()
op = Utill()


@app.post("/listar")
def retornar_json(
    limit: int = Query(default=5, ge=1, le=100), offset: int = Query(default=0, ge=0) # O parametro Query é usado para definir possiveis valores para uma propriedade default = o padrao, ge= o minimo, len=o maximo
):
    return op.listar_offset(offset,limit)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
