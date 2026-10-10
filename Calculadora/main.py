from fastapi import FastAPI
from util import Calculos

app = FastAPI()
import uvicorn


@app.post("/soma")
def apresentacao_soma(calcular: Calculos):
    return {"resultado": calcular.soma()}


@app.post("/subtracao")
def apresentacao_sub(calcular: Calculos):
    return {"resultado": calcular.subtracao()}


@app.post("/multiplicacao")
def apresentacao_multi(calcular: Calculos):
    return {"resultado": calcular.multiplicacao()}


@app.post("/divisao")
def apresentacao_div(calcular: Calculos):
    return {"resultado": calcular.divisao()}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
