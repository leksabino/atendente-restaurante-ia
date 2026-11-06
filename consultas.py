import sqlite3
import unicodedata

CAMINHO_BANCO = "restaurante.db"

def _sem_acento(texto):
    decomposto = unicodedata.normalize("NFD", texto)
    sem_marcas = "".join(c for c in decomposto if unicodedata.category(c) != "Mn")
    return sem_marcas.lower()


def _conectar():
    con = sqlite3.connect(CAMINHO_BANCO)
    con.row_factory = sqlite3.Row
    con.create_function("sem_acento", 1, _sem_acento)
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
    palavras = _sem_acento(nome).split()
    if not palavras:
        return []
    condicoes = " AND ".join(["sem_acento(nome) LIKE ?"] * len(palavras))
    parametros = [f"%{palavra}%" for palavra in palavras]
    con = _conectar()
    linhas = con.execute(
        f"SELECT * FROM pratos WHERE {condicoes}", parametros
    ).fetchall()
    con.close()
    return [dict(linha) for linha in linhas]

def pegar_prato(id_prato: int):
    con = _conectar()
    linha = con.execute(
        "SELECT * FROM pratos WHERE id = ?", (id_prato,)
    ).fetchone()
    con.close()
    return dict(linha) if linha else None

def filtrar_por_dieta(dieta: str) -> list[dict]:
    """Lista os pratos que atendem a uma dieta. O parâmetro dieta deve ser 'vegano' ou 'vegetariano'. Devolve id, nome, categoria e preço em centavos."""
    dieta = _sem_acento(dieta)
    if dieta not in ("vegano", "vegetariano"):
        return []
    con = _conectar()
    linhas = con.execute(
        f"SELECT id, nome, categoria, preco_centavos FROM pratos WHERE {dieta} = 1"
    ).fetchall()
    con.close()
    return [dict(linha) for linha in linhas]