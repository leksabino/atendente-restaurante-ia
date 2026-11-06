import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from consultas import listar_pratos, buscar_prato
from pedido import adicionar_ao_pedido, ver_pedido

load_dotenv()

MODELO = "gemini-flash-lite-latest"

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

config = types.GenerateContentConfig(
    tools=[listar_pratos, buscar_prato, adicionar_ao_pedido, ver_pedido],
)

resposta = client.models.generate_content(
    model=MODELO,
    contents="Quero 2 hambúrgueres e 1 suco de laranja. Quanto fica o total?",
    config=config,
)
print(resposta.text)

for conteudo in resposta.automatic_function_calling_history or []:
    for parte in conteudo.parts:
        if parte.function_call:
            print("Chamou:", parte.function_call.name, dict(parte.function_call.args))