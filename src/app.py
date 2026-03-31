import json  
import pandas as pd
import requests
import streamlit as st

# ============ Configuração da página ============
st.set_page_config(page_title="PlanejaAI", page_icon="💰")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"

# ============ Carrega o CSS externo ============
def load_css(path: str):
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("src/style.css")

# ============ HEADER ============
st.markdown(
    """ 
<div class="top-header"> 
<div class="header-logo"><span style="margin-right:8px; font-size:26px">💰</span>Planeja<span class="blue">AI</span></div> 
<div class="header-badge">Beta</div> 
</div> 

<div class="footer-bg-cover"></div>
""",
    unsafe_allow_html=True,
)

# ============ DADOS ============
perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))

transacoes['valor'] = transacoes['valor'].astype(float)

# ============ PRÉ-PROCESSAMENTO ============
total_receitas = transacoes[transacoes['tipo'] == 'entrada']['valor'].sum()
total_gastos = transacoes[transacoes['tipo'] == 'saida']['valor'].sum()
saldo = total_receitas - total_gastos

# gastos por categoria
gastos_categoria = transacoes[transacoes['tipo'] == 'saida'] \
    .groupby('categoria')['valor'].sum()

gastos_str = "\n".join([
    f"- {cat}: R$ {valor:.2f}"
    for cat, valor in gastos_categoria.items()
])

# metas
metas_lista = perfil.get('metas', [])
metas = "\n".join([
    f"- {m['meta']}: R$ {m['valor_necessario']} até {m['prazo']}"
    for m in metas_lista
]) if metas_lista else "Nenhuma meta"

# histórico resumido
historico_recente = historico.tail(3)

historico_str = "\n".join([
    f"- {row['tema']} ({row['intencao']})"
    for _, row in historico_recente.iterrows()
])

# ============ CONTEXTO ============
# produtos formatados
produtos_str = "\n".join([
    f"- {p['nome']} | risco: {p['risco']} | liquidez: {p['liquidez']} | objetivo: {p['objetivo_indicado']}"
    for p in produtos
])

contexto = f"""
Usuário: {perfil['nome']}, perfil {perfil['perfil_investidor']}
Renda: R$ {perfil['renda_mensal']}
Gastos: R$ {total_gastos}
Saldo: R$ {saldo}

Objetivo principal:
{perfil['objetivo_principal']}

Metas:
{metas}

Gastos por categoria:
{gastos_str}

Histórico recente:
{historico_str}

Produtos disponíveis:
{produtos_str}
"""

# ============ SYSTEM PROMPT ============
SYSTEM_PROMPT = """Você é o PlanejaAI, um agente de finanças pessoais.

OBJETIVO:
Ajudar o usuário a entender sua situação financeira e tomar decisões conscientes com base no contexto.

REGRAS:
- Use linguagem simples, educativa e neutra
- Todos os valores devem estar no formato: R$ 0.000,00
- Use apenas dados do contexto
- Nunca invente valores, datas ou informações
- Não estime prazos sem data atual explícita
- Não garanta retornos nem tome decisões pelo usuário
- Não solicite dados sensíveis
- Nunca forneça ou exponha dados sensíveis (ex: número de cartão, dados bancários)
- Quando o usuário solicitar esse tipo de informação, a resposta DEVE obrigatoriamente:
  1. Recusar de forma educada
  2. Explicar brevemente que se trata de informação sensível
  3. Redirecionar oferecendo ajuda em finanças pessoais

- Diferencie:
  → saldo mensal = valor disponível por mês  
  → valor acumulado = valor já guardado (somente se informado)  
- Nunca trate saldo mensal como valor acumulado

INVESTIMENTOS:
- Use apenas produtos do contexto
- Não sugira ativos externos
- Alinhe com perfil, objetivo e prazo
- Não sugira valores específicos de investimento
- Use linguagem consultiva (ex: "você pode considerar", "uma possibilidade é")
- Nunca imponha decisões

CÁLCULOS:
- Só calcule com dados completos
- Nunca invente números
- Não converta datas em períodos sem data atual

- Para metas:
  → valor restante = meta - valor acumulado (se informado)
  → só use valor acumulado se estiver explícito
  → nunca use saldo mensal como valor acumulado
  → só calcule valor mensal com prazo completo

- Se não for possível calcular:
  → explique o motivo
  → diga o que falta
  → explique como calcular (sem resultado final)

- Não sugira valores de economia ou cortes específicos

COMPORTAMENTO:
- Explique conceitos de forma simples e educativa
- Identifique padrões de gastos quando relevante
- Seja direto (máx. 3 blocos curtos)
- Priorize liquidez e segurança para curto prazo

FORMATO:
Se for análise ou recomendação:

Situação atual:
Insight:
Recomendação:

- Use quebra de linha entre seções
- Use frases curtas

Para perguntas simples:
- responda em uma frase direta

ESCOPO:
Apenas finanças pessoais.

FORA DO ESCOPO:
Responda educadamente e redirecione para finanças.
"""

# ============ FUNÇÃO IA ============
def perguntar(msg):
    prompt = f"""
{SYSTEM_PROMPT}

CONTEXTO:
{contexto}

PERGUNTA:
{msg}
"""
    try:
        r = requests.post(
            OLLAMA_URL,
            json={"model": MODELO, "prompt": prompt, "stream": False}
        )
        return r.json().get('response', 'Erro ao gerar resposta.')
    except:
        return "Erro na conexão com o modelo."

# ============ INTERFACE ============
st.markdown("""
<div style="text-align: center;">
    <h1>Como posso ajudar?</h1>
    <p style="font-size:18px; color: #000000;">
        Sou seu assistente financeiro inteligente
    </p>
</div>
""", unsafe_allow_html=True)

# Container fixo para a interação atual
chat_placeholder = st.container()

if pergunta_usuario := st.chat_input("Digite sua dúvida financeira..."):

    with chat_placeholder:
        st.chat_message("user").write(pergunta_usuario)
        
        with st.chat_message("assistant"):
            with st.spinner("Analisando..."):
                resposta = perguntar(pergunta_usuario)
                st.markdown(resposta)
