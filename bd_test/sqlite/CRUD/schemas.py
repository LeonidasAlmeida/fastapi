
from pydantic import BaseModel, ConfigDict


class ProdutoCreate(BaseModel):
    nome: str
    preco: float
    quantidade: int = 0


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    preco: float
    quantidade: int

    model_config = ConfigDict(from_attributes=True)
