from pydantic import BaseModel,ConfigDict

class CategoriaCreate(BaseModel):
    name: str
    description: str
    
class CategoriaResponse(BaseModel):
    id: int
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)