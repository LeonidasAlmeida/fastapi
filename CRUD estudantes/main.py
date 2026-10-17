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
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
