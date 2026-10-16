from pydantic import BaseModel, ConfigDict


class ContactoCreate(BaseModel):
    nome: str
    telemovel: str
    email: str


class ContactoResponse(BaseModel):
    id: int
    nome: str
    telemovel: str
    email: str

    model_config = ConfigDict(from_attributes=True)
