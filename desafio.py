from openai import OpenAI
import json

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed"
)

def carregar_resenhas(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
        return linhas
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {nome_do_arquivo}")
        return []

def analisar_sentimento(resenha):
    prompt_sistema = """
    Você é um assistente de análise de sentimentos.
    Sua tarefa é analisar a resenha de um aplicativo, fornecida pelo usuário.
    Extraia o nome do usuário, a resenha original, traduza a resenha para o português e classifique o sentimento como 'positiva', 'negativa' ou 'neutra'.
    Retorne a sua análise SOMENTE em formato JSON, como no exemplo abaixo:

    {
        "usuario": "Nome do Usuário",
        "resenha_original": "Texto original da resenha.",
        "traducao_portugues": "Tradução da resenha para o português.",
        "avaliacao": "positiva"
    }
    """

    response = client.chat.completions.create(
        model="gemma-3-1b-it",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": resenha}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

def salvar_json(lista, nome_arquivo):
    """Salva uma lista de dicionários em um arquivo JSON."""
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)

def consolidar_analises(lista_de_analises):
    """
    Conta as avaliações e consolida as análises em uma única string.
    Retorna a contagem e a string consolidada.
    """
    # 1. Contar as avaliações
    contagem = {
        "positivas": 0,
        "negativas": 0,
        "neutras": 0
    }
    for analise in lista_de_analises:
        avaliacao = analise.get('avaliacao', '').lower()
        if avaliacao == 'positiva':
            contagem['positivas'] += 1
        elif avaliacao == 'negativa':
            contagem['negativas'] += 1
        elif avaliacao == 'neutra':
            contagem['neutras'] += 1

    # 2. Unir os itens em uma string
    itens_formatados = []
    for analise in lista_de_analises:
        item_str = f"Usuário: {analise.get('usuario')}\nAvaliação: {analise.get('avaliacao')}\nTradução: {analise.get('traducao_portugues')}"
        itens_formatados.append(item_str)
    
    string_consolidada = "\n\n---\n\n".join(itens_formatados)
    return contagem, string_consolidada

lista_resenhas = carregar_resenhas("Resenhas_App_ChatGPT.txt")
lista_analisada = []

if lista_resenhas:
    print("Arquivo carregado com sucesso!")
    print("Iniciando análise de sentimentos...")
    for resenha in lista_resenhas:
        try:
            print(f"Analisando a resenha: {resenha.strip()}")
            analise = analisar_sentimento(resenha)

            # Limpeza e extração do JSON da resposta do modelo
            start_json = analise.find('{')
            end_json = analise.rfind('}') + 1
            if start_json == -1 or end_json == 0:
                print(f"   -> Resposta inválida do modelo (não contém JSON): {analise}")
                continue

            json_str = analise[start_json:end_json]
            dados_json = json.loads(json_str)
            lista_analisada.append(dados_json)
        except Exception as e:
            print(f"   -> Erro ao processar a resenha: {resenha.strip()}\n   -> Erro: {e}")

print("\nAnálise concluída!")
if lista_analisada:
    nome_arquivo_saida = "analises_sentimento.json"
    salvar_json(lista_analisada, nome_arquivo_saida)
    print(f"Resultados salvos com sucesso em '{nome_arquivo_saida}'!")

    # Passo 3: Consolidar e contar os resultados
    contagem_avaliacoes, string_geral = consolidar_analises(lista_analisada)

    print("\n--- Contagem de Avaliações ---")
    print(f"Positivas: {contagem_avaliacoes['positivas']}")
    print(f"Negativas: {contagem_avaliacoes['negativas']}")
    print(f"Neutras:   {contagem_avaliacoes['neutras']}")

    # Opcional: Imprimir a string consolidada (pode ser muito longa)
    # print("\n--- String Consolidada ---")
    # print(string_geral)
