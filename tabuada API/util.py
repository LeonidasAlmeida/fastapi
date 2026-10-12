from pydantic import BaseModel
class Tabuada(BaseModel):
    numero:int
    def calcular(self) ->dict:
        base=range(1,13)
        tabela={}
        for i in base:
            tabela[i]=self.numero * i
        return tabela
    
