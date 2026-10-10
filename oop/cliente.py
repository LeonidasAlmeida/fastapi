from pessoa import Pessoa

p1 = Pessoa("leonidas", 20, 1.9)
model = {'nome': "name", 'peso': 0, 'altura': 0.1}
listaP = Pessoa(**model)
print(listaP.nome)
