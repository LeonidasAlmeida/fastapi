from typing import Generator
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from schemas import ContactoCreate, ContactoResponse
import crud

# Criar as tabelas que ainda não existem
Base.metadata.create_all(bind=engine)
# criar o app
app = FastAPI(title="API de Contactos")


# abrir e fechar sessão
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------Rotas
# criar contacto
@app.post("/contacto")
def criar_contacto(dados: ContactoCreate, db: Session = Depends(get_db)):
    return crud.criar_contacto(db, dados)


# listar contactos
@app.get("/contacto/", response_model=list[ContactoResponse])
def listar_contacto(db: Session = Depends(get_db)):
    return crud.listar_contacto(db)


# lista um contacto
@app.get("/contacto/pegar", response_model=ContactoResponse)
def get_contacto(id, db: Session = Depends(get_db)):
    contacto = crud.obter_contacto(id, db)
    if contacto is None:
        raise HTTPException(status_code=404, detail="Contact was not found !")
    return contacto


# atualizar contacto
@app.put("/contacto/")
def atualizar_contacto(dado: ContactoCreate, id: int, db: Session = Depends(get_db)):
    contato = crud.obter_contacto(id, db)
    if contato is None:
        raise HTTPException(status_code=404, detail="Contact was not found !")
    return crud.atualizar_contacto(contato, dado, db)


# eliminar contacto
@app.delete("/contacto/")
def delete_contacto(id: int, db: Session = Depends(get_db)):
    contacto = crud.obter_contacto(id, db)
    if contacto is None:
        raise HTTPException(status_code=404, detail="Contact was not found !")
    return crud.deletar_contacto(contacto, db)


# criar o uvicorn para executar o servidor
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
