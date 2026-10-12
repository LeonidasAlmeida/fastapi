from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI()

class Pessoa(BaseModel):
    nome:str

@app.post("/resposta")
def resposta(resposta: Pessoa):
    return f"ola {resposta.nome} Bem vindo"

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
