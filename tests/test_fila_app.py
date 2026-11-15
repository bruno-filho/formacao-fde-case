"""Testes do MCP App da fila (issue 02 do grupo 2). Offline: não abrem o host."""

from __future__ import annotations

import asyncio
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from mcp import Client  # noqa: E402

from mcp_server import analista  # noqa: E402

URI = "ui://ja-chegou-analista/fila"
HTML = RAIZ / "mcp_server" / "ui" / "fila.html"


def _rodar(corrotina):
    return asyncio.run(corrotina)


def test_mostrar_fila_declara_o_recurso_de_ui():
    async def ver():
        async with Client(analista.servidor) as c:
            return {t.name: t for t in (await c.list_tools()).tools}["mostrar_fila"].meta

    assert _rodar(ver()) == {"ui": {"resourceUri": URI}}


def test_recurso_servido_com_o_tipo_de_mcp_app():
    async def ler():
        async with Client(analista.servidor) as c:
            return (await c.read_resource(URI)).contents[0]

    conteudo = _rodar(ler())
    assert conteudo.mime_type == "text/html;profile=mcp-app"
    assert "Fila do analista" in conteudo.text


def test_mostrar_fila_devolve_a_mesma_fila_em_texto(tmp_path, monkeypatch):
    """Num host sem MCP Apps, o resultado em texto é a fila, igual à de listar_fila."""
    monkeypatch.setattr(analista, "SAIDAS", tmp_path)
    monkeypatch.setenv("FDE_ANALISTA_NIVEL", "coordenacao")
    nota = next(iter(analista.base.notas.values()))
    (tmp_path / "propostas.jsonl").write_text(json.dumps({
        "nota_id": nota["nota_id"], "classificacao": "E5", "acao_doca": "recusar",
        "encaminhamento": "coordenacao", "valor_em_risco": 10.0, "justificativa": "teste da tela"}) + "\n",
        encoding="utf-8")
    if analista.base.fornecedores[nota["fornecedor_id"]]["bloqueado"] or nota["valor_total"] > 100_000:
        return
    assert analista.mostrar_fila() == analista.listar_fila()

    async def chamar():
        async with Client(analista.servidor) as c:
            return await c.call_tool("mostrar_fila", {})

    texto = _rodar(chamar()).content[0].text
    assert nota["nota_id"] in texto and "total_valor_em_risco" in texto


def test_a_tela_so_chama_ler_proposta_e_decidir():
    html = HTML.read_text(encoding="utf-8")
    chamadas = set(re.findall(r'chamarTool\("([a-z_]+)"', html))
    assert chamadas == {"ler_proposta", "decidir"}
    assert html.count('"tools/call"') == 1, "toda chamada de tool passa por chamarTool"


def test_a_tela_mostra_a_recusa_da_tool_sem_contornar():
    html = HTML.read_text(encoding="utf-8")
    assert "r.erro" in html
    assert "gravada" in html
