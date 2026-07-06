# config_loader.py
# Responsável por ler os arquivos de configuração (.txt)

def carregar_config(nome_arquivo):

    carros = []
    estrada_x = 100
    estrada_largura = 300

    with open(nome_arquivo, "r") as arquivo:

        for linha in arquivo:

            linha = linha.strip()

            if linha == "" or linha.startswith("#"):
                continue

            if linha.startswith("estrada_x="):
                estrada_x = int(linha.split("=")[1])

            elif linha.startswith("estrada_largura="):
                estrada_largura = int(linha.split("=")[1])

            elif linha.startswith("carro="):
                dados = linha.split("=")[1]
                x, y, r, g, b = map(int, dados.split(","))
                carros.append({"x": x, "y": y, "cor": (r, g, b)})

    return estrada_x, estrada_largura, carros
