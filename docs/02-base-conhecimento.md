# Base de Conhecimento

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

```
import pandas as pd
import json

#CSVs
historico = pd.read_csv('data/historico_atendimento.csv')
transacoes = pd.read_csv('data/transacoes.csv')

#JSONs
with open('data/perfil_investidor.json', 'r', encoding='utf-8') as f:
    perfil = json.load(f)
with open('data/produtos_financeiros.json', 'r', encoding='utf-8') as f:
    produtos = json.load(f)
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Os dados são utilizados de forma híbrida. Parte das informações principais, como perfil do usuário e resumo financeiro, são incluídas no contexto do prompt para orientar a IA. Já os dados mais detalhados, como transações e produtos financeiros, são consultados dinamicamente conforme a necessidade da pergunta do usuário.

Dessa forma, o agente consegue manter respostas relevantes sem sobrecarregar o prompt, garantindo maior eficiência e precisão nas interações.

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dados do Cliente:
- Nome: João Silva
- Idade: 32 anos
- Perfil: Moderado
- Renda mensal: R$ 5.000
- Gastos mensais estimados: R$ 2.488,90
- Objetivo principal: Construir reserva de emergência
- Reserva atual: R$ 10.000

Metas:
- Completar reserva de emergência (R$ 15.000 até 2026-06)
- Entrada do apartamento (R$ 50.000 até 2027-12)

Resumo financeiro:
- Capacidade de economia mensal: aproximadamente R$ 2.500
- Maior gasto: Moradia

Últimas transações:
- 01/10: Salário + R$ 5.000
- 02/10: Aluguel - R$ 1.200
- 03/10: Supermercado - R$ 450
- 05/10: Netflix - R$ 55,90

Histórico recente:
- Interesse em CDB e Tesouro Selic
- Solicitação de planejamento financeiro
...
```
