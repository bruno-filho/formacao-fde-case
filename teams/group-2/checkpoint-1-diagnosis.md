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
- O que o grupo entende que é o problema: a Já Chegou paga notas que ninguém conferiu. Só 0,7% das notas do CD batem sozinhas com a ordem (Dossiê, Anexo 3), a doca aceita ou recusa a carga inteira e, para o jurídico, "aceitar a nota é aceitar o pedido" (Dossiê). O erro é do fornecedor, mas a conta fica com a Já Chegou: nada volta. O atraso é consequência: a conferência manual leva 14 dias da nota ao lançamento no CD (Dossiê, Anexo 3).
- Onde, no caminho do pedido de compra até o pagamento, ele aparece: entre a nota e a doca. A nota quase sempre chega antes da mercadoria, mas "ninguém a olha antes da doca" (compras, Dossiê). Depois, na conferência manual de ordem, nota e recebido, e na lista do dia, que o CFO aprova item a item com o saldo que muda ao longo do dia.
- Quem sente a dor (por papel: CFO, controller, compras, outro): CFO (juros, margem e aprovação de cada pagamento), controller e os 5 analistas terceirizados (fila manual, provisão no fechamento), compras (doca sem aviso, ruptura quando o fornecedor bloqueia entrega).
- Evidência (dossiê ou reunião): pagar errado custa R$ 543 mil por mês e o recuperado é zero em todos os meses (Dossiê, Anexos 2 e 3). Em janeiro, 76% do valor saiu depois do vencimento (Dossiê, Anexo 3). Conferir uma nota de 80 itens leva mais de 1h30 (Dossiê).

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
| Baseline (valor hoje) | R$ 543 mil por mês, ou 1,56% dos R$ 34,8 milhões em notas | Dossiê, Anexos 1 e 2; taxa é conta do grupo |
| Período do baseline | Média de jan a set, com faixa de R$ 136 mil a R$ 1,8 milhão; abril concentrou quase 40% do período | Dossiê, Anexo 2 |
| Quem assina o baseline | Controller, dono do processo, e CFO, antes de mudar qualquer coisa | A combinar |
| Meta | Taxa de P1 do CD cair pela metade em 8 semanas, medida em média móvel de 4 semanas, sem a ruptura passar de 1,2 ponto | Suposição do grupo; ruptura em Dossiê, Anexo 2 |
| Prazo da meta | Primeiro valor em até 4 semanas (quick win); meta cheia em 8 semanas | Dossiê; Briefing |
| Indicador do quick win | Valor pago depois do vencimento: baseline de 41% (média de jan a set) e R$ 122 mil por mês de juros e multa. Meta: ficar abaixo de 16% sem força-tarefa | Dossiê, Anexos 2 e 3; meta é suposição do grupo |

- Por que esta perda, e não as outras três: P1 é 4,5 vezes P2 (R$ 543 mil contra R$ 122 mil) e 76% da perda em reais do contas a pagar (Dossiê, Anexo 2). P2 entra como indicador do quick win porque é o número que o CFO acompanha.
- Como medir apesar da variação mensal: em taxa (P1 sobre o valor das notas e percentual pago depois do vencimento), em média móvel, e separando abril e setembro. Setembro não serve de baseline para atraso: os 16% vieram de uma semana de força-tarefa do controller, e o processo não mudou (Dossiê).

## 3. A prioridade

Os nomes das frentes são os que o time interno já discutiu (Dossiê).

| Frente | Perda que move | Retorno | Tempo até o primeiro valor (5 = mais rápido) | Esforço (5 = menor esforço) | Total | Depende de | Confiança |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A. Check antecipado: confrontar a nota com a ordem antes de a mercadoria chegar e avisar compras e a doca, só em leitura no início | P1, e P2 por tirar a conferência do caminho | 5 | 4 | 4 | 13 | Credencial de serviço na captura de NF, usuário de leitura no ERP, agenda de doca | Alta |
| B. Priorização de caixa e aprovação: lista do dia do CFO ordenada por vencimento e risco de juros, marcando duplicidade e nota sem ordem | P2, e P1 nas duplicidades | 3 | 5 | 4 | 12 | CSV diário de títulos, já liberado | Média |
| C. Conciliação ordem × nota × recebido, com conversão de unidade, depois do recebimento | P1 e P4 | 3 | 2 | 2 | 7 | Acesso ao WMS, ainda não pedido | Média |
| D. Cadastro e ordem complementar, na origem | P1 e P4 | 2 | 1 | 2 | 5 | Três áreas e o cadastro por planilha | Baixa |

