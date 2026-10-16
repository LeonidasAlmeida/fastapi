from typing import Generator

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from schemas import NotasCreate, NotasResponse
import crud

# Criar as tabelas que ainda não existem
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Notas")


# Criar e fechar uma sessão por pedido
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------CREATE -criar produto
@app.post("/notas/", response_model=NotasResponse, status_code=201)
def criar_notas(dados: NotasCreate, db: Session = Depends(get_db)):
    return crud.criar_nota(db, dados)

# -----------------------------READ — listar produtos
@app.get("/notas/", response_model = list[NotasResponse])
def listar_notas(db:Session = Depends(get_db)):
    return crud.listar_nota(db)

# -----------------------------READ — listar produtos
@app.get("/notas/pegar", response_model = NotasResponse)
def pegar_nota(nota_id:int,db:Session = Depends(get_db)):
    nota = crud.obter_nota(db, nota_id)
    if nota is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return nota
 # -----------------------------READ — listar produtos
@app.put("/notas/", response_model=NotasResponse)
def atualizar_nota(nota_id:int, dados:NotasCreate, db:Session = Depends(get_db)):
    nota = crud.obter_nota(db, nota_id) #procuro a tona na bd

    if nota is None: #verifico se exite resultado
        raise HTTPException(status_code=404, detail="Nota não encontrada") #disparo uma excepção
    return crud.atualizar_nota(db,nota,dados) # atualizo a nota
#------------------------------Delete nota
@app.delete("/notas/")
def deletar_nota(nota_id:int,db:Session = Depends(get_db)):
    nota = crud.obter_nota(db,nota_id)
    
    if nota is None:
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    else:
        crud.deletar_nota(db,nota)
    return {"Message":"Delected with sucesse !"}
    
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
