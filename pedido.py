from consultas import pegar_prato

_itens = {}


def _formatar_reais(centavos: int) -> str:
    return f"R$ {centavos // 100},{centavos % 100:02d}"


def adicionar_ao_pedido(id_prato: int, quantidade: int) -> dict:
    """Adiciona um prato ao pedido do cliente. Use o id do prato (obtido pela busca ou pela lista). Se o cliente não disser a quantidade, use 1."""
    if quantidade < 1:
        return {"erro": "A quantidade deve ser pelo menos 1."}
    prato = pegar_prato(id_prato)
    if prato is None:
        return {"erro": f"Não existe prato com id {id_prato}."}
    _itens[id_prato] = _itens.get(id_prato, 0) + quantidade
    return {
        "ok": True,
        "prato": prato["nome"],
        "quantidade_no_pedido": _itens[id_prato],
    }


def ver_pedido() -> dict:
    """Mostra os itens do pedido atual e o total a pagar."""
    itens = []
    total = 0
    for id_prato, quantidade in _itens.items():
        prato = pegar_prato(id_prato)
        subtotal = prato["preco_centavos"] * quantidade
        total += subtotal
        itens.append(
            {
                "prato": prato["nome"],
                "quantidade": quantidade,
                "subtotal": _formatar_reais(subtotal),
            }
        )
    return {"itens": itens, "total": _formatar_reais(total)}