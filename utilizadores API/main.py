from fastapi import FastAPI
from util import Utill
import uvicorn

app = FastAPI()
usuario = Utill()

@app.post("/consultar/")
def conultar_user(user:int):
    return usuario.pesquisar_utilizadores(user)

if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)