from pydantic import BaseModel, ConfigDict


class EstudanteCreate(BaseModel):
    nome_aluno: str
    idade: int


class EstudanteResponse(BaseModel):
    id: int
    nome_aluno: str
    idade: int
    model_config = ConfigDict(from_attributes=True)


class CursosCreate(BaseModel):
    nome_curso: str
    departamento: str


class CursosResponse(BaseModel):
    id: int
    nome_curso: str
    departamento: str
    model_config = ConfigDict(from_attributes=True)
