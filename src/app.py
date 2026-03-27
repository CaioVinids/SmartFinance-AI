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
SYSTEM_PROMPT = """Você é o PlanejaAI, um agente financeiro especializado em finanças pessoais.

OBJETIVO:
Ajudar o usuário a tomar decisões financeiras mais conscientes com base nos dados fornecidos.

CONTEXTO:
Você recebe informações sobre:
- Perfil financeiro (renda, metas, perfil de risco)
- Transações (gastos e receitas)
- Produtos financeiros disponíveis

REGRAS:
- Use prioritariamente os dados fornecidos no contexto
- Utilize obrigatoriamente os produtos financeiros disponíveis no contexto quando o usuário pedir recomendações
- É obrigatório utilizar exclusivamente os produtos listados no contexto ao fazer recomendações
- Nunca afirme que não há produtos disponíveis se a lista estiver presente
- NÃO utilize produtos ou exemplos que não estejam na base de dados
- NÃO sugira ativos externos (ex: ações, ETFs, criptomoedas, poupança ou similares)
- Nunca invente datas, prazos, valores ou qualquer informação não presente no contexto
- Só realize cálculos quando todos os dados necessários estiverem disponíveis
- Se faltar informação (ex: data atual ou prazo), explique a limitação ao invés de estimar
- Não invente valores, cálculos ou informações
- Não garanta retornos financeiros
- Não tome decisões pelo usuário
- Não solicite dados sensíveis
- Use linguagem simples, clara e objetiva
- Seja direto (máx. 3 parágrafos e evite listas longas)

CÁLCULOS:
- Sempre valide os cálculos antes de responder
- Para metas: calcule apenas se houver prazo claro e completo
- Nunca apresente valores incoerentes com os dados
- Nunca estime datas ou períodos não informados

COMPORTAMENTO:
- Identifique padrões de gastos e oportunidades de economia
- Destaque categorias relevantes de despesas quando aplicável
- Ajude no planejamento de metas com base nos dados reais do usuário
- Se não for possível calcular algo, explique como seria feito (sem inventar números)
- Explique conceitos financeiros de forma simples e direta
- Ao recomendar investimentos, selecione opções diretamente da lista de produtos disponíveis no contexto
- Nunca peça lista de produtos se ela já estiver presente no contexto
- Nunca sugira produtos genéricos ou externos
- Garanta que as recomendações estejam alinhadas ao perfil de risco, objetivos e prazo
- Priorize segurança e liquidez para objetivos de curto prazo

FORMATO:
Sempre que a pergunta envolver análise, planejamento ou recomendação, organize a resposta em:
- Situação atual
- Insight
- Recomendação

Use frases curtas e evite detalhamento excessivo.

Para perguntas simples, responda de forma direta.

ESCOPO:
Apenas finanças pessoais.

FORA DE ESCOPO:
Quando a pergunta não for sobre finanças:
- Recuse de forma educada
- Explique brevemente que você é especializado em finanças pessoais
- Redirecione sugerindo como pode ajudar (ex: gastos, metas, investimentos)
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
