import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client, Client
from streamlit_autorefresh import st_autorefresh

# Configuração de tela mobile centrada de alta estabilidade
st.set_page_config(page_title="Central de Auditoria - Firebolt", page_icon="🖥️", layout="centered")

# Estilização visual Matrix/Cyberpunk de Controle Central
st.markdown("""
    <style>
    .stApp { background-color: #05070f; color: #ffffff; }
    header, footer, #MainMenu {visibility: hidden;}
    div[data-testid="stDecoration"] {display: none;}
    .main-title { color: #00ffcc; text-align: center; font-family: 'Courier New', monospace; font-size: 28px; font-weight: bold; margin-top: 15px; }
    .sub-title { text-align: center; font-size: 13px; color: #8892b0; margin-bottom: 25px; }
    
    /* Box de Auditoria Individual */
    .bot-box { background-color: #0b0f19; border: 1px solid #1e293b; border-radius: 8px; padding: 12px; margin-bottom: 12px; }
    .bot-name { font-size: 16px; font-weight: bold; font-family: 'Courier New', monospace; margin-bottom: 4px; }
    .bot-meta { font-size: 13px; color: #8892b0; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🖥️ CENTRAL DE AUDITORIA</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">📊 Monitoramento Consolidado do Ecossistema de AutoBots</div>', unsafe_allow_html=True)

# Atualizador nativo automático a cada 6 segundos para não estressar o banco
st_autorefresh(interval=6000, key="auditoria_heartbeat")

# --- CONEXÃO COM O BANCO CENTRAL ---
def puxar_dados_banco(tabela):
    try:
        url = st.secrets.get("SUPABASE_URL") or st.secrets.get("supabase_url")
        key = st.secrets.get("SUPABASE_KEY") or st.secrets.get("supabase_key")
        if url and key:
            supabase = create_client(url, key)
            res = supabase.table(tabela).select("*").eq("id", 1).execute()
            if res.data and len(res.data) > 0:
                return res.data[0]
    except: pass
    return {"saldo_usdt": 10000.0, "saldo_btc": 0.0, "bot_ativo": False}

# Varre as 3 tabelas em segundo plano no Supabase
dados_duck = puxar_dados_banco("duck_memory")
dados_lion = puxar_dados_banco("lion_memory")
dados_bot3 = puxar_dados_banco("bot3_memory")

# --- CÁLCULO DE PATRIMÔNIO LÍQUIDO (CONVERSÃO SIMULADA EM BASE BITCOIN TO USD) ---
total_duck = float(dados_duck.get('saldo_usdt', 10000.0)) + (float(dados_duck.get('saldo_btc', 0.0)) * 64000)
total_lion = float(dados_lion.get('saldo_usdt', 10000.0)) + (float(dados_lion.get('saldo_btc', 0.0)) * 64000)
total_bot3 = float(dados_bot3.get('saldo_usdt', 10000.0)) + (float(dados_bot3.get('saldo_btc', 0.0)) * 64000)

patrimonio_total_banca = total_duck + total_lion + total_bot3

# --- CARD DE PATRIMÔNIO CONSOLIDADO ---
st.metric(label="💰 VALOR TOTAL DO FUNDO QUANTITATIVO (USDT)", value=f"${patrimonio_total_banca:,.2f}", delta="Atualizando Globalmente")
st.write("---")

# --- 📊 GRÁFICO PLOTLY DE DISPUTA DE PERFORMANCE ---
st.write("### 📈 Disputa de Lucros (Patrimônio Líquido por Bot)")
df_performance = pd.DataFrame({
    'Robô': ['🦆 Duck Hunter', '🦁 LionBot', '🔥 SARA_FIREBOLT'],
    'Capital Atual ($)': [total_duck, total_lion, total_bot3]
})
fig = px.bar(df_performance, x='Robô', y='Capital Atual ($)', text_auto='.2f', color='Robô',
             color_discrete_sequence=['#00ffcc', '#ffaa00', '#ff4500']) # Laranja fogo para a Sara!
fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#ffffff", height=180, showlegend=False, xaxis_title=None, yaxis_title=None)
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.write("---")
st.write("### 📡 Status Individual dos Operadores")

# --- MURAL DOS APARTAMENTOS (MOBILES BOXES) ---
status_d = "🟢 EM OPERAÇÃO" if dados_duck.get('bot_ativo') else "🔴 PAUSADO"
st.markdown(f"""
    <div class="bot-box">
        <div class="bot-name" style="color: #00ffcc;">🦆 DUCK HUNTER</div>
        <div class="bot-meta"><b>Status:</b> {status_d} | <b>Saldo:</b> ${float(dados_duck.get('saldo_usdt', 10000.0)):,.2f} USDT</div>
    </div>
""", unsafe_allow_html=True)

status_l = "🟢 EM OPERAÇÃO" if dados_lion.get('bot_ativo') else "🔴 PAUSADO"
st.markdown(f"""
    <div class="bot-box">
        <div class="bot-name" style="color: #ffaa00;">🦁 LIONBOT</div>
        <div class="bot-meta"><b>Status:</b> {status_l} | <b>Saldo:</b> ${float(dados_lion.get('saldo_usdt', 10000.0)):,.2f} USDT</div>
    </div>
""", unsafe_allow_html=True)

status_b3 = "🟢 EM OPERAÇÃO" if dados_bot3.get('bot_ativo') else "🔴 PAUSADO"
st.markdown(f"""
    <div class="bot-box">
        <div class="bot-name" style="color: #ff4500;">🔥 SARA_FIREBOLT</div>
        <div class="bot-meta"><b>Status:</b> {status_b3} | <b>Saldo:</b> ${float(dados_bot3.get('saldo_usdt', 10000.0)):,.2f} USDT</div>
    </div>
""", unsafe_allow_html=True)
