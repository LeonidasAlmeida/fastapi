from fastapi import FastAPI, Body
from util import Utill
import uvicorn

app = FastAPI()
op = Utill()


@app.post("/listar")
def retornar_json(
categoria:str = Body(embed=True) # O parametro Query é usado para definir possiveis valores para uma propriedade default = o padrao, ge= o minimo, len=o maximo
):
    return op.listar(categoria)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
