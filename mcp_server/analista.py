"""Servidor MCP do analista da Já Chegou: decidir a fila de propostas de dentro do Claude.

Leitura: `listar_fila` (o que espera pessoa e cabe no nível do analista) e `ler_proposta`.
Escrita: `decidir`, que grava a decisão em saidas/decisoes.jsonl, e `delegar_ao_motor`, que grava só
o pedido de simulação em saidas/delegacoes.jsonl (sempre dry_run, nada é aprovado).

É um servidor separado do `ja-chegou` de propósito: o subagente `auditor-de-notas` libera
`mcp__ja-chegou__*` e não pode ganhar uma tool que decide. A trava fica no sistema: o nível de cada
nota é recalculado pela régua (`jachegou.regua`), e `decidir` recusa o que passa da alçada.

Quem decide vem do ambiente, repassado pelo .mcp.json:
  FDE_ANALISTA_ID     quem decide (obrigatório para gravar)
  FDE_ANALISTA_NIVEL  analista ou coordenacao (padrão analista)
Diretoria e bloqueio nunca são decididos aqui.

Rodar sozinho (stdio):  uv run python mcp_server/analista.py
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from mcp.server.apps import Apps  # noqa: E402
from mcp.server.mcpserver import MCPServer  # noqa: E402

from jachegou.base import ACOES, NIVEIS, Base  # noqa: E402
from jachegou.comparar import comparar  # noqa: E402
from jachegou.regua import nivel_mais_alto, nivel_minimo  # noqa: E402

base = Base()
SAIDAS = Path(os.environ.get("FDE_SAIDAS") or RAIZ / "saidas")

NIVEIS_DO_ANALISTA = ["analista", "coordenacao"]
DECISOES = ["aprovar", "alterar"]
# Regra mínima da simulação do motor, inspirada no mock do grupo 1 (teams/group-2/motor-mock/).
EXCECOES_DELEGAVEIS = {"E1", "E3", "E4"}
TETO_VALOR_EM_RISCO = 20_000.0
TETO_VALOR_DA_NOTA = 100_000.0

URI_FILA = "ui://ja-chegou-analista/fila"
HTML_FILA = Path(__file__).resolve().parent / "ui" / "fila.html"
apps = Apps()

# As tools com tela entram no Apps antes de o servidor ser criado: o MCPServer as lê da extensão.
@apps.tool(resource_uri=URI_FILA)
def mostrar_fila(destino: str | None = None) -> dict:
    """A mesma fila de listar_fila, desenhada numa tela dentro do chat (MCP App), onde o analista abre a
    proposta e aprova ou altera a ação na doca. A tela chama ler_proposta e decidir pelo host, com as
    mesmas travas. Num host sem MCP Apps, o resultado é a fila em texto, igual ao de listar_fila."""
    return listar_fila(destino=destino)  # definida abaixo; resolvida na hora da chamada


apps.add_html_resource(URI_FILA, HTML_FILA.read_text(encoding="utf-8"), name="fila",
                       title="Fila do analista", description="A fila de propostas, com aprovar e alterar ação")


servidor = MCPServer(
    name="ja-chegou-analista",
    extensions=[apps],
    instructions=(
        "Fila de propostas do check antecipado da Já Chegou, para o analista decidir. "
        "Todo número vem destas tools. Só chame decidir quando o analista pedir, e não contorne uma recusa: "
        "diretoria e bloqueio não são decididos aqui."
    ),
)


def _analista() -> tuple[str, str]:
    """Quem decide e o nível dele, lidos na hora da chamada."""
    return ((os.environ.get("FDE_ANALISTA_ID") or "").strip(),
            (os.environ.get("FDE_ANALISTA_NIVEL") or "analista").strip())


def _ler_jsonl(caminho: Path) -> list[dict]:
    if not caminho.is_file():
        return []
    return [json.loads(x) for x in caminho.read_text(encoding="utf-8").splitlines() if x.strip()]


def _arquivo_propostas() -> Path:
    arquivo = SAIDAS / (os.environ.get("FDE_ARQUIVO_PROPOSTAS") or "propostas.jsonl")
    return arquivo if arquivo.is_file() else SAIDAS / "baseline.jsonl"


def _propostas() -> dict[str, dict]:
    """Por nota, a última proposta aceita: linhas com `recusada` não contam."""
    vigentes: dict[str, dict] = {}
    for p in _ler_jsonl(_arquivo_propostas()):
        if "recusada" not in p and p.get("nota_id"):
            vigentes[p["nota_id"]] = p
    return vigentes


def _decididas() -> dict[str, dict]:
    return {d["nota_id"]: d for d in _ler_jsonl(SAIDAS / "decisoes.jsonl") if d.get("nota_id")}


def _efetivo(proposta: dict, nota: dict) -> str:
    """O encaminhamento que vale: o do arquivo ou o mínimo da régua, o que for mais alto. O nível só sobe."""
    return nivel_mais_alto(proposta.get("encaminhamento"), nivel_minimo(proposta["classificacao"], nota, base))


def _gravar(nome: str, linha: dict) -> None:
    SAIDAS.mkdir(parents=True, exist_ok=True)
    with open(SAIDAS / nome, "a", encoding="utf-8") as f:
        f.write(json.dumps(linha, ensure_ascii=False) + "\n")


def _fila(teto: str) -> list[dict]:
    """As propostas não decididas cujo nível efetivo é analista ou coordenacao e não passa do teto."""
    decididas = _decididas()
    linhas = []
    for nota_id, p in _propostas().items():
        nota = base.notas.get(nota_id)
        if nota is None or nota_id in decididas:
            continue
        efetivo = _efetivo(p, nota)
        if efetivo not in NIVEIS_DO_ANALISTA or NIVEIS.index(efetivo) > NIVEIS.index(teto):
            continue
        fornecedor = base.fornecedores.get(nota["fornecedor_id"], {})
        linhas.append({"nota_id": nota_id, "fornecedor_id": nota["fornecedor_id"],
                       "fornecedor": fornecedor.get("razao_social"), "destino": nota["destino"],
                       "data_emissao": nota["data_emissao"], "classificacao": p["classificacao"],
                       "acao_doca": p.get("acao_doca"), "encaminhamento": efetivo,
                       "valor_em_risco": p.get("valor_em_risco"), "valor_total": nota["valor_total"]})
    linhas.sort(key=lambda x: (-(x["valor_em_risco"] or 0), x["data_emissao"]))
    return linhas


@servidor.tool()
def listar_fila(nivel: str | None = None, destino: str | None = None) -> dict:
    """As propostas que esperam uma pessoa e cabem no nível do analista, ainda não decididas.

    Ordem: valor em risco (maior primeiro) e depois data de emissão. O encaminhamento de cada linha é o
    recalculado pela régua (só sobe). Filtros opcionais: nivel (analista ou coordenacao; restringe, nunca
    passa do nível do analista) e destino (ex.: CD-01, LJ-007). Devolve também o total de valor em risco."""
    _, nivel_do_analista = _analista()
    if nivel_do_analista not in NIVEIS_DO_ANALISTA:
        return {"erro": f"FDE_ANALISTA_NIVEL deve ser um de {NIVEIS_DO_ANALISTA}", "fila": [], "total_valor_em_risco": 0}
    teto = nivel_do_analista
    if nivel is not None:
        if nivel not in NIVEIS_DO_ANALISTA:
            return {"erro": f"nivel deve ser um de {NIVEIS_DO_ANALISTA}", "fila": [], "total_valor_em_risco": 0}
        teto = min(nivel, nivel_do_analista, key=NIVEIS.index)
    fila = [x for x in _fila(teto)
            if (nivel is None or x["encaminhamento"] == teto) and (destino is None or x["destino"] == destino)]
    return {"fila": fila, "total_valor_em_risco": round(sum(x["valor_em_risco"] or 0 for x in fila), 2),
            "nivel_do_analista": nivel_do_analista}


@servidor.tool()
def ler_proposta(nota_id: str) -> dict:
    """A proposta vigente de uma nota, a nota resumida, o comparar_itens (nota, ordem e doca lado a lado),
    o fornecedor (inclusive se está bloqueado), o nível mínimo pela régua, o encaminhamento que vale e se
    a nota já foi decidida."""
    nota = base.notas.get(nota_id)
    if nota is None:
        return {"erro": f"nota {nota_id} não encontrada"}
    proposta = _propostas().get(nota_id)
    if proposta is None:
        return {"erro": f"nota {nota_id} não tem proposta registrada"}
    resumo = {k: nota[k] for k in ("nota_id", "numero", "serie", "fornecedor_id", "destino", "data_emissao",
                                   "pedido_referenciado", "canal_entrada", "valor_total")} | {"itens": len(nota["itens"])}
    decisao = _decididas().get(nota_id)
    return {"proposta": proposta, "nota": resumo, "comparar_itens": comparar(nota_id, base),
            "fornecedor": base.fornecedores.get(nota["fornecedor_id"]),
            "nivel_minimo_regua": nivel_minimo(proposta["classificacao"], nota, base),
            "encaminhamento": _efetivo(proposta, nota), "decidida": decisao is not None, "decisao": decisao}


def _recusa(erro: str) -> dict:
    return {"gravada": False, "erro": erro}


@servidor.tool()
def decidir(nota_id: str, decisao: str, justificativa: str, acao_doca: str | None = None) -> dict:
    """Grava a decisão do analista sobre a proposta de uma nota, em saidas/decisoes.jsonl. Vale uma vez por nota.

    decisao: aprovar (mantém a ação na doca proposta) ou alterar (troca a ação; acao_doca obrigatória).
    acao_doca: receber, receber_parcial ou recusar (só com alterar).
    justificativa: por que, em pelo menos 10 caracteres.
    Recusa sem gravar o que passa da alçada de quem decide; diretoria e bloqueio nunca são decididos aqui."""
    analista_id, nivel_do_analista = _analista()
    if not analista_id:
        return _recusa("FDE_ANALISTA_ID vazio: não há quem decide nesta sessão")
    if nivel_do_analista not in NIVEIS_DO_ANALISTA:
        return _recusa(f"FDE_ANALISTA_NIVEL '{nivel_do_analista}' não decide aqui; deve ser um de {NIVEIS_DO_ANALISTA}")
    nota = base.notas.get(nota_id)
    if nota is None:
        return _recusa(f"nota {nota_id} não encontrada")
    proposta = _propostas().get(nota_id)
    if proposta is None:
        return _recusa(f"nota {nota_id} não tem proposta registrada")
    if nota_id in _decididas():
        return _recusa(f"nota {nota_id} já foi decidida; a decisão vale uma vez")
    efetivo = _efetivo(proposta, nota)
    if efetivo in ("diretoria", "bloqueio"):
        return _recusa(f"nota {nota_id} é de {efetivo} pela régua; este servidor não decide {efetivo}")
    if efetivo not in NIVEIS_DO_ANALISTA:
        return _recusa(f"nota {nota_id} é de {efetivo} pela régua e não espera pessoa")
    if NIVEIS.index(efetivo) > NIVEIS.index(nivel_do_analista):
        return _recusa(f"nota {nota_id} exige {efetivo} pela régua, acima do nível de quem decide ({nivel_do_analista})")
    if decisao not in DECISOES:
        return _recusa(f"decisao deve ser uma de {DECISOES}")
    if decisao == "alterar" and acao_doca not in ACOES:
        return _recusa(f"alterar exige acao_doca, uma de {ACOES}")
    if not justificativa or len(justificativa.strip()) < 10:
        return _recusa("justificativa precisa de pelo menos 10 caracteres")
    proposta_acao = proposta.get("acao_doca")
    final = acao_doca if decisao == "alterar" else proposta_acao
    if decisao == "alterar" and acao_doca == proposta_acao:
        decisao = "aprovar"
    linha = {"nota_id": nota_id, "decisao": decisao, "acao_doca": final, "acao_doca_proposta": proposta_acao,
             "nivel_minimo": efetivo, "decidido_por": analista_id, "nivel_de_quem_decidiu": nivel_do_analista,
             "justificativa": justificativa.strip(), "decidido_em": datetime.now().isoformat(timespec="seconds")}
    _gravar("decisoes.jsonl", linha)
    return {"gravada": True, "decisao": linha}


def _motivo_para_pessoa(linha: dict) -> str | None:
    """None quando o motor aprovaria; senão, por que o caso fica com a pessoa."""
    if linha["classificacao"] not in EXCECOES_DELEGAVEIS:
        return f"{linha['classificacao']} não é exceção delegável ({', '.join(sorted(EXCECOES_DELEGAVEIS))})"
    if linha["encaminhamento"] != "analista":
        return f"nível {linha['encaminhamento']} não é delegável ao motor"
    if (linha["valor_em_risco"] or 0) > TETO_VALOR_EM_RISCO:
        return f"valor em risco acima de R$ {TETO_VALOR_EM_RISCO:,.0f}"
    if linha["valor_total"] > TETO_VALOR_DA_NOTA:
        return f"valor da nota acima de R$ {TETO_VALOR_DA_NOTA:,.0f}"
    return None


@servidor.tool()
def delegar_ao_motor(nota_ids: list[str] | None = None, classificacoes: list[str] | None = None) -> dict:
    """Pede ao motor de decisão uma simulação (dry_run) sobre a fila do analista. Nada é aprovado.

    Sem filtro, simula a fila inteira do nível do analista. Filtros opcionais: nota_ids e classificacoes.
    Grava só o pedido em saidas/delegacoes.jsonl e devolve o que o motor aprovaria e o que fica com a pessoa."""
    analista_id, nivel_do_analista = _analista()
    if not analista_id:
        return {"gravado": False, "erro": "FDE_ANALISTA_ID vazio: não há quem pede a delegação"}
    if nivel_do_analista not in NIVEIS_DO_ANALISTA:
        return {"gravado": False, "erro": f"FDE_ANALISTA_NIVEL deve ser um de {NIVEIS_DO_ANALISTA}"}
    fila = [x for x in _fila(nivel_do_analista)
            if (nota_ids is None or x["nota_id"] in nota_ids)
            and (classificacoes is None or x["classificacao"] in classificacoes)]
    aprovaria, com_pessoa = [], []
    for x in fila:
        item = {"nota_id": x["nota_id"], "classificacao": x["classificacao"], "acao_doca": x["acao_doca"],
                "valor_em_risco": x["valor_em_risco"]}
        motivo = _motivo_para_pessoa(x)
        if motivo is None:
            aprovaria.append(item)
        else:
            com_pessoa.append(item | {"motivo": motivo})
    resumo = {"avaliadas": len(fila), "motor_aprovaria": len(aprovaria), "fica_com_pessoa": len(com_pessoa)}
    pedido = {"dry_run": True, "solicitado_por": analista_id, "nivel_de_quem_pediu": nivel_do_analista,
              "filtros": {"nota_ids": nota_ids, "classificacoes": classificacoes}, "resumo": resumo,
              "pedido_em": datetime.now().isoformat(timespec="seconds")}
    _gravar("delegacoes.jsonl", pedido)
    return {"gravado": True, "dry_run": True, "pedido": pedido,
            "motor_aprovaria": aprovaria, "fica_com_pessoa": com_pessoa}


if __name__ == "__main__":
    servidor.run("stdio")
