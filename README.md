# 💸 PlanejaAI — Educador Financeiro Inteligente

> Agente de educação financeira com IA Generativa, desenvolvido durante o **Bootcamp Bradesco – GenAI & Dados**.

---

## 🎯 Sobre o Projeto

O **PlanejaAI** é um agente financeiro inteligente que atua como educador e consultor pessoal de finanças. Ele analisa o perfil, histórico de transações e comportamento financeiro do usuário para oferecer orientações personalizadas, identificar padrões de gastos e sugerir metas.

**Problema que resolve:** A maioria das pessoas não tem acesso a um consultor financeiro. O PlanejaAI resolve isso usando IA generativa para oferecer orientação de forma simples e acessível.

---

## ✨ Funcionalidades

- 🧠 **Análise de perfil** — identifica o perfil do investidor (conservador, moderado, arrojado)
- 📊 **Diagnóstico financeiro** — interpreta histórico de transações e aponta padrões
- 🎯 **Planejamento de metas** — sugere objetivos com base na realidade do usuário
- 💬 **Educação contextual** — explica conceitos financeiros sob demanda, de forma didática
- 🛡️ **Respostas seguras** — arquitetura anti-alucinação com base de conhecimento estruturada

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
| LLM | API de IA Generativa (Ollama - Local) |
| Dados | CSV + JSON (mockados) |
| Linguagem | Python |

---

## 📄 Documentação

Toda a documentação do agente está na pasta [`docs/`](./docs):

- **[Documentação do Agente](./docs/01-documentacao-agente.md)** — persona, arquitetura e segurança
- **[Base de Conhecimento](./docs/02-base-conhecimento.md)** — estrutura e estratégia dos dados
- **[Prompts](./docs/03-prompts.md)** — system prompt, exemplos e edge cases
- **[Métricas](./docs/04-metricas.md)** — como a qualidade do agente é avaliada
- **[Pitch](./docs/05-pitch.md)** — apresentação do projeto

---

## 🤖 Agente

<img width="1915" height="1007" alt="image" src="https://github.com/user-attachments/assets/eb32ebb3-e3d8-4c37-8f94-0238bbe8e24a" />
