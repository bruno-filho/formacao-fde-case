"""A régua de alçadas como código: o nível mínimo que cada caso exige.

Os dois servidores MCP (`ja-chegou` e `ja-chegou-analista`) importam daqui, para a trava ser uma só.
"""

from __future__ import annotations

from jachegou.base import NIVEIS, Base


def nivel_minimo(classificacao: str, nota: dict, base: Base) -> str:
    """O nível mais baixo que a régua aceita. O agente pode subir um caso, nunca descer."""
    r = base.regua
    if classificacao == "E6":
        return "bloqueio"
    if nota["valor_total"] > r["teto_coordenacao"] or base.fornecedores[nota["fornecedor_id"]]["bloqueado"]:
        return "diretoria"
    if classificacao in {"E5", "E7", "E8"}:
        return "coordenacao"
    if classificacao in {"E1", "E2", "E3", "E4"}:
        return "analista" if nota["valor_total"] <= r["teto_analista"] else "coordenacao"
    return "regra"


def nivel_mais_alto(*niveis: str | None) -> str:
    """O mais alto dos níveis, pela ordem da régua. Nível desconhecido ou vazio não conta."""
    validos = [n for n in niveis if n in NIVEIS]
    return max(validos, key=NIVEIS.index) if validos else "regra"
