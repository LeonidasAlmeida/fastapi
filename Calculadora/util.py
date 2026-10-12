from pydantic import BaseModel

class Calculos(BaseModel):
    numero1: float = 0.0
    numero2: float = 0.0
    operacao: str = "+"
    resultado: float = 0.0

    def verificador(self) -> bool:
        return self.operacao in {"+", "-", "*", "/"}

    def soma(self) -> float:
        if not self.verificador():
            raise ValueError("Operação inválida")

        if self.operacao != "+":
            raise ValueError("A operação não é uma soma")

        self.resultado = self.numero1 + self.numero2
        return self.resultado

    def subtracao(self) -> float:
        if not self.verificador():
            raise ValueError("Operação inválida")

        if self.operacao != "-":
            raise ValueError("A operação não é uma subtração")

        self.resultado = self.numero1 - self.numero2
        return self.resultado

    def multiplicacao(self) -> float:
        if not self.verificador():
            raise ValueError("Operação inválida")

        if self.operacao != "*":
            raise ValueError("A operação não é uma multiplicação")

        self.resultado = self.numero1 * self.numero2
        return self.resultado

    def divisao(self) -> float:
        if not self.verificador():
            raise ValueError("Operação inválida")

        if self.operacao != "/":
            raise ValueError("A operação não é uma divisão")

        if self.numero2 == 0:
            raise ValueError("Não é possível dividir por zero")

        self.resultado = self.numero1 / self.numero2
        return self.resultado



##coisas novas raisen ValueError ("error ") usado para lançar uma execpcao 
##operador in {...} uo in [...] para iterar sobre um conjunto de dados para verificar uma condição