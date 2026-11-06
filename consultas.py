import sqlite3

CAMINHO_BANCO = "restaurante.db"


def _conectar():
    con = sqlite3.connect(CAMINHO_BANCO)
    con.row_factory = sqlite3.Row
    return con


def listar_pratos():
    con = _conectar()
    linhas = con.execute(
        "SELECT id, nome, categoria, preco_centavos FROM pratos"
    ).fetchall()
    con.close()
    return [dict(linha) for linha in linhas]


def buscar_prato(nome):
    con = _conectar()
    linhas = con.execute(
        "SELECT * FROM pratos WHERE nome LIKE ?",
        (f"%{nome}%",),
    ).fetchall()
    con.close()
    return [dict(linha) for linha in linhas]