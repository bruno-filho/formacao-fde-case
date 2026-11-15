"""Testes do servidor do analista (`ja-chegou-analista`). Offline: propostas sintéticas sobre a base real."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from jachegou.base import Base  # noqa: E402
from jachegou.regua import nivel_minimo  # noqa: E402
from mcp_server import analista  # noqa: E402

BASE = Base()
TETO_ANALISTA = BASE.regua["teto_analista"]


def _escolher(usadas: set[str], classificacao: str, nivel: str, bloqueado: bool = False) -> str:
    """A primeira nota ainda não usada que a régua põe no nível pedido para a classificação."""
    for nota_id, nota in BASE.notas.items():
        if nota_id in usadas or BASE.fornecedores[nota["fornecedor_id"]]["bloqueado"] != bloqueado:
            continue
        if nivel_minimo(classificacao, nota, BASE) == nivel:
            usadas.add(nota_id)
            return nota_id
    raise AssertionError(f"nenhuma nota {classificacao} de {nivel}")


def _proposta(nota_id: str, classificacao: str, encaminhamento: str, valor_em_risco: float | None,
              acao_doca: str = "receber_parcial", **extra) -> dict:
    return {"nota_id": nota_id, "classificacao": classificacao, "acao_doca": acao_doca,
            "encaminhamento": encaminhamento, "valor_em_risco": valor_em_risco,
            "justificativa": "proposta sintética de teste", "origem": "teste"} | extra


@pytest.fixture
def casos(tmp_path, monkeypatch) -> dict[str, str]:
    """Grava saidas/propostas.jsonl com um caso de cada tipo e devolve as notas por nome do caso."""
    monkeypatch.setattr(analista, "SAIDAS", tmp_path)
    monkeypatch.setenv("FDE_ANALISTA_ID", "analista-1")
    monkeypatch.setenv("FDE_ANALISTA_NIVEL", "analista")
    monkeypatch.setenv("FDE_ARQUIVO_PROPOSTAS", "propostas.jsonl")
    usadas: set[str] = set()
    c = {
        "e1": _escolher(usadas, "E1", "analista"),
        "e3": _escolher(usadas, "E3", "analista"),
        "sobe": _escolher(usadas, "E4", "analista"),
        "sem_risco": _escolher(usadas, "E2", "analista"),
        "e5": _escolher(usadas, "E5", "coordenacao"),
        "e6": _escolher(usadas, "E6", "bloqueio"),
        "bloqueado": _escolher(usadas, "E1", "diretoria", bloqueado=True),
        "match": _escolher(usadas, "match", "regra"),
        "recusada": _escolher(usadas, "E1", "analista"),
        "ultima": _escolher(usadas, "E1", "analista"),
    }
    linhas = [
        _proposta(c["e1"], "E1", "analista", 500.0, acao_doca="receber"),
        _proposta(c["e3"], "E3", "analista", 1500.0),
        _proposta(c["sobe"], "E4", "regra", 50.0),  # abaixo da régua no arquivo: sobe para analista
        _proposta(c["sem_risco"], "E2", "analista", None),
        _proposta(c["e5"], "E5", "coordenacao", 9000.0, acao_doca="recusar"),
        _proposta(c["e6"], "E6", "bloqueio", 99999.0, acao_doca="recusar"),
        _proposta(c["bloqueado"], "E1", "analista", 88888.0),  # fornecedor bloqueado: diretoria pela régua
        _proposta(c["match"], "match", "regra", 0.0, acao_doca="receber"),
        _proposta(c["recusada"], "E1", "regra", 70000.0, recusada="regua"),
        _proposta(c["ultima"], "E5", "coordenacao", 77777.0),
        _proposta(c["ultima"], "E1", "analista", 800.0),  # a última vale
    ]
    (tmp_path / "propostas.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in linhas),
                                              encoding="utf-8")
    return c


def _decisoes(tmp_path_saidas: Path) -> list[dict]:
    arquivo = tmp_path_saidas / "decisoes.jsonl"
    if not arquivo.is_file():
        return []
    return [json.loads(x) for x in arquivo.read_text(encoding="utf-8").splitlines() if x.strip()]


# AC-1: a fila


def test_fila_do_analista_ordenada_por_valor_em_risco(casos):
    r = analista.listar_fila()
    ids = [x["nota_id"] for x in r["fila"]]
    assert ids == [casos["e3"], casos["ultima"], casos["e1"], casos["sobe"], casos["sem_risco"]]
    assert r["total_valor_em_risco"] == 1500.0 + 800.0 + 500.0 + 50.0
    assert r["nivel_do_analista"] == "analista"
    assert all(x["encaminhamento"] == "analista" for x in r["fila"])


def test_fila_deixa_fora_coordenacao_diretoria_bloqueio_regra_e_recusada(casos):
    ids = {x["nota_id"] for x in analista.listar_fila()["fila"]}
    for caso in ("e5", "e6", "bloqueado", "match", "recusada"):
        assert casos[caso] not in ids, caso


def test_coordenacao_ve_a_propria_fila_e_a_do_analista(casos, monkeypatch):
    monkeypatch.setenv("FDE_ANALISTA_NIVEL", "coordenacao")
    r = analista.listar_fila()
    ids = [x["nota_id"] for x in r["fila"]]
    assert ids[0] == casos["e5"] and len(ids) == 6
    assert casos["e6"] not in ids and casos["bloqueado"] not in ids
    assert [x["nota_id"] for x in analista.listar_fila(nivel="coordenacao")["fila"]] == [casos["e5"]]
    assert casos["e5"] not in {x["nota_id"] for x in analista.listar_fila(nivel="analista")["fila"]}


def test_filtro_de_nivel_nao_amplia_acima_do_ambiente(casos):
    r = analista.listar_fila(nivel="coordenacao")
    assert casos["e5"] not in {x["nota_id"] for x in r["fila"]}
    assert "erro" in analista.listar_fila(nivel="diretoria")


def test_encaminhamento_abaixo_da_regua_entra_com_o_minimo(casos):
    linha = next(x for x in analista.listar_fila()["fila"] if x["nota_id"] == casos["sobe"])
    assert linha["encaminhamento"] == "analista"


def test_filtro_por_destino(casos):
    destino = BASE.notas[casos["e1"]]["destino"]
    fila = analista.listar_fila(destino=destino)["fila"]
    assert fila and all(x["destino"] == destino for x in fila)


def test_linha_da_fila_tem_os_campos(casos):
    linha = analista.listar_fila()["fila"][0]
    nota = BASE.notas[linha["nota_id"]]
    assert linha["fornecedor_id"] == nota["fornecedor_id"]
    assert linha["fornecedor"] == BASE.fornecedores[nota["fornecedor_id"]]["razao_social"]
    assert linha["valor_total"] == nota["valor_total"]
    assert {"destino", "classificacao", "acao_doca", "encaminhamento", "valor_em_risco"} <= set(linha)


def test_sem_propostas_cai_no_baseline(tmp_path, monkeypatch):
    monkeypatch.setattr(analista, "SAIDAS", tmp_path)
    monkeypatch.setenv("FDE_ANALISTA_NIVEL", "analista")
    monkeypatch.delenv("FDE_ARQUIVO_PROPOSTAS", raising=False)
    nota_id = _escolher(set(), "E1", "analista")
    (tmp_path / "baseline.jsonl").write_text(json.dumps(_proposta(nota_id, "E1", "analista", 10.0)) + "\n",
                                             encoding="utf-8")
    assert [x["nota_id"] for x in analista.listar_fila()["fila"]] == [nota_id]


def test_ler_proposta(casos):
    r = analista.ler_proposta(casos["bloqueado"])
    assert r["fornecedor"]["bloqueado"] is True
    assert r["nivel_minimo_regua"] == "diretoria" and r["encaminhamento"] == "diretoria"
    assert r["decidida"] is False
    assert "Ordem" in r["comparar_itens"]
    assert r["nota"]["valor_total"] == BASE.notas[casos["bloqueado"]]["valor_total"]
    assert "erro" in analista.ler_proposta("NF-999")
    assert "erro" in analista.ler_proposta(next(n for n in BASE.notas if n not in casos.values()))


# AC-2 e AC-4: a decisão


def test_decidir_grava_a_linha(casos):
    r = analista.decidir(casos["e1"], "aprovar", "  contagem confere com a nota  ")
    assert r["gravada"] is True
    [linha] = _decisoes(analista.SAIDAS)
    assert linha == r["decisao"]
    assert linha["nota_id"] == casos["e1"] and linha["decisao"] == "aprovar"
    assert linha["acao_doca"] == "receber" and linha["acao_doca_proposta"] == "receber"
    assert linha["nivel_minimo"] == "analista"
    assert linha["decidido_por"] == "analista-1" and linha["nivel_de_quem_decidiu"] == "analista"
    assert linha["justificativa"] == "contagem confere com a nota"
    assert len(linha["decidido_em"]) == 19


def test_alterar_troca_a_acao(casos):
    r = analista.decidir(casos["e3"], "alterar", "a doca contou menos caixas", acao_doca="recusar")
    assert r["decisao"]["decisao"] == "alterar"
    assert r["decisao"]["acao_doca"] == "recusar" and r["decisao"]["acao_doca_proposta"] == "receber_parcial"


def test_alterar_para_a_mesma_acao_vira_aprovar(casos):
    r = analista.decidir(casos["e3"], "alterar", "mantém a devolução parcial", acao_doca="receber_parcial")
    assert r["gravada"] is True and r["decisao"]["decisao"] == "aprovar"


def test_decidida_sai_da_fila_e_nao_aceita_segunda(casos):
    assert analista.decidir(casos["e1"], "aprovar", "contagem confere com a nota")["gravada"]
    assert casos["e1"] not in {x["nota_id"] for x in analista.listar_fila()["fila"]}
    assert analista.ler_proposta(casos["e1"])["decidida"] is True
    r = analista.decidir(casos["e1"], "alterar", "mudei de ideia depois", acao_doca="recusar")
    assert r["gravada"] is False and "já foi decidida" in r["erro"]
    assert len(_decisoes(analista.SAIDAS)) == 1


def test_coordenacao_decide_coordenacao(casos, monkeypatch):
    monkeypatch.setenv("FDE_ANALISTA_NIVEL", "coordenacao")
    r = analista.decidir(casos["e5"], "aprovar", "dossiê da exceção confere")
    assert r["gravada"] is True and r["decisao"]["nivel_minimo"] == "coordenacao"


# AC-3: cada recusa, sem gravar


RECUSAS = {
    "sem_id": ({"FDE_ANALISTA_ID": ""}, "e1", "aprovar", "justificativa boa", None, "FDE_ANALISTA_ID"),
    "nota_inexistente": ({}, "NF-999", "aprovar", "justificativa boa", None, "não encontrada"),
    "sem_proposta": ({}, None, "aprovar", "justificativa boa", None, "não tem proposta"),
    "acima_do_nivel": ({}, "e5", "aprovar", "justificativa boa", None, "acima do nível"),
    "diretoria": ({}, "bloqueado", "aprovar", "justificativa boa", None, "diretoria"),
    "diretoria_para_coordenacao": ({"FDE_ANALISTA_NIVEL": "coordenacao"}, "bloqueado", "aprovar",
                                   "justificativa boa", None, "diretoria"),
    "bloqueio": ({"FDE_ANALISTA_NIVEL": "coordenacao"}, "e6", "aprovar", "justificativa boa", None, "bloqueio"),
    "regra": ({}, "match", "aprovar", "justificativa boa", None, "não espera pessoa"),
    "recusada_nao_conta": ({}, "recusada", "aprovar", "justificativa boa", None, "não tem proposta"),
    "nivel_do_ambiente_invalido": ({"FDE_ANALISTA_NIVEL": "diretoria"}, "e1", "aprovar", "justificativa boa",
                                   None, "FDE_ANALISTA_NIVEL"),
    "decisao_invalida": ({}, "e1", "pagar", "justificativa boa", None, "decisao"),
    "alterar_sem_acao": ({}, "e1", "alterar", "justificativa boa", None, "acao_doca"),
    "alterar_acao_invalida": ({}, "e1", "alterar", "justificativa boa", "pagar", "acao_doca"),
    "justificativa_curta": ({}, "e1", "aprovar", "   curta   ", None, "10 caracteres"),
}


@pytest.mark.parametrize("caso", RECUSAS)
def test_decidir_recusa_sem_gravar(casos, monkeypatch, caso):
    env, nota, decisao, justificativa, acao, trecho = RECUSAS[caso]
    for chave, valor in env.items():
        monkeypatch.setenv(chave, valor)
    if nota is None:
        nota_id = next(n for n in BASE.notas if n not in casos.values())
    else:
        nota_id = casos.get(nota, nota)
    r = analista.decidir(nota_id, decisao, justificativa, acao_doca=acao)
    assert r["gravada"] is False
    assert trecho in r["erro"]
    assert _decisoes(analista.SAIDAS) == []


# AC-5: a delegação ao motor


def test_delegar_ao_motor_so_grava_o_pedido(casos):
    r = analista.delegar_ao_motor()
    assert r["gravado"] is True and r["dry_run"] is True
    aprovaria = {x["nota_id"] for x in r["motor_aprovaria"]}
    com_pessoa = {x["nota_id"]: x["motivo"] for x in r["fica_com_pessoa"]}
    assert aprovaria == {casos["e1"], casos["e3"], casos["sobe"], casos["ultima"]}
    assert set(com_pessoa) == {casos["sem_risco"]} and "E2" in com_pessoa[casos["sem_risco"]]
    assert _decisoes(analista.SAIDAS) == []
    [pedido] = [json.loads(x) for x in (analista.SAIDAS / "delegacoes.jsonl").read_text(encoding="utf-8").splitlines()]
    assert pedido["dry_run"] is True and pedido["solicitado_por"] == "analista-1"
    assert pedido["resumo"] == {"avaliadas": 5, "motor_aprovaria": 4, "fica_com_pessoa": 1}
    assert len(analista.listar_fila()["fila"]) == 5, "nada saiu da fila"


def test_delegar_ao_motor_com_filtros_e_sem_id(casos, monkeypatch):
    r = analista.delegar_ao_motor(classificacoes=["E3"])
    assert [x["nota_id"] for x in r["motor_aprovaria"]] == [casos["e3"]] and r["fica_com_pessoa"] == []
    r = analista.delegar_ao_motor(nota_ids=[casos["e5"]])
    assert r["pedido"]["resumo"]["avaliadas"] == 0, "coordenação não está na fila do analista"
    monkeypatch.setenv("FDE_ANALISTA_ID", "")
    assert analista.delegar_ao_motor()["gravado"] is False


# O servidor pelo cliente MCP


def test_servidor_mcp_expoe_as_tools_e_trava_a_alcada(casos):
    from mcp import Client

    async def rodar():
        async with Client(analista.servidor) as c:
            nomes = {t.name for t in (await c.list_tools()).tools}
            assert nomes == {"listar_fila", "ler_proposta", "decidir", "delegar_ao_motor"}
            fila = json.loads((await c.call_tool("listar_fila", {})).content[0].text)
            assert fila["fila"][0]["nota_id"] == casos["e3"]
            r = json.loads((await c.call_tool("decidir", {"nota_id": casos["e5"], "decisao": "aprovar",
                                                          "justificativa": "tentando acima da alçada"})).content[0].text)
            assert r["gravada"] is False
            r = json.loads((await c.call_tool("decidir", {"nota_id": casos["e1"], "decisao": "aprovar",
                                                          "justificativa": "contagem confere com a nota"})).content[0].text)
            assert r["gravada"] is True

    asyncio.run(rodar())
    assert [d["nota_id"] for d in _decisoes(analista.SAIDAS)] == [casos["e1"]]


def test_mcp_json_registra_o_servidor_do_analista():
    env = json.loads((RAIZ / ".mcp.json").read_text(encoding="utf-8"))["mcpServers"]["ja-chegou-analista"]
    assert env["args"][-1] == "mcp_server/analista.py"
    assert env["env"] == {"FDE_ANALISTA_ID": "${FDE_ANALISTA_ID:-}",
                          "FDE_ANALISTA_NIVEL": "${FDE_ANALISTA_NIVEL:-analista}",
                          "FDE_ARQUIVO_PROPOSTAS": "${FDE_ARQUIVO_PROPOSTAS:-propostas.jsonl}"}


def test_os_dois_servidores_usam_a_mesma_regua():
    from mcp_server import servidor

    for nota in BASE.notas.values():
        for classificacao in ("match", "E1", "E5", "E6"):
            assert servidor.nivel_minimo(classificacao, nota) == nivel_minimo(classificacao, nota, BASE)
    assert "def nivel_minimo(classificacao: str, nota: dict, base" not in (RAIZ / "mcp_server" / "analista.py").read_text(encoding="utf-8")
