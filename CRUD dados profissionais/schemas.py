from pydantic import BaseModel, ConfigDict


class ProfissionalCreate(BaseModel):
    nome_funcionario: str
    cargo: str


class ProfissionalResponse(BaseModel):
    id: int
    nome_funcionario: str
    cargo: str
    model_config = ConfigDict(from_attributes=True)
