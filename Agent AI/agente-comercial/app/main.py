
from agent import perguntar_agente

contexto = {}

while True:
    pergunta = input(
        "\nPergunta comercial (ou 'sair' para terminar): "
    ).strip()

    if pergunta.lower() == "sair":
        print("Agente terminado.")
        break

    if not pergunta:
        continue

    try:
        resposta, contexto = perguntar_agente(
            pergunta,
            contexto
        )
        print(f"\nAgente:\n{resposta}")

    except Exception as erro:
        print(f"\nErro ao processar a pergunta: {erro}")
