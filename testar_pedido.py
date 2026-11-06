import json
from pedido import adicionar_ao_pedido, ver_pedido


def mostrar(resultado):
    print(json.dumps(resultado, indent=2, ensure_ascii=False))


mostrar(adicionar_ao_pedido(1, 2))
mostrar(adicionar_ao_pedido(4, 1))
mostrar(adicionar_ao_pedido(99, 1))
mostrar(adicionar_ao_pedido(1, 0))
mostrar(ver_pedido())