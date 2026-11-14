# Checkpoint 1: diagnóstico e prioridade

> **Momento:** checkpoint 1, sábado, 14/11, depois do roleplay e do dossiê.
>
> **Onde entregar:** no fork do líder do grupo, em `teams/group-2/checkpoint-1-diagnosis.md`, por pull request.
>
> **Fontes usadas:** "Gemini hh:mm:ss" é o minuto da reunião de sábado no resumo do Gemini (fonte principal do grupo); "Briefing" é o briefing do cliente no Pack 1; "Suposição do grupo" é conta ou inferência nossa, ainda sem dado do cliente.

---

## Grupo

- Grupo: Grupo 2
- Integrantes: ____

## 1. O problema

- O que o cliente disse que é o problema: o contas a pagar lança, paga e baixa cerca de 400 boletos por dia à mão, e a empresa paga juros e multa por atraso (Gemini 00:19:59, 00:21:20; Briefing).
- O que o grupo entende que é o problema: o recebimento do CD só tem duas saídas, aceitar ou recusar a carga inteira, e aceita para não haver ruptura. Ao aceitar, a Já Chegou assume a nota como veio, com item a mais ou a menos: paga a nota cheia e corrige o ERP à mão para manter a consistência. O erro é do fornecedor, mas a conta e o retrabalho ficam com a Já Chegou, e a divergência só aparece na doca, quando já não há tempo de resolver na origem.
- Onde, no caminho do pedido de compra até o pagamento, ele aparece: no recebimento do CD, que confere a nota física só na hora de descarregar, sem validação no sistema (Gemini 00:04:15), e decide entre aceitar ou recusar tudo (Gemini 00:05:58). Depois, na correção manual do ERP, que segura o pagamento.
- Quem sente a dor (por papel: CFO, controller, compras, outro): CFO (margem e juros), controller e o contas a pagar (correção manual e aprovação), compras (escolha entre recusar e arriscar ruptura ou aceitar e gerar problema no financeiro).
- Evidência (dossiê ou reunião): R$ 440 mil pagos por mercadoria que não foi pedida, mas foi aceita e paga (Gemini 00:45:19). As únicas opções são devolver tudo, com risco de ruptura, ou aceitar e gerar problema na controladoria (Gemini 00:05:58, 00:16:28). No início do ano, 76% dos fornecedores ficaram travados e a diretoria conferiu e aprovou pagamentos à mão (Gemini 00:01:00).

## 2. O número a mover

### Qual perda

- [x] Pagar errado
- [ ] Pagar atrasado
- [ ] Ruptura de estoque
- [ ] Custo de operar

### Baseline e meta

| Campo | Valor | Fonte |
| --- | --- | --- |
| Indicador (como a perda é medida) | Valor pago por mercadoria não pedida, aceita no recebimento do CD | Gemini 00:45:19 (estimativa do cliente) |
| Baseline (valor hoje) | R$ 440 mil | Gemini 00:45:19 |
| Período do baseline | Por mês, segundo a anotação do grupo; o resumo do Gemini não diz o período | A confirmar (Q1) |
| Meta | Reduzir em 50% a perda líquida (pago a mais menos o recuperado do fornecedor), sem a ruptura passar de 1,5% e sem mudar a regra de aceitar a carga | Suposição do grupo; ruptura de 1% a 1,5% em Gemini 00:13:26 |
| Prazo da meta | Primeiras divergências registradas e cobradas do fornecedor até a semana 4 (quick win); meta cheia em 8 semanas | Gemini 00:01:22, 00:20:58; Briefing |
| Indicador do quick win | Juros e multa pagos por mês: baseline de R$ 120 mil, meta de cair 50% até a semana 4 | Baseline no Briefing, a confirmar com a exportação de títulos de jan a set; meta é suposição do grupo |

- Por que esta perda, e não as outras três: os R$ 440 mil são mais de 3 vezes os R$ 120 mil de juros por mês (Briefing), se o período for mensal. Ela também puxa o atraso: toda nota aceita com divergência exige correção manual no ERP antes de pagar, o que trava a aprovação e gera juros (Gemini 00:21:20, 00:29:52). Ruptura fica como limite da meta, não como alvo. Juros entram como o indicador do quick win porque são a métrica que o CFO já acompanha e cobra.

## 3. A prioridade

| Frente | Retorno | Tempo até o primeiro valor (5 = mais rápido) | Esforço (5 = menor esforço) | Total |
| --- | --- | --- | --- | --- |
| A. Check antecipado da nota do CD, assim que ela é emitida e antes do caminhão: conferir nota × pedido, avisar compras do que diverge, deixar pronta a correção do ERP e registrar a diferença. O que bate segue direto para a fila de pagamento por vencimento | 5 | 5 | 4 | 14 |
| B. Cobrar formalmente do fornecedor a diferença registrada (abatimento na nota seguinte), no lugar da negociação verbal | 4 | 3 | 3 | 10 |
| C. Corrigir o cadastro de conversão caixa × unidade, que gera divergência | 3 | 2 | 3 | 8 |
| D. Automatizar o lançamento de boletos, o pagamento e a baixa no ERP | 2 | 3 | 2 | 7 |

