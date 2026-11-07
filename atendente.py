import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors
from consultas import listar_pratos, buscar_prato, filtrar_por_dieta
from pedido import adicionar_ao_pedido, ver_pedido

load_dotenv()

MODELO = "gemini-flash-lite-latest"
TENTATIVAS = 3
ESPERA_SEGUNDOS = 5

INSTRUCAO = """Você é o atendente de um restaurante.
Use SEMPRE as ferramentas para consultar pratos, preços e alergênicos. Nunca invente pratos.
Se um prato não existir, diga que não temos.
Para montar o pedido, use adicionar_ao_pedido, e use ver_pedido para informar o total.
Você NÃO tem informações sobre pagamento, entrega, retirada, horários, endereço ou promoções. Se perguntarem sobre isso, diga que não tem essa informação e que o cliente deve confirmar com o restaurante. Nunca invente regras do restaurante.
Responda em até 4 linhas, em português.
Cumprimente só na primeira mensagem.
Recuse assuntos que não sejam do restaurante."""

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

config = types.GenerateContentConfig(
    system_instruction=INSTRUCAO,
    tools=[listar_pratos, buscar_prato, filtrar_por_dieta, adicionar_ao_pedido, ver_pedido],
)

chat = client.chats.create(model=MODELO, config=config)


def perguntar(texto):
    for tentativa in range(TENTATIVAS):
        try:
            return chat.send_message(texto).text
        except errors.ServerError:
            print(f"Servidor ocupado. Tentativa {tentativa + 1} de {TENTATIVAS}...")
            time.sleep(ESPERA_SEGUNDOS)
    return None


def main():
    print("Atendente pronto. Digite 'sair' para encerrar.")

    while True:
        texto = input("Você: ").strip()
        if texto.lower() == "sair":
            break
        if not texto:
            continue
        resposta = perguntar(texto)
        if resposta:
            print("Atendente:", resposta)
        else:
            print("Não consegui responder agora. Tente de novo em alguns minutos.")


if __name__ == "__main__":
    main()