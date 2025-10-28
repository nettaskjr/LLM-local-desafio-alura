from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="your_api_key_here"
)

response = client.chat.completions.create(
    model="gemma-3-1b-it",
    messages=[
        {"role": "system", "content": "Voce é um assistente de IA bem receptivo."},
        {"role": "user", "content": "O que é uma IA Generativa?"}
    ],
    temperature=1.0
)

print(response.choices[0].message.content)