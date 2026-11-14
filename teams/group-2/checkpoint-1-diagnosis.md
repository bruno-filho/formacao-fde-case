# Checkpoint 1: diagnóstico e prioridade

> **Momento:** checkpoint 1, sábado, 14/11, depois do roleplay e do dossiê.
>
> **Onde entregar:** no fork do líder do grupo, em `teams/group-2/checkpoint-1-diagnosis.md`, por pull request.
>
> **Fontes usadas:** "Dossiê" é o dossiê pós-reunião do Pack 2 (fonte principal dos números, medidos de jan a set); "Gemini hh:mm:ss" é o minuto da reunião de sábado no resumo do Gemini (fonte do que foi dito); "Briefing" é o briefing do Pack 1; "Suposição do grupo" é conta ou inferência nossa, ainda sem dado do cliente.

---

## Grupo

- Grupo: Grupo 2
- Integrantes: ____

## 1. O problema

- O que o cliente disse que é o problema: o contas a pagar lança, paga e baixa cerca de 400 boletos por dia à mão, e a empresa paga juros e multa por atraso. "Contratei para automatizar o boleto" (CFO, Dossiê; Gemini 00:19:59, 00:21:20).
- O que o grupo entende que é o problema: o recebimento do CD só tem duas saídas, aceitar ou recusar a carga inteira, e aceita para não haver ruptura. Ao aceitar, a Já Chegou assume a nota como veio, com item a mais ou a menos: para o jurídico, "aceitar a nota é aceitar o pedido" (Dossiê). O erro é do fornecedor, mas a conta e o retrabalho ficam com a Já Chegou, e a divergência só aparece na doca, quando já não há tempo de resolver na origem. A correção manual depois do aceite segura o pagamento e gera os juros que o CFO quer eliminar.
- Onde, no caminho do pedido de compra até o pagamento, ele aparece: no recebimento do CD, que confere a nota física só na hora de descarregar, sem validação no sistema (Gemini 00:04:15), e decide entre aceitar ou recusar tudo (Gemini 00:05:58). Depois, na conferência e correção manual, que leva 14 dias da nota ao lançamento no CD e segura o pagamento (Dossiê, Anexo 3).
- Quem sente a dor (por papel: CFO, controller, compras, outro): CFO (juros, margem e aprovação de cada pagamento), controller e os 5 analistas terceirizados (fila manual, provisão no fechamento), compras (doca sem aviso, ruptura quando o fornecedor bloqueia entrega).
- Evidência (dossiê ou reunião): 41% do valor é pago depois do vencimento, com R$ 122 mil por mês de juros e multa (Dossiê, Anexos 2 e 3). Em janeiro, 76% do valor saiu depois do vencimento (Dossiê, Anexo 3). Pagar errado custa R$ 543 mil por mês, e o recuperado é zero em todos os meses (Dossiê, Anexos 2 e 3). Só 0,7% das notas do CD batem sozinhas com a ordem (Dossiê, Anexo 3).

## 2. O número a mover

### Qual perda

- [x] Pagar errado
- [ ] Pagar atrasado
- [ ] Ruptura de estoque
- [ ] Custo de operar

### Baseline e meta

| Campo | Valor | Fonte |
| --- | --- | --- |
| Indicador (como a perda é medida) | P1: pago sem mercadoria correspondente, menos o recuperado, em R$ e como taxa sobre o valor das notas | Dossiê, Anexo 2 |
| Baseline (valor hoje) | R$ 543 mil por mês, ou 1,56% dos R$ 34,8 milhões em notas; recuperado zero | Dossiê, Anexos 1 a 3; taxa é conta do grupo |
| Período do baseline | Média de jan a set, com faixa de R$ 136 mil a R$ 1,8 milhão; abril concentrou quase 40% do período | Dossiê, Anexo 2 |
| Quem assina o baseline | Controller, dono do processo, e CFO, antes de mudar qualquer coisa | A combinar |
| Meta | Reduzir em 50% a perda líquida (pago sem mercadoria menos o recuperado do fornecedor), sem a ruptura passar de 1,2 ponto e sem mudar a regra de aceitar a carga | Suposição do grupo; ruptura em Dossiê, Anexo 2 |
| Prazo da meta | Primeiras divergências registradas e cobradas do fornecedor até a semana 4 (quick win); meta cheia em 8 semanas | Dossiê; Briefing |
| Indicador do quick win | Juros e multa pagos por mês: baseline de R$ 122 mil, com 41% do valor pago depois do vencimento. Meta: cair 50% até a semana 4 | Baseline no Dossiê, Anexos 2 e 3; meta é suposição do grupo |

