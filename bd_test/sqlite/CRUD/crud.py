from sqlalchemy.orm import Session
from models import Produto
from schemas import ProdutoCreate


def criar_produto(db: Session, dados: ProdutoCreate):
    produto = Produto(**dados.model_dump())

    db.add(produto)
    db.commit()
    db.refresh(produto)

    return produto


def listar_produtos(db: Session):
    return db.query(Produto).all()


def obter_produto(db: Session, produto_id: int):
    return db.get(Produto, produto_id)


def atualizar_produto(db: Session, produto: Produto, dados: ProdutoCreate):
    produto.nome = dados.nome
    produto.preco = dados.preco
    produto.quantidade = dados.quantidade
    db.commit()
    db.refresh(produto)

    return produto


def eliminar_produto(db: Session, produto: Produto):
    db.delete(produto)
    db.commit()
