import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from consultas import listar_pratos, buscar_prato

load_dotenv()

MODELO = "gemini-flash-lite-latest"

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

config = types.GenerateContentConfig(
    tools=[listar_pratos, buscar_prato],
)

resposta = client.models.generate_content(
    model=MODELO,
    contents="Me fala todos os pratos que vocês têm.",
    config=config,
)
print(resposta.text)