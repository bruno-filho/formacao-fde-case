---
name: decidir-fila
description: O que espera o analista e como ele decide? Orienta a sessão do analista do contas a pagar a ver a fila de propostas, abrir uma proposta com a divergência e a evidência, e aprovar ou alterar a ação na doca pelas tools do servidor ja-chegou-analista. Use quando o analista pedir "mostra a minha fila", "abre a NF-0xx", "aprova", "altera para recusar" ou "simula o que o motor aprovaria".
---

# Decidir a fila

Esta skill orienta a sessão principal do analista. Ela usa só as tools do servidor `ja-chegou-analista`:
`listar_fila`, `ler_proposta`, `decidir` e `delegar_ao_motor`. Quem decide e o nível dele vêm do
ambiente (`FDE_ANALISTA_ID` e `FDE_ANALISTA_NIVEL`), não da conversa.

## Caminho feliz

1. O analista pede "mostra a minha fila". Chame `listar_fila` e mostre a fila numa tabela: nota,
   fornecedor, destino, classificação, ação na doca proposta, encaminhamento, valor em risco e valor da
   nota, na ordem em que a tool devolveu. Abaixo da tabela, o total de valor em risco que a tool devolveu.
2. O analista pede "abre a NF-0xx". Chame `ler_proposta` e resuma em poucas linhas a divergência e a
   evidência: o que o `comparar_itens` mostra (nota, ordem e doca lado a lado), a proposta do agente, se o
   fornecedor está bloqueado e o encaminhamento que vale pela régua.
3. O analista diz "aprova" ou "altera para recusar". Antes de chamar `decidir`, confirme em uma linha o
   que vai gravar (nota, decisão, ação na doca final e a justificativa nas palavras dele) e espere o sim.
4. Chame `decidir`. Se a tool gravou, diga que a nota saiu da fila. Se recusou, mostre o motivo que a tool
   devolveu, como veio.

Para "simula o que o motor aprovaria", chame `delegar_ao_motor`. É sempre simulação: nada é aprovado,
só o pedido fica registrado. Mostre o que o motor aprovaria e o que fica com a pessoa, com o motivo.

Diretoria e bloqueio ficam fora desta sessão: a fila não os mostra e `decidir` os recusa. Se o analista
perguntar por eles, diga que são decididos fora daqui.

## O que a sessão nunca faz

- **Inventar número.** Todo valor, nível e contagem vem de uma tool. Se a tool não devolveu, diga que não sabe.
- **Decidir sem o analista pedir.** `decidir` só é chamada depois de um pedido explícito e da confirmação de uma linha.
- **Contornar uma recusa da tool.** Não tenta de novo com outro nível, não troca a decisão para passar,
  não edita arquivo em `saidas/` nem o ambiente. A recusa é a resposta: mostre o motivo ao analista.
