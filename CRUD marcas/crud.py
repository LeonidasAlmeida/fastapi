from sqlalchemy.orm import Session
from models import Marca
from schemas import CategoriaCreate


# controllers
# Criar marcas
def criar_marca(dados: CategoriaCreate, db: Session):
    marca = Marca(**dados.model_dump())
    db.add(marca)
    db.commit()
    db.refresh(marca)
    return {"Message": "Marca criada com sucesso !"}


# listar marcas
def listar_marcas(db: Session):
    return db.query(Marca).all()


# obter marca
def obter_marca(id_marca: int, db: Session):
    return db.get(Marca, id_marca)


# atualizar marca
def atualizar_marca(dados: CategoriaCreate, marca: Marca, db: Session):
    marca.nome_marca = dados.nome_marca
    marca.nome_produto = dados.nome_produto
    db.commit()
    db.refresh(marca)
    return {"Message": "Marca atualizada com sucesso !"}

#eliminar marca
def deletar_marca(marca: Marca, db: Session):
    db.delete(marca)
    db.commit()
    return {"Message": "Marca eliminada com sucesso !"}