- Por que esta perda, e não as outras três: P1 é 4,5 vezes os juros (R$ 543 mil contra R$ 122 mil por mês) (Dossiê, Anexo 2). Ela também puxa o atraso: toda nota aceita com divergência exige correção manual antes de pagar, o que trava a aprovação e gera juros (Gemini 00:21:20, 00:29:52). Ruptura fica como limite da meta, não como alvo. Juros entram como o indicador do quick win porque são a dor que o CFO trouxe e a métrica que ele acompanha.
- Como medir apesar da variação mensal: em taxa (P1 sobre o valor das notas e percentual pago depois do vencimento), em média móvel, e separando abril e setembro. Setembro não serve de baseline para atraso: os 16% vieram de uma semana de força-tarefa do controller, e o processo não mudou (Dossiê).

## 3. A prioridade

| Frente | Perda que move | Retorno | Tempo até o primeiro valor (5 = mais rápido) | Esforço (5 = menor esforço) | Total | Depende de | Confiança |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A. Check antecipado da nota do CD, assim que ela é emitida e antes do caminhão: conferir nota × pedido, avisar compras do que diverge, deixar pronta a correção do ERP e registrar a diferença. O que bate segue direto para a fila de pagamento por vencimento | P2 (juros) e P1 | 5 | 5 | 4 | 14 | CSV diário de títulos (liberado), credencial de serviço na captura de NF, usuário de leitura no ERP | Alta |
| B. Cobrar formalmente do fornecedor a diferença registrada (abatimento na nota seguinte), no lugar da negociação verbal | P1 | 4 | 3 | 3 | 10 | O registro da diferença feito pela frente A e a regra do jurídico | Baixa: o recuperado hoje é zero |
| C. Corrigir o cadastro de conversão caixa × unidade, que gera divergência | P1 | 3 | 2 | 3 | 8 | Cadastro por planilha e WMS que não converte unidade | Média |
| D. Automatizar o lançamento de boletos, o pagamento e a baixa no ERP | P2 e P4 | 2 | 3 | 2 | 7 | API do banco, que não existe, e escrita no ERP | Baixa |

- Frente escolhida para começar: A, como quick win, atacando primeiro a dor do CFO: pagar em dia e parar de pagar juros. É o check antecipado das notas do CD, começando pelos fornecedores com mais divergência. Ele não muda a regra de aceitar ou recusar a carga: muda o momento em que a divergência é descoberta, da doca para a emissão da nota.
- Por quê: entra pelo objetivo principal do CFO, que é parar de pagar juros (Gemini 00:21:20, 00:29:52; Dossiê). Hoje 41% do valor sai depois do vencimento, e a conferência manual leva 14 dias da nota ao lançamento no CD (Dossiê, Anexo 3). Se a correção já estiver pronta quando a carga é aceita, a nota não fica parada e é paga em dia. Ao mesmo tempo, a diferença registrada vira a base para cobrar o fornecedor e atacar os R$ 543 mil de P1. É rápido porque não depende de integração bancária nem de mudar a regra de recebimento: usa a nota que a captura de NF já busca na SEFAZ, a ordem do ERP e o CSV diário de títulos, já liberado (Dossiê, Anexo 6). A nota quase sempre chega antes da mercadoria (Dossiê), e o pagamento sai em média em 45 dias (Gemini 00:15:36), então há folga para corrigir antes de vencer. No quick win, a correção fica preparada para o analista lançar: nada escreve no ERP sem homologação, e a atual é uma cópia de março (Dossiê, Anexo 6).
- O que fica para depois, e por quê: o quick win abre caminho para as frentes mais robustas, nesta ordem.
  - **Semanas 1 a 4 (quick win):** check na emissão da nota, aviso a compras antes do caminhão, correção do ERP preparada, registro da diferença e fila de pagamento por vencimento, com alerta das notas paradas perto de vencer. O relatório semanal ao CFO mostra os juros pagos e o valor das divergências registradas.
  - **Semanas 5 a 8:** B, com a cobrança formal da diferença registrada, e o check entrando no fluxo de aprovação, incluindo o bloqueio de pagamento duplicado (Gemini 00:07:47; Dossiê, Anexo 4). C entra se a H1 se confirmar.
  - **Depois das 8 semanas:** D, porque o banco não tem API (Dossiê, Anexo 6) e automatizar antes só acelera um pagamento que pode estar errado. Aceite parcial com nota de devolução também fica para depois: muda a regra de recebimento, o que já foi tentado e não andou (Gemini 00:18:22, 00:43:06), e exige escrita no ERP.

