import json
from envia_LLM import recebe_linhas_do_arquivo

# Etapa 1: Carregar o arquivo .txt
lista_resenhas = []

with open("Resenhas_App_ChatGPT.txt", "r", encoding="utf-8") as arquivo:
    for linha in arquivo:
        lista_resenhas.append(linha)

print(lista_resenhas)
print("\n\n")
print(lista_resenhas[0])

# Etapa 2: Enviar a lista para o modelo e 3: Transformar a resposta em um dicionário
lista_resenhas_json = []

for resenha in lista_resenhas:
    resenha_json = recebe_linhas_do_arquivo(resenha)
    resenha_dict = json.loads(resenha_json)
    lista_resenhas_json.append(resenha_dict)
