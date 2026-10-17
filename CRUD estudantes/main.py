from typing import Generator

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from schemas import CursosCreate, CursosResponse, EstudanteCreate, EstudanteResponse
import crud

# Criar as tabelas que ainda não existem
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Aluno")


# -------------------------------------------------------------------
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Estudante route----------------------------------------------------

# Criar Estudante-------------------------------------------------
@app.post("/estudante/")
def criar_estudante(dados: EstudanteCreate, db: Session = Depends(get_db)):
    estudante = crud.criar_estudante(db, dados)
    return estudante

# Listar Estudante
@app.get("/estudante/", response_model=list[EstudanteResponse])
def listar_estudante(db: Session = Depends(get_db)):
    return crud.listar_estudante(db)

# obter Estudante
@app.get("/estudante/pegar/", response_model=EstudanteResponse)
def listar_estudante(id: int, db: Session = Depends(get_db)):
    estudante = crud.obter_estudante(id, db)
    if estudante is None:
        raise HTTPException(status_code=404, detail="Student is not found !")
    return estudante

# atualizar Estudante
@app.put("/estudante/")
def atualizar(id: int, dados: EstudanteCreate, db: Session = Depends(get_db)):
    estudante = crud.obter_estudante(id, db)
    if estudante is None:
        raise HTTPException(status_code=404, detail="Student is not found !")
    return crud.atualizar_estudante(dados, estudante, db)

# eliminar estudante
@app.delete("/estudante/")
def eliminar_estudante(id: int, db: Session = Depends(get_db)):
    estudante = crud.obter_estudante(id, db)
    if estudante is None:
        raise HTTPException(status_code=404, detail="Student is not found")
    return crud.eliminar_estudante(estudante,db)
# -------------------------------------------------------------------
#criar cursos
@app.post("/curso/")
def criar_curso(dados:CursosCreate,db:Session = Depends(get_db)):
    return crud.criar_curso(db,dados)
#listar cursos
@app.get("/curso/", response_model=list[CursosResponse])
def listar_curso(db:Session = Depends(get_db)):
    return crud.listar_curso(db)
#obter curso
@app.get("/curso/pegar/", response_model= CursosResponse)
def obter_curso(id:int, db:Session = Depends(get_db)):
    curso = crud.obter_curso(id,db)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curse was not found !")
    return curso

@app.put("/curso/")
def atualizar_curso(id:int,dados:CursosCreate,db:Session = Depends(get_db)):
    curso = crud.obter_curso(id,db)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curse was not found !")
    crud.atualizar_curso(dados,curso,db)
    return {"Message": "Update with Success !"}
#deletar curso
@app.delete("/curso/delete/")
def deletar_curso(id:int, db:Session = Depends(get_db)):
    curso = crud.obter_curso(id,db)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curse was not found !")
    crud.deletar_curso(curso,db)
    return {"Message": "delete with Success !"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