## 4. A reformulação do pedido do CFO

| | Texto |
| --- | --- |
| O pedido, como o CFO trouxe | Automatizar lançar, pagar e baixar os boletos sem digitação, e parar de pagar juros e multa (Briefing; Dossiê). |
| O pedido, como o grupo propõe | Parar de descobrir o erro do fornecedor na doca: conferir nota × pedido assim que a nota é emitida, para que a nota aceita já chegue com a correção pronta e seja paga em dia, e a diferença fique registrada para cobrar do fornecedor. A regra de aceitar a carga continua. |
| Por que a mudança move mais o número | A correção manual feita depois do aceite é o que segura o pagamento e gera juros: antecipá-la ataca os juros e, ao mesmo tempo, P1, que vale 4,5 vezes mais (R$ 543 mil contra R$ 122 mil por mês). Abrindo a perda em ramos, o pedido como veio cobre P2 e P4: R$ 167 mil de R$ 710 mil por mês. |
| Como o grupo vai apresentar isso ao CFO | Começar pela dor dele, com o número dele: R$ 122 mil por mês de juros e 41% do valor pago depois do vencimento. O quick win em até 4 semanas mostra os juros caindo num relatório semanal, junto com as divergências registradas, sem mexer na regra de recebimento que protege contra a ruptura. Depois, mostrar os R$ 543 mil pagos sem mercadoria correspondente, que nunca voltam. |

## 5. Hipóteses e o que falta saber

### Hipóteses

| # | Hipótese | Como confirmar | Se estiver errada, o que muda |
| --- | --- | --- | --- |
| H1 | Parte relevante da divergência no CD é erro de conversão caixa × unidade, já que o WMS não converte (Dossiê) | Classificar uma amostra de notas do CD nas exceções 1 a 8 do Dossiê (Anexo 4) | A frente C perde força e o foco fica no check e na cobrança |
| H2 | A maior parte dos juros vem de notas paradas na conferência e na correção manual (14 dias até o lançamento no CD) | Cruzar os títulos pagos com atraso, do CSV diário, com os dias da nota até o lançamento | Se o atraso vier da fila de boletos ou do saldo, o quick win se apoia na fila por vencimento e a frente D sobe na prioridade |
| H3 | Avisar compras antes do caminhão não aumenta a ruptura (1,2 ponto hoje) | Piloto com poucos fornecedores do CD, acompanhando a ruptura | O check só alerta, e a diferença segue para a cobrança (B) |
| H4 | A correção feita logo no aceite cabe no prazo médio de 45 dias, sem gerar atraso | Comparar a data de recebimento no CD com o vencimento de cada nota | O quick win precisa priorizar as notas de vencimento curto |
| H5 | O atraso de setembro (16%) não se sustenta sem a força-tarefa | Acompanhar outubro e novembro no CSV diário de títulos | Se se sustentar, o baseline de juros do quick win precisa ser revisto |

### O que falta saber

