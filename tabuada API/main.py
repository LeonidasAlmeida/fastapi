from fastapi import FastAPI
import uvicorn
from util import Tabuada

app = FastAPI()

@app.post("/tabuada")
def calcular(tabua: Tabuada):
    return tabua.calcular()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)