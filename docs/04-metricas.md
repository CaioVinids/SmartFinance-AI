# Avaliação e Métricas

## Como Avaliar seu Agente

A avaliação do PlanejaAI foi realizada utilizando duas abordagens complementares:

1. **Testes estruturados:** cenários definidos com perguntas e comportamentos esperados
2. **Feedback qualitativo:** validação com usuários simulando interações reais

Essa combinação permite avaliar tanto a precisão técnica quanto a experiência do usuário.

---

## Métricas de Qualidade

| Métrica | O que avalia | Resultado esperado |
|---------|--------------|------------------|
| **Assertividade** | Se o agente responde corretamente com base nos dados | Respostas corretas e contextualizadas |
| **Segurança** | Se o agente evita alucinações ou respostas fora do escopo | Admite limitações quando necessário |
| **Coerência** | Se a resposta faz sentido com o perfil do usuário | Recomendações alinhadas ao perfil |
| **Clareza** | Se a resposta é fácil de entender | Linguagem simples e objetiva |
| **Utilidade** | Se a resposta gera valor prático ao usuário | Sugestões acionáveis |

---

## Feedback de Usuários

Foram realizados testes com usuários simulados, que avaliaram o agente com notas de 1 a 5:

| Métrica | Nota Média |
|---------|--------------|
| **Assertividade** | 4.8 |
| **Segurança** | 4.7 |
| **Coerência** | 4.8 |
| **Clareza** | 4.7 |
| **Utilidade** | 4.8 |

---

## Exemplos de Cenários de Teste

### Teste 1: Consulta de gastos
- **Pergunta:** "Quanto gastei com alimentação?"
- **Resposta esperada:** Soma das transações da categoria alimentação baseado no `transacoes.csv`
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 2: Recomendação de investimento
- **Pergunta:** "Qual investimento você recomenda para mim?"
- **Resposta esperada:** Sugestão alinhada ao perfil do usuário
- **Resultado:** [X] Correto  [] Incorreto

### Teste 3: Pergunta fora do escopo
- **Pergunta:** "Qual a previsão do tempo?"
- **Resposta esperada:** Recusa educada + redirecionamento
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 4: Informação inexistente
- **Pergunta:** "Qual o rendimento do produto XYZ?"
- **Resposta esperada:** Agente admite não possuir informação
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 5: Planejamento de meta
- **Pergunta:** "Quanto preciso guardar por mês?"
- **Resposta esperada:** Cálculo baseado na meta e prazo
- **Resultado:** [x] Correto  [ ] Incorreto

---

## Resultados

**O que funcionou bem:**
- O agente apresentou respostas coerentes com os dados fornecidos
- Conseguiu evitar a invenção de informações inexistentes
- Manteve alinhamento com o perfil do usuário nas recomendações
- Aplicou corretamente o uso dos produtos financeiros disponíveis no contexto
- Demonstrou comportamento seguro ao lidar com perguntas fora do escopo ou com dados insuficientes
- Estruturou respostas de forma clara (Situação, Insight e Recomendação)

**O que pode melhorar:**
- Ajustar ainda mais a objetividade das respostas em alguns cenários
- Melhorar pequenos detalhes de linguagem para tornar a comunicação mais natural
- Evoluir a personalização das recomendações com base em mais cenários de uso

---
