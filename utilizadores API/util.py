from data import utilizadores
from pprint import pprint
user = utilizadores

class Utill:
    def pesquisar_utilizadores(self,id:int):
        return [users for users in user if users["id"] == id]
    