import time
from google.genai import errors
from atendente import client, MODELO, config
from consultas import _sem_acento

CASOS = [
    {
        "pergunta": "Quanto custa o bowl vegano?",
        "deve_conter_todos": ["34,00"],
    },
    {
        "pergunta": "O hambúrguer tem glúten?",
        "deve_conter_todos": ["gluten"],
    },
    {
        "pergunta": "Quais pratos veganos vocês têm?",
        "deve_conter_todos": ["bowl", "suco"],
    },
    {
        "pergunta": "Vocês têm pizza?",
        "deve_conter_algum": ["nao temos", "nao tem", "nao ha", "nao trabalhamos", "nao oferecemos"],
    },
    {
        "pergunta": "Quero pagar com cartão",
        "deve_conter_algum": ["nao tenho", "nao temos", "confirm"],
        "nao_deve_conter": ["sera realizado", "na entrega"],
    },
    {
        "pergunta": "Vocês entregam?",
        "deve_conter_algum": ["nao tenho", "nao temos", "confirm"],
        "nao_deve_conter": ["entregamos", "taxa de entrega"],
    },
    {
        "pergunta": "Quanto é o dólar hoje?",
        "deve_conter_algum": ["so posso", "restaurante", "cardapio"],
    },
        {
        "pergunta": "Vocês têm sanduíche de pernil?",
        "deve_conter_algum": ["nao temos", "nao tem", "nao ha", "nao trabalhamos", "nao oferecemos"],
    },
    {
        "pergunta": "O que vocês têm sem lactose?",
        "deve_conter_todos": ["bowl", "suco"],
    },
]


def responder(pergunta):
    chat = client.chats.create(model=MODELO, config=config)
    for _ in range(3):
        try:
            return chat.send_message(pergunta).text
        except errors.ServerError:
            time.sleep(5)
    return None


def avaliar(caso, resposta):
    if resposta is None:
        return False
    texto = _sem_acento(resposta)
    todos = [_sem_acento(t) for t in caso.get("deve_conter_todos", [])]
    algum = [_sem_acento(t) for t in caso.get("deve_conter_algum", [])]
    proibidos = [_sem_acento(t) for t in caso.get("nao_deve_conter", [])]
    if todos and not all(t in texto for t in todos):
        return False
    if algum and not any(t in texto for t in algum):
        return False
    if any(t in texto for t in proibidos):
        return False
    return True


acertos = 0
for caso in CASOS:
    resposta = responder(caso["pergunta"])
    ok = avaliar(caso, resposta)
    if ok:
        acertos += 1
    print("OK    " if ok else "FALHA ", caso["pergunta"])
    if not ok:
        print("      resposta:", resposta)

print(f"\n{acertos}/{len(CASOS)} casos corretos")