- Frente escolhida para começar: A, o check antecipado, com a lista do dia de B como primeiro valor do quick win.
- Por quê: A ataca a maior perda (P1) no único momento em que ainda dá para agir, antes de a mercadoria entrar. Compras pediu isso: "Se eu soubesse antes, planejava a equipe e recusava na hora" (Dossiê). B entrega na semana 1 ou 2 com um dado que já está liberado e mostra ao CFO os juros caindo enquanto as credenciais de A são resolvidas. As duas só leem: nada escreve no ERP.
- O que fica para depois, e por quê:
  - **Semanas 1 a 4 (quick win):** lista do dia priorizada para o CFO (B) e check antecipado das notas do CD (A), em leitura, com uma pessoa decidindo.
  - **Semanas 5 a 8:** devolução e recusa parcial no ERP, que precisam de escrita e de uma homologação atualizada (a atual é uma cópia de março), e conversão de unidade (C) se a H1 se confirmar.
  - **Depois das 8 semanas:** pagamento em lote, porque o plano do banco não tem API (Dossiê, Anexo 6), e D, porque depende de três áreas e a ordem complementar leva de 2 dias a 3 meses (Dossiê).

## 4. A reformulação do pedido do CFO

| | Texto |
| --- | --- |
| O pedido, como o CFO trouxe | Automatizar lançar, pagar e baixar os boletos sem digitação, e parar de pagar juros e multa (Briefing; Dossiê). |
| O pedido, como o grupo propõe | Atender uma parte e reenquadrar o resto: atacar os juros já com a lista do dia, e conferir a nota antes de a mercadoria chegar, para parar de pagar o que não foi recebido. A automação do boleto vem depois do check. |
| Por que a mudança move mais o número | Abrindo a perda em ramos (P1 + P2 + P4 = R$ 710 mil por mês), o pedido do CFO cai em P2 e P4: R$ 167 mil, 24% do total. Atendido como veio, ele aumentaria a perda: pagar mais rápido notas que só batem sozinhas em 0,7% dos casos, com recuperado zero, tira a janela em que o erro ainda pode ser pego. E tirar o CFO da aprovação remove a única trava contra pagar duas vezes. |
| Como o grupo vai apresentar isso ao CFO | Começar pelo que ele pediu, com o número dele: o atraso caiu para 16% em setembro, mas com uma semana de força-tarefa, e a média é 41%. A lista do dia sustenta esse nível sem força-tarefa. Depois, mostrar os R$ 543 mil por mês que saem sem mercadoria e nunca voltam, e o check antecipado como a forma de parar isso sem brigar com o fornecedor na doca. |

## 5. Hipóteses e o que falta saber

### Hipóteses

| # | Hipótese | Como confirmar | Se estiver errada, o que muda |
| --- | --- | --- | --- |
| H1 | Boa parte de P1 no CD vem de unidade de medida (caixa × unidade) e de falta física, e não de item trocado | Classificar uma amostra de notas do CD nas exceções 1 a 8 do Dossiê (Anexo 4); o WMS não converte caixa em unidade | Se o grosso for item trocado ou nota sem ordem, D sobe na prioridade |
| H2 | O atraso vem da conferência manual (14 dias até o lançamento no CD) e não da falta de saldo | Cruzar os títulos pagos com atraso, do CSV diário, com os dias da nota até o lançamento | Se for saldo, B vira a frente principal e A perde parte do efeito em P2 |
| H3 | Avisar a doca antes faz compras recusar ou receber diferente sem aumentar a ruptura | Piloto com poucos fornecedores do CD, acompanhando a ruptura (1,2 ponto hoje) | Se a ruptura subir, o check só alerta e a correção passa para a conciliação (C) |
| H4 | O atraso de setembro (16%) não se sustenta sem a força-tarefa | Acompanhar outubro e novembro no CSV diário de títulos | Se se sustentar, P2 pesa menos e o quick win se apoia só em A |

### O que falta saber

| # | Pergunta | Para quem (por papel) | Por que importa |
| --- | --- | --- | --- |
| Q1 | Quanto dos R$ 543 mil de P1 é do CD e quanto é das lojas? | Controller | O CD tem 1,9 mil notas e cerca de 64% do valor (Dossiê, Anexo 1); define o alcance do check no CD |
| Q2 | Quanto custou a semana de força-tarefa de setembro, e o atraso de outubro já voltou a subir? | Controller e CFO | Define o baseline de P2 e o custo da alternativa atual |
| Q3 | Quando saem a credencial de serviço da captura de NF e o usuário de leitura no ERP, com o termo de confidencialidade? | Controller e área fiscal | Hoje a credencial é o login de um analista terceirizado; sem isso, o check não começa |
| Q4 | O jurídico aceita recusa parcial ou nota de devolução quando a divergência é vista antes da doca? | Controller, com o jurídico | Define se o check pode virar recusa parcial ou só alerta |
| Q5 | Por que abril concentrou quase 40% de P1? | Controller | Um evento único, como um fornecedor ou um item, muda a prioridade e o baseline |

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
