from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed"
)

def recebe_linhas_do_arquivo(linha):

    response = client.chat.completions.create(
        model="gemma-3-1b-it",
        messages=[
            {"role": "system", 
            "content": """Voce é um especialista em analise de sentimentos.
            Sua tarefa é analisar a resenha de um aplicativo, fornecida pelo usuário.
            Extraia o nome do usuário, a resenha original, traduza a resenha para o português classifique o sentimento como 'positiva', 'negativa' ou 'neutra'.
            Retorne a sua análise SOMENTE em formato JSON, como no exemplo abaixo:
            usuario: Nome do Usuário
            resenha_original: Texto original da resenha.
            traducao_portugues: Tradução da resenha para o português.
            avaliacao: positiva"
            Retorne a sua análise SOMENTE em formato JSON, como no exemplo abaixo:
            {
                "usuario": "Nome do Usuário",
                "resenha_original": "Texto original da resenha.",
                "traducao_portugues": "Tradução da resenha para o português.",
                "avaliacao": "positiva"
            }
            """},
            
            {"role": "user", 
            "content": f"Resenha: {linha}"}
        ],
        temperature=1.0
    )

    print(response.choices[0].message.content)