- Frente escolhida para começar: A, como quick win. É o check antecipado das notas do CD, começando pelos fornecedores com mais divergência. Ele não muda a regra de aceitar ou recusar a carga: muda o momento em que a divergência é descoberta, da doca para a emissão da nota.
- Por quê: entra pelo objetivo principal do CFO, que é parar de pagar juros (Gemini 00:21:20, 00:29:52). Se a correção do ERP já estiver pronta quando a carga é aceita, a nota não fica parada e é paga em dia. Ao mesmo tempo, a diferença registrada vira a base para cobrar o fornecedor e atacar os R$ 440 mil. É rápido porque não depende de integração bancária nem de mudar a regra de recebimento: usa a nota que a captura de NF já busca na SEFAZ (Briefing) e o pedido, que em 98% dos casos vem do sistema de demanda (Gemini 00:22:35). A carga chega em até 15 dias e o pagamento sai em média em 45 (Gemini 00:23:03, 00:15:36), então há folga para corrigir antes de vencer.
- O que fica para depois, e por quê: o quick win abre caminho para as frentes mais robustas, nesta ordem.
  - **Semanas 1 a 4 (quick win):** check na emissão da nota, aviso a compras antes do caminhão, correção do ERP preparada, registro da diferença e fila de pagamento por vencimento, com alerta das notas paradas perto de vencer. O relatório semanal ao CFO mostra os juros pagos e o valor das divergências registradas.
  - **Semanas 5 a 8:** B, com a cobrança formal da diferença registrada, e o check entrando no fluxo de aprovação, incluindo o bloqueio de pagamento duplicado (Gemini 00:07:47). C entra se a H1 se confirmar.
  - **Depois das 8 semanas:** D, porque não há integração bancária hoje (Gemini 00:04:38) e automatizar antes só acelera um pagamento que pode estar errado. Aceite parcial com nota de devolução também fica para depois: muda a regra de recebimento, o que já foi tentado e não andou (Gemini 00:18:22, 00:43:06).

## 4. A reformulação do pedido do CFO

| | Texto |
| --- | --- |
| O pedido, como o CFO trouxe | Automatizar lançar, pagar e baixar os boletos sem digitação, e parar de pagar juros e multa (Briefing). |
| O pedido, como o grupo propõe | Parar de descobrir o erro do fornecedor na doca: conferir nota × pedido assim que a nota é emitida, para que a nota aceita já chegue corrigida ao ERP e seja paga em dia, e a diferença fique registrada para cobrar do fornecedor. A regra de aceitar a carga continua. |
| Por que a mudança move mais o número | Os R$ 440 mil de pagamento indevido valem mais de 3 vezes os R$ 120 mil de juros (se mensais). E a correção manual feita depois do aceite é o que segura o pagamento e gera juros: antecipá-la ataca os dois. |
| Como o grupo vai apresentar isso ao CFO | Com o número dele: "vocês estimam R$ 440 mil pagos por mercadoria não pedida". Entrar pelo pedido dele e mostrar o problema maior: um quick win em até 4 semanas, com relatório semanal de juros pagos e das divergências registradas e cobradas, sem mexer na regra de recebimento que protege contra a ruptura. |

## 5. Hipóteses e o que falta saber

### Hipóteses

| # | Hipótese | Como confirmar | Se estiver errada, o que muda |
| --- | --- | --- | --- |
| H1 | Parte relevante da divergência é erro de conversão caixa × unidade no cadastro, não mercadoria a mais (Gemini 00:03:48) | Classificar uma amostra de notas divergentes do CD por tipo de diferença | A frente C perde força e o foco fica no check e na cobrança |
| H2 | A maior parte dos juros vem de notas paradas na correção manual do ERP depois de aceitas com divergência | Cruzar os títulos pagos com atraso (exportação de jan a set) com as notas que tiveram divergência | Se o atraso vier da fila de boletos, o quick win se apoia na fila por vencimento e a frente D sobe na prioridade |
| H3 | A nota eletrônica chega pela captura de NF antes do caminhão, com tempo para conferir e avisar compras | Comparar a data de captura de cada nota com a data de recebimento no CD | O check acontece na chegada do caminhão: ainda prepara a correção do ERP, mas sobra pouco tempo para falar com o fornecedor |
| H4 | A correção feita logo no aceite cabe no prazo médio de 45 dias, sem gerar atraso | Comparar a data de recebimento no CD com o vencimento de cada nota | O quick win precisa priorizar as notas de vencimento curto |

### O que falta saber

| # | Pergunta | Para quem (por papel) | Por que importa |
| --- | --- | --- | --- |
| Q1 | Os R$ 440 mil são por mês ou o total de um período? | Controller | Define o tamanho da perda e a comparação com os R$ 120 mil de juros |
| Q2 | Os R$ 440 mil incluem cargas incompletas ou só mercadoria não pedida? | Controller | Item a mais aceito vira estoque, e item que faltou é perda inteira; o peso de cada um muda o tamanho da perda |
| Q3 | O recebimento do CD é registrado em sistema e chega ao ERP antes do pagamento? | Controller e compras | Diz se a conferência pode ser automática ou depende de digitar a contagem |
| Q4 | Quanto do pago a mais é recuperado hoje, e por qual caminho? | Compras e controller | Separa a perda bruta da perda líquida |
| Q5 | Quanto tempo leva a correção no ERP de uma nota aceita com divergência, e quem faz? | Controller | Se for o que atrasa o pagamento, é onde o quick win reduz juros |
| Q6 | O fornecedor aceita cancelar e reemitir a nota antes da entrega, ou dar abatimento na nota seguinte? | Compras | Define se a divergência vista antes do caminhão pode ser resolvida na origem ou só cobrada depois |

## Conferência antes de entregar

- [x] Uma perda marcada, com baseline, meta e fonte.
- [x] Quatro frentes pontuadas e uma escolhida, com o porquê.
- [x] Pedido do CFO reformulado (ou mantido, com justificativa).
- [x] Pelo menos três hipóteses e três perguntas abertas.
- [x] Nenhuma pessoa citada pelo nome: só pelo papel.
