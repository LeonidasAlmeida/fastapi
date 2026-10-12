from pydantic import BaseModel


class Utill(BaseModel):
    numero: int

    def calcular(self):
        resultado = self.numero % 2
        if resultado == 1:
            return "IMPAR"
        elif resultado == 0:
            return "PAR"
        else:
            return "Zero"



