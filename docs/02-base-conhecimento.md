# Base de Conhecimento

> [!TIP]
> Prompt Utilizado para esta etapa: Preciso organizar a base de conhecimento do meu agente financeiro inteligente. Tenho estes arquivos de dados [liste os arquivos].
> 
> Me ajuda a:
> - Entender o que cada arquivo contém
> - Decidir como usar cada um dentro do agente
> - Criar um exemplo de contexto formatado para incluir no prompt
> 
> Use o template abaixo como base:
> 
> [cole o template 02-base-conhecimento.md]

---

## Dados Utilizados

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Manter contexto e adaptar respostas com base em interações anteriores |
| `perfil_investidor.json` | JSON | Definir perfil, metas e orientar decisões financeiras  |
| `produtos_financeiros.json` | JSON | Sugerir produtos conforme perfil, objetivos e restrições |
| `transacoes.csv` | CSV | Analisar padrão de gastos do usuário, usar essas informações de forma didática, gerar alertas e apoiar simulações |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Os dados mockados foram complementados para permitir análises mais completas e personalizadas pelo agente. No arquivo de transações, foram adicionadas colunas como forma de pagamento e identificação de despesas fixas, possibilitando a distinção entre gastos recorrentes e variáveis.

No perfil do investidor, foram incluídos novos atributos como gastos mensais estimados, tolerância à perda, horizonte de investimento e preferências, permitindo uma personalização mais precisa das recomendações.

Já na base de produtos financeiros, foram adicionadas informações como liquidez, prazo mínimo, impostos e objetivo indicado, facilitando a comparação e sugestão de investimentos adequados ao perfil do usuário.

Por fim, o histórico de atendimento foi expandido com campos de intenção e nível de satisfação, permitindo ao agente compreender melhor o comportamento do usuário e adaptar suas respostas ao longo do tempo.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Os arquivos CSV e JSON são carregados no início da execução do sistema, utilizando Python para leitura e estruturação dos dados.

Injetar os dados diretamente no prompt (Ctrl + C + Ctrl + V) ou carregar os arquivos via código, como no exemplo abaixo:

```python
import json
import pandas as pd

# ============ Carregar os dados ============
perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Os dados são utilizados de forma híbrida. Parte das informações principais, como perfil do usuário e resumo financeiro, são incluídas no contexto do prompt para orientar a IA. Já os dados mais detalhados, como transações e produtos financeiros, são consultados dinamicamente conforme a necessidade da pergunta do usuário.

Dessa forma, o agente consegue manter respostas relevantes sem sobrecarregar o prompt, garantindo maior eficiência e precisão nas interações.

```text
DADOS DO CLIENTE E PERFIL (data/perfil_investidor.json):
{
  "nome": "Matheus Silva",
  "idade": 32,
  "profissao": "Analista de Sistemas",
  "renda_mensal": 5000.00,
  "gastos_mensais_estimados": 2488.90,
  "perfil_investidor": "moderado",
  "tolerancia_perda": "baixa",
  "horizonte_investimento": "medio_prazo",
  "objetivo_principal": "Construir reserva de emergência",
  "patrimonio_total": 15000.00,
  "reserva_emergencia_atual": 10000.00,
  "aceita_risco": false,
  "preferencias": {
    "liquidez": true,
    "isento_ir": true
  },
  "metas": [
    {
      "meta": "Completar reserva de emergência",
      "valor_necessario": 15000.00,
      "prazo": "2026-06",
      "prioridade": "alta"
    },
    {
      "meta": "Entrada do apartamento",
      "valor_necessario": 50000.00,
      "prazo": "2027-12",
      "prioridade": "media"
    }
  ]
}

TRANSAÇÕES DO CLIENTE (data/transacoes.csv):
data,descricao,categoria,valor,tipo,forma_pagamento,fixo,recorrente
2025-10-01,Salário,receita,5000.00,entrada,pix,não,sim
2025-10-02,Aluguel,moradia,1200.00,saida,pix,sim,sim
2025-10-03,Supermercado,alimentacao,450.00,saida,debito,não,não
2025-10-05,Netflix,lazer,55.90,saida,credito,sim,sim
2025-10-07,Farmácia,saude,89.00,saida,debito,não,não
2025-10-10,Restaurante,alimentacao,120.00,saida,credito,não,não
2025-10-12,Uber,transporte,45.00,saida,credito,não,não
2025-10-15,Conta de Luz,moradia,180.00,saida,pix,sim,sim
2025-10-20,Academia,saude,99.00,saida,credito,sim,sim
2025-10-25,Combustível,transporte,250.00,saida,debito,não,não

