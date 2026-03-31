import json  
import pandas as pd
import requests
import streamlit as st
from datetime import datetime

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
data_hoje = datetime.now()
data_hoje_str = data_hoje.strftime("%d/%m/%Y")

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
    f"- {m['meta']}: R$ {m['valor_necessario']} (Prazo: {m['prazo']})"
    for m in metas_lista
]) if metas_lista else "Nenhuma meta"

# Histórico resumido
historico_recente = historico.tail(3)
historico_str = "\n".join([
    f"- {row['tema']} ({row['intencao']})"
    for _, row in historico_recente.iterrows()
])

# Produtos formatados
produtos_str = "\n".join([
    f"- {p['nome']} | risco: {p['risco']} | liquidez: {p['liquidez']} | objetivo: {p['objetivo_indicado']}"
    for p in produtos
])

# ============ CONTEXTO ============
contexto = f"""
DATA ATUAL: {data_hoje_str}
Usuário: {perfil['nome']}, perfil {perfil['perfil_investidor']}
Renda: R$ {perfil['renda_mensal']}
Gastos Mensais Totais: R$ {total_gastos}
Saldo Mensal Disponível: R$ {saldo}
Valor já acumulado em Reserva: R$ {perfil['reserva_emergencia_atual']}

Objetivo principal: 
{perfil['objetivo_principal']}

Metas ativas:
{metas}

Detalhamento de Gastos:
{gastos_str}

Produtos Financeiros Disponíveis:
{produtos_str}
"""

# ============ SYSTEM PROMPT ============
SYSTEM_PROMPT = """Você é o PlanejaAI, um agente de finanças pessoais.

OBJETIVO:
Ajudar o usuário a entender sua situação financeira e tomar decisões conscientes com base no contexto.

REGRAS:
- Use linguagem simples, educativa e neutra
- Todos os valores devem estar no formato: R$ 0.000,00 (com 2 casas decimais após a virugla)
- NUNCA use LaTeX, símbolos matemáticos complexos (como \\frac, \\text) ou colchetes do tipo \\[ \\].
- Sempre use "R$" (nunca "R ")
- Use apenas dados do contexto
- Nunca invente valores, datas ou informações
- Não estime prazos sem data atual explícita
- Não garanta retornos nem tome decisões pelo usuário
- Não solicite nem exponha dados sensíveis

DADOS SENSÍVEIS:
Se o usuário pedir dados sensíveis:
1. Recuse educadamente
2. Explique que é informação sensível
3. Redirecione para ajuda em finanças
Nunca responda apenas “não posso ajudar”

INTERPRETAÇÃO:
- saldo mensal = valor disponível por mês
- valor acumulado = valor já guardado (somente se informado)
- Nunca trate saldo mensal como valor acumulado

INVESTIMENTOS:
- Use apenas produtos do contexto
- Não sugira ativos externos
- Alinhe com perfil, objetivo e prazo
- Não sugira valores específicos
- Use linguagem consultiva (ex: “você pode considerar”)
- Nunca imponha decisões

CÁLCULOS:
- Use a DATA ATUAL fornecida para calcular prazos.
- Só calcule com dados completos
- Nunca invente números
- Nunca assuma valor acumulado como zero

Para metas:
- valor restante = meta - valor acumulado (se informado)
- só use valor acumulado se estiver explícito
- nunca use saldo mensal como valor acumulado
- só calcule valor mensal com prazo completo

Para prazo:
- só calcule com data atual explícita
- nunca converta datas em meses sem essa informação

Se não for possível calcular:
- explique o motivo
- diga o que falta
- explique como calcular (sem resultado final)

COMPORTAMENTO:
- Explique de forma simples e educativa (ensine o raciocínio)
- Seja direto (máx. 3 blocos curtos)
- Evite respostas genéricas
- Priorize liquidez e segurança no curto prazo

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
Responda educadamente e redirecione para finanças. (ex: posso ajudar com gastos, metas ou investimentos)

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
                
#streamlit run .\src\app.py
