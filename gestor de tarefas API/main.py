from fastapi import FastAPI,Body
import uvicorn
from util import Utill

app = FastAPI()
tarefas = Utill()
@app.post("/tarefa/criar")
def criar_tarefas(tarefa: str = Body(embed=True)):
    return tarefas.criar_tarefa(tarefa)

@app.post("/tarefa/eliminar")
def criar_tarefas(id:int):
    return tarefas.eliminar_tarefa(id)

@app.get("/tarefa/listar")
def criar_tarefas():
    return tarefas.listar_tarefa()


if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)