HISTORICO DE ATENDIMENTO DO CLIENTE (data/historico_atendimento.csv):
data,canal,tema,resumo,resolvido,intencao,satisfacao
2025-09-10,chat,Investimentos,Cliente pediu informações sobre CDB,sim,investimento,4
2025-09-15,app,Erro no app,Erro ao acessar extrato,não,suporte,2
2025-09-20,chat,Investimentos,Explicação sobre Tesouro Selic,sim,investimento,5
2025-09-25,telefone,Atualização cadastral,Atualização de dados pessoais,sim,suporte,4
2025-09-30,chat,Planejamento financeiro,Cliente solicitou ajuda para definir metas,sim,planejamento,5

PRODUTOS DISPONIVEIS PARA ENSINO (data/produtos_financeiros.json):
[
  {
    "nome": "Tesouro Selic",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "100% da Selic",
    "aporte_minimo": 30.00,
    "liquidez": "diaria",
    "prazo_minimo": "0 dias",
    "imposto": "IR regressivo",
    "objetivo_indicado": "reserva_emergencia",
    "indicado_para": "Reserva de emergência e iniciantes"
  },
  {
    "nome": "CDB Liquidez Diária",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "102% do CDI",
    "aporte_minimo": 100.00,
    "liquidez": "diaria",
    "prazo_minimo": "0 dias",
    "imposto": "IR regressivo",
    "objetivo_indicado": "reserva_emergencia",
    "indicado_para": "Quem busca segurança com rendimento diário"
  },
  {
    "nome": "LCI/LCA",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "95% do CDI",
    "aporte_minimo": 1000.00,
    "liquidez": "baixa",
    "prazo_minimo": "90 dias",
    "imposto": "isento",
    "objetivo_indicado": "medio_prazo",
    "indicado_para": "Quem pode esperar 90 dias (isento de IR)"
  },
  {
    "nome": "Fundo Multimercado",
    "categoria": "fundo",
    "risco": "medio",
    "rentabilidade": "CDI + 2%",
    "aporte_minimo": 500.00,
    "liquidez": "media",
    "prazo_minimo": "30 dias",
    "imposto": "IR regressivo",
    "objetivo_indicado": "diversificacao",
    "indicado_para": "Perfil moderado que busca diversificação"
  },
  {
    "nome": "Fundo de Ações",
    "categoria": "fundo",
    "risco": "alto",
    "rentabilidade": "variavel",
    "aporte_minimo": 100.00,
    "liquidez": "baixa",
    "prazo_minimo": "30 dias",
    "imposto": "IR regressivo",
    "objetivo_indicado": "longo_prazo",
    "indicado_para": "Perfil arrojado com foco no longo prazo"
  }
]

```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dados do Cliente:
- Nome: Matheus Silva
- Idade: 32 anos
- Profissão: Analista de Sistemas
- Perfil de Investidor: Moderado
- Tolerância a perda: Baixa
- Renda mensal: R$ 5.000
- Gastos mensais estimados: R$ 2.488,90
- Capacidade de economia: ~R$ 2.500

Metas:
Completar reserva de emergência
- Valor necessário: R$ 15.000
- Valor atual: R$ 10.000
- Prioridade: Alta
Entrada do apartamento
- Valor necessário: R$ 50.000
- Prazo: 12-2027
- Prioridade: Média

Resumo financeiro:
- Percentual de gastos: 50% da renda
- Maior categoria de gasto: Moradia
- Situação: Financeiramente equilibrada, com boa capacidade de poupança

Últimas transações:
- 01/10: Salário + R$ 5.000
- 02/10: Aluguel - R$ 1.200 (fixo)
- 03/10: Supermercado - R$ 450
- 05/10: Netflix - R$ 55,90 (fixo)

Histórico recente:
- Interesse em CDB e Tesouro Selic
- Solicitação de planejamento financeiro
...
```

---
