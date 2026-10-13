from data import lista_tarefa
from datetime import datetime


class Utill:
    lista = lista_tarefa

    # criar tarefa
    def criar_tarefa(self, tarefa: str):
        self.lista.append(
            {
                "id": len(self.lista) + 1,
                "tarefa": tarefa,
                "data_criacao": datetime.now().date(),
            }
        )
        return {"Criado com sucesso !"}

    # listar tarefa
    def listar_tarefa(self):
        return [tarefa for tarefa in self.lista]

    # eliminar tarefa
    def eliminar_tarefa(self, id: int):
        self.lista = [tarefa for tarefa in self.lista if tarefa["id"] != id]
        return {"Atualizado com sucesso !"}
