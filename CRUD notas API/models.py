from sqlalchemy import Column, Integer, String
from database import Base

class Nota(Base):
    __tablename__ = "notas"
    id = Column(Integer,primary_key=True, index=True)
    title = Column(String(100),nullable=False)
    comentario = Column(String(200),nullable=False)