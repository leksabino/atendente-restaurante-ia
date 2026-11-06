import sqlite3

CAMINHO_BANCO = "restaurante.db"


def _conectar():
    con = sqlite3.connect(CAMINHO_BANCO)
    con.row_factory = sqlite3.Row
    return con


def listar_pratos() -> list[dict]:
    """Lista todos os pratos do cardápio, com id, nome, categoria e preço em centavos."""
    con = _conectar()
    linhas = con.execute(
        "SELECT id, nome, categoria, preco_centavos FROM pratos"
    ).fetchall()
    con.close()
    return [dict(linha) for linha in linhas]


def buscar_prato(nome: str) -> list[dict]:
    """Busca pratos pelo nome (ou parte do nome). Devolve ingredientes, alergênicos, preço em centavos, tempo de preparo e se é vegano ou vegetariano. Devolve lista vazia se o prato não existe no cardápio."""
    con = _conectar()
    linhas = con.execute(
        "SELECT * FROM pratos WHERE nome LIKE ?",
        (f"%{nome}%",),
    ).fetchall()
    con.close()
    return [dict(linha) for linha in linhas]