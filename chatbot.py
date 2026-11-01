import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

MODELO = "gemini-flash-lite-latest"
TENTATIVAS = 3
ESPERA_SEGUNDOS = 5

chave = os.environ.get("GEMINI_API_KEY")
if not chave:
    raise RuntimeError("Chave GEMINI_API_KEY não encontrada no .env")

client = genai.Client(api_key=chave)
chat = client.chats.create(model=MODELO)


def perguntar(texto):
    for tentativa in range(TENTATIVAS):
        try:
            resposta = chat.send_message(texto)
            return resposta.text
        except errors.ServerError:
            print(f"Servidor ocupado. Tentativa {tentativa + 1} de {TENTATIVAS}...")
            time.sleep(ESPERA_SEGUNDOS)
    return None


print("Chatbot iniciado. Digite 'sair' para encerrar.")

while True:
    pergunta = input("Você: ").strip()
    if pergunta.lower() == "sair":
        break
    if not pergunta:
        continue

    resposta = perguntar(pergunta)
    if resposta is None:
        print("Bot: Não consegui responder agora. Tente de novo.")
    else:
        print("Bot:", resposta)

print("Até logo!")