| # | Pergunta | Para quem (por papel) | Por que importa |
| --- | --- | --- | --- |
| Q1 | Quanto dos R$ 543 mil de P1 é do CD e quanto é das lojas? | Controller | O CD tem 1,9 mil notas e cerca de 64% do valor (Dossiê, Anexo 1); define o alcance do check |
| Q2 | Quanto custou a semana de força-tarefa de setembro, e o atraso de outubro já voltou a subir? | Controller e CFO | Define o baseline de juros do quick win |
| Q3 | Quando saem a credencial de serviço da captura de NF e o usuário de leitura no ERP, com o termo de confidencialidade? | Controller e área fiscal | Hoje a credencial é o login de um analista terceirizado; sem isso, o check não começa |
| Q4 | Quanto tempo leva a correção no ERP de uma nota aceita com divergência, e quem faz? | Controller | Se for o que atrasa o pagamento, é onde o quick win reduz juros |
| Q5 | O fornecedor aceita cancelar e reemitir a nota antes da entrega, ou dar abatimento na nota seguinte? | Compras | Define se a divergência vista antes do caminhão pode ser resolvida na origem ou só cobrada depois |
| Q6 | O jurídico aceita recusa parcial ou nota de devolução quando a divergência é vista antes da doca? | Controller, com o jurídico | Define se o aceite parcial pode sair do "depois das 8 semanas" |
| Q7 | Por que abril concentrou quase 40% de P1? | Controller | Um evento único, como um fornecedor ou um item, muda o baseline |

## 6. Quem decide, quem paga, quem sente e quem libera

| Papel | O que quer | Decide, paga, sente ou libera | Posição sobre o pedido | O que precisamos dele |
| --- | --- | --- | --- | --- |
| CFO, sponsor | Parar de pagar juros, fechar o mês mais cedo e controlar cada saída de caixa | Decide e paga; libera o banco | Apoia o pedido como veio e acha que o atraso já está caindo | Decisão sobre o reenquadramento e patrocínio |
| Controller | Fechar sem provisão gorda e com menos fila manual | Sente e libera: ERP, captura de NF, CSV de títulos, caixa de e-mail | Apoia, mas exige homologação e termo de confidencialidade por pessoa | Acessos e baseline assinado |
| Gerente de compras e comercial | Produto na prateleira, receber rápido, não romper | Sente e libera: agenda de doca, WMS, ordens por CSV | Neutro: "não quero briga com fornecedor bom", mas quer saber antes | Agenda de doca e piloto com fornecedores |
| Jurídico | Proteger a posição fiscal e contratual | Libera a regra de recusa e devolução | Hoje trava: "aceitar a nota é aceitar o pedido" | Regra para recusa parcial |
| Analistas do contas a pagar (terceirizados) | Menos trabalho manual | Sentem; um deles detém a credencial da SEFAZ | Neutros | Troca da credencial nominal por uma de serviço |

- Conflito principal: compras e comercial ganham quando a mercadoria entra, e o financeiro absorve o custo da divergência depois (Dossiê). O check antecipado reduz o conflito porque compras fica sabendo antes e decide na doca, sem brigar com o fornecedor depois.
- Quem arbitra: o CFO, como sponsor e dono do caixa. A confirmar se alguém acima dele resolve um impasse entre compras e financeiro.

## 7. Termos com sentidos diferentes

| Termo | Como um cargo usa | Como outro cargo usa | Onde isso pesa |
| --- | --- | --- | --- |
| Aprovado | CFO: aprovou o pagamento na lista do dia | Na prática, abaixo de R$ 5 mil ele "assina sem olhar" (Dossiê) | Aprovado não quer dizer conferido |
| Aceitar | Doca: deixar a carga entrar | Jurídico: aceitar a nota é aceitar o pedido | Aceitar na doca vira obrigação de pagar a nota cheia |
| Recebido | Doca e WMS: caixas descarregadas | Controller: quantidade conferida contra a nota e a ordem | O WMS não converte caixa em unidade |
| Atrasado | CFO: o atraso vem caindo (16% em setembro) | Dossiê: 41% do valor na média de jan a set | O baseline muda conforme o mês escolhido |
| Divergência | Compras: o que não bate na doca | Controller: o que vira ordem complementar, criada por três áreas | Ninguém soma a divergência num lugar só |
| Pedido ou ordem | Forecast: plano de compra | ERP: ordem, sendo 20% subida por CSV manual | Nota sem ordem (cerca de 4%) não tem dono |

## Conferência antes de entregar

- [x] Uma perda marcada, com baseline, meta e fonte.
- [x] Quatro frentes pontuadas e uma escolhida, com o porquê.
- [x] Pedido do CFO reformulado (ou mantido, com justificativa).
- [x] Pelo menos três hipóteses e três perguntas abertas.
- [x] Quem decide, quem paga e quem sente, com o conflito principal.
- [x] Termos com sentidos diferentes entre os cargos.
- [x] Nenhuma pessoa citada pelo nome: só pelo papel.
