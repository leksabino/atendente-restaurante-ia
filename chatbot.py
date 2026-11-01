import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types
from cardapio import CARDAPIO

load_dotenv()

MODELO = "gemini-flash-lite-latest"
TENTATIVAS = 3
ESPERA_SEGUNDOS = 5


def montar_cardapio():
    linhas = []
    for prato in CARDAPIO:
        ingredientes = ", ".join(prato["ingredientes"])
        alergenicos = ", ".join(prato["alergenicos"]) or "nenhum"
        linhas.append(
            f"- {prato['nome']} | categoria: {prato['categoria']} | "
            f"R$ {prato['preco']:.2f} | ingredientes: {ingredientes} | "
            f"alergênicos: {alergenicos}"
        )
    return "\n".join(linhas)


INSTRUCAO = (
    "Você é o assistente de atendimento de um restaurante. "
    "Responda em português, de forma simpática e em no máximo 4 linhas. "
    "Se a pergunta não for sobre o restaurante ou comida, "
    "diga educadamente que só ajuda com isso. "
    "Use SOMENTE o cardápio abaixo. Se o cliente pedir algo que não está nele, "
    "diga que não temos e sugira uma opção do cardápio. "
    "Nunca invente pratos, preços, ingredientes ou alergênicos.\n\n"
    "CARDÁPIO:\n" + montar_cardapio()
)

chave = os.environ.get("GEMINI_API_KEY")
if not chave:
    raise RuntimeError("Chave GEMINI_API_KEY não encontrada no .env")

client = genai.Client(api_key=chave)

chat = client.chats.create(
    model=MODELO,
    config=types.GenerateContentConfig(system_instruction=INSTRUCAO),
)


def perguntar(texto):
    for tentativa in range(TENTATIVAS):
        try:
            resposta = chat.send_message(texto)

            if not resposta.text:
                if resposta.candidates:
                    motivo = resposta.candidates[0].finish_reason
                else:
                    motivo = "sem candidatos"
                print(f"DEBUG: resposta vazia. Motivo: {motivo}")
                return "Não consegui montar uma resposta para essa pergunta. Pode reformular?"

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