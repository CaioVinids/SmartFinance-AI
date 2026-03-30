# 💸 PlanejaAI — Educador Financeiro Inteligente

> Agente de educação financeira com IA Generativa, desenvolvido durante o **Bootcamp Bradesco – GenAI & Dados**.

---

## 🎯 Sobre o Projeto

O **PlanejaAI** é um agente financeiro inteligente que atua como educador e consultor pessoal de finanças. 

Ele analisa dados como perfil do usuário, histórico de transações e metas financeiras para oferecer orientações personalizadas, ajudando na tomada de decisões mais conscientes.

**Problema que resolve:** Muitas pessoas não sabem para onde o dinheiro está indo e têm dificuldade em organizar suas finanças ou atingir metas. O PlanejaAI resolve isso oferecendo orientação financeira acessível, personalizada e baseada em dados.

---

## ✨ Funcionalidades

- 🧠 **Análise de perfil** — identifica o perfil do investidor (conservador, moderado, arrojado)
- 📊 **Diagnóstico financeiro** — interpreta transações e identifica padrões de gastos
- 🎯 **Planejamento de metas** — calcula quanto economizar e sugere estratégias
- 💬 **Educação contextual** — explica conceitos financeiros de forma simples
- 🛡️ **Respostas seguras** — evita alucinações e usa apenas dados do contexto

---

## 🗂️ Estrutura do Repositório

```
SmartFinance-AI/
│
├── data/
│   ├── transacoes.csv              # Histórico de transações do usuário
│   ├── historico_atendimento.csv   # Atendimentos anteriores
│   ├── perfil_investidor.json      # Perfil e preferências do usuário
│   └── produtos_financeiros.json   # Produtos e serviços disponíveis
│
├── docs/
│   ├── 01-documentacao-agente.md   # Caso de uso, persona e arquitetura
│   ├── 02-base-conhecimento.md     # Estratégia de dados e fontes
│   ├── 03-prompts.md               # Engenharia de prompts (system + exemplos)
│   ├── 04-metricas.md              # Avaliação, métricas e testes
│   └── 05-pitch.md                 # Roteiro do pitch (3 min)
│
├── src/
│   └── app.py                      # Aplicação principal (Streamlit)
│   ├── style.css                   # Estilização da interface
│   └── README.md                   # Instruções de instalação e execução
│
└── README.md
```

---

## 🛠️ Tecnologias

| Camada | Tecnologia |
|---|---|
| Interface | Streamlit + CSS |
| LLM | Ollama (modelo Local) |
| Dados | CSV + JSON (mockados) |
| Linguagem | Python |

---

## 📄 Documentação

Toda a documentação do agente está na pasta [`docs/`](./docs):

- **[Documentação do Agente](./docs/01-documentacao-agente.md)** — arquitetura, persona e segurança
- **[Base de Conhecimento](./docs/02-base-conhecimento.md)** — estrutura e uso dos dados
- **[Prompts](./docs/03-prompts.md)** — system prompt e comportamento do agente
- **[Métricas](./docs/04-metricas.md)** — avaliação e testes
- **[Pitch](./docs/05-pitch.md)** — apresentação do projeto

---

## 🚀 Como Executar

As instruções para execução do projeto estão na pasta [`src/`](./src):

- **[Passo a Passo de Execução](./src/README.md)**

---

## 🤖 Agente

<img width="1915" height="1007" alt="image" src="https://github.com/user-attachments/assets/eb32ebb3-e3d8-4c37-8f94-0238bbe8e24a" />
