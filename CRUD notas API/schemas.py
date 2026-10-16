from pydantic import BaseModel, ConfigDict


class NotasCreate(BaseModel):
    title: str
    comentario: str


class NotasResponse(BaseModel):
    id: int
    title: str
    comentario: str

    model_config = ConfigDict(from_attributes=True)
