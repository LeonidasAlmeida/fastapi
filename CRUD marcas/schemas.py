from pydantic import BaseModel, ConfigDict

class CategoriaCreate(BaseModel):
    nome_marca: str
    nome_produto: str

class CategoriaResponse(BaseModel):
    id: int
    nome_marca: str
    nome_produto: str
    
    model_config = ConfigDict(from_attributes=True)
    
    