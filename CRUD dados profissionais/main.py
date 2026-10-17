from typing import Generator
from fastapi import FastAPI, Depends, HTTPException
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from models import Profissional
from schemas import ProfissionalCreate,ProfissionalResponse
import crud

# Criar as tabelas que ainda não existem
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Profissional")


# Criar e fechar uma sessão por pedido
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------CREATE -criarprofissional
@app.post("/profissional/",status_code=201)
def criar_prof(dados: ProfissionalCreate, db: Session = Depends(get_db)):
    return crud.criar_prof(db, dados)

# -----------------------------READ — listar profissional
@app.get("/profissional/", response_model = list[ProfissionalResponse])
def listar_prof(db:Session = Depends(get_db)):
    return crud.listar_prof(db)

# -----------------------------READ — listar profissional
@app.get("/profissional/pegar", response_model = ProfissionalResponse)
def pegar_prof(id:int,db:Session = Depends(get_db)):
    prof = crud.obter_prof(id, db)
    if prof is None:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")
    return prof

 # -----------------------------atualizar profissional
@app.put("/profissional/")
def atualizar_nota(id:int, dados:ProfissionalCreate, db:Session = Depends(get_db)):
    prof = crud.obter_prof(id, db) #procuro a tona na bd
    if prof is None: #verifico se exite resultado
        raise HTTPException(status_code=404, detail="Nota não encontrada") #disparo uma excepção
    return crud.atualizar_prof(dados,prof,db) # atualizo a nota

#------------------------------Delete nota
@app.delete("/profissional/")
def deletar_nota(id:int,db:Session = Depends(get_db)):
    prof = crud.obter_prof(db,id)
    if prof is None:
        raise HTTPException(status_code=404, detail="Prof não encontrada")
    else:
        crud.deletar_prof(db,prof)
    return {"Message":"Delected with sucesse !"}
    
    
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
