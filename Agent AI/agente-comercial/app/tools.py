from data import vendas

#faturação total
def calcular_faturacao(lista_vendas):
    return sum([venda["quantidade"] * venda["preco_unitario"] for venda in lista_vendas ])

#faturação total
def filtrar_por_mes(lista_vendas, mes):
    return [venda for venda in lista_vendas if venda["mes"] == mes]

#faturação total
def faturacao_por_mes(lista_vendas, mes):
    vendas_mes = filtrar_por_mes(lista_vendas, mes)
    return calcular_faturacao(vendas_mes)



def faturacao_por_produto(lista_vendas):
    resultado = {}
    for venda in lista_vendas:
        produto = venda["produto"]

        faturacao = venda["quantidade"] * venda["preco_unitario"]

        if produto not in resultado:
            resultado[produto] = 0

        resultado[produto] += faturacao

    return resultado


def produto_mais_vendido(lista_vendas):
    quantidades = {}

    for venda in lista_vendas:
        produto = venda["produto"]

        if produto not in quantidades:
            quantidades[produto] = 0

        quantidades[produto] += venda["quantidade"]

    if not quantidades:
        return None

    return max(quantidades, key=quantidades.get)


def comparar_meses(lista_vendas, mes_atual, mes_anterior):
    faturacao_atual = faturacao_por_mes(lista_vendas, mes_atual)

    faturacao_anterior = faturacao_por_mes(lista_vendas, mes_anterior)

    diferenca = faturacao_atual - faturacao_anterior

    if faturacao_anterior == 0:
        variacao_percentual = None
    else:
        variacao_percentual = (diferenca / faturacao_anterior) * 100

    if diferenca > 0:
        situacao = "aumentou"
    elif diferenca < 0:
        situacao = "diminuiu"
    else:
        situacao = "manteve-se"

    return {
        "mes_atual": mes_atual,
        "mes_anterior": mes_anterior,
        "faturacao_atual": faturacao_atual,
        "faturacao_anterior": faturacao_anterior,
        "diferenca": diferenca,
        "variacao_percentual": variacao_percentual,
        "situacao": situacao,
    }
