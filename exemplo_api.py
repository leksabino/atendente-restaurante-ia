import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import errors

# Carrega as variáveis do arquivo .env
load_dotenv()

MODELO = "gemini-flash-lite-latest"
TENTATIVAS = 3
ESPERA_SEGUNDOS = 5

chave = os.environ.get("GEMINI_API_KEY")
if not chave:
    raise RuntimeError("Chave GEMINI_API_KEY não encontrada no .env")

client = genai.Client(api_key=chave)

deu_certo = False

for tentativa in range(TENTATIVAS):
    try:
        resposta = client.models.generate_content(
            model=MODELO,
            contents="Explique o que é uma API em duas frases.",
        )
        print(resposta.text)
        deu_certo = True
        break
    except errors.ServerError:
        print(f"Servidor ocupado. Tentativa {tentativa + 1} de {TENTATIVAS}...")
        time.sleep(ESPERA_SEGUNDOS)

if not deu_certo:
    print("Não deu certo agora. Tente de novo em alguns minutos.")