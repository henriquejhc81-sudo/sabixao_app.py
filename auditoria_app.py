import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client, Client
from streamlit_autorefresh import st_autorefresh

# Configuração de tela mobile centrada de alta estabilidade
st.set_page_config(page_title="Central de Auditoria", page_icon="🖥️", layout="centered")

# Estilização visual Matrix/Cyberpunk Ultra Compacta (Sem rolagem de tela)
st.markdown("""
    <style>
    .stApp { background-color: #05070f; color: #ffffff; }
    header, footer, #MainMenu {visibility: hidden;}
    div[data-testid="stDecoration"] {display: none;}
    
    /* Fontes e títulos reduzidos para telas pequenas */
    .main-title { color: #00ffcc; text-align: center; font-family: 'Courier New', monospace; font-size: 24px; font-weight: bold; margin-top: 10px; }
    .sub-title { text-align: center; font-size: 11px; color: #8892b0; margin-bottom: 15px; }
    
    /* Grid horizontal compacto para os status individuais no celular */
    .status-container { display: flex; justify-content: space-between; gap: 8px; margin-top: 15px; }
    .status-card { background-color: #0b0f19; border: 1px solid #1e293b; border-radius: 6px; padding: 8px; flex: 1; text-align: center; }
    .status-label { font-size: 10px; font-weight: bold; text-transform: uppercase; }
    .status-val { font-size: 13px; font-weight: bold; margin-top: 3px; }
    .status-state { font-size: 9px; margin-top: 2px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🖥️ CENTRAL DE AUDITORIA</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Monitoramento Consolidado do Ecossistema de AutoBots</div>', unsafe_allow_html=True)

# Atualizador nativo automático a cada 6 segundos
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

dados_duck = puxar_dados_banco("duck_memory")
dados_lion = puxar_dados_banco("lion_memory")
dados_bot3 = puxar_dados_banco("bot3_memory")

# Integração matemática dinâmica baseada no Bitcoin real
total_duck = float(dados_duck.get('saldo_usdt', 10000.0)) + (float(dados_duck.get('saldo_btc', 0.0)) * 64000)
total_lion = float(dados_lion.get('saldo_usdt', 10000.0)) + (float(dados_lion.get('saldo_btc', 0.0)) * 64000)
total_bot3 = float(dados_bot3.get('saldo_usdt', 10000.0)) + (float(dados_bot3.get('saldo_btc', 0.0)) * 64000)

patrimonio_total_banca = total_duck + total_lion + total_bot3

# --- CARD GLOBAL REDUZIDO ---
st.metric(label="💰 VALOR TOTAL DO FUNDO QUANTITATIVO (USDT)", value=f"${patrimonio_total_banca:,.2f}")

# --- 📊 GRÁFICO PLOTLY COMPACTO ---
df_performance = pd.DataFrame({
    'Robô': ['🦆 Duck', '🦁 Lion', '🔥 Sara'],
    'Capital Actual ($)': [total_duck, total_lion, total_bot3]
})
fig = px.bar(df_performance, x='Robô', y='Capital Actual ($)', text_auto='.2f', color='Robô',
             color_discrete_sequence=['#00ffcc', '#ffaa00', '#ff4500'])
fig.update_layout(margin=dict(l=5, r=5, t=5, b=5), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#ffffff", height=150, showlegend=False, xaxis_title=None, yaxis_title=None)
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# --- MURAL HORIZONTAL MOBILE DE MÁXIMA COMPACTAÇÃO ---
state_duck = "🟢 ON" if dados_duck.get('bot_ativo') else "🔴 OFF"
state_lion = "🟢 ON" if dados_lion.get('bot_ativo') else "🔴 OFF"
state_sara = "🟢 ON" if dados_bot3.get('bot_ativo') else "🔴 OFF"

st.markdown(f"""
    <div class="status-container">
        <div class="status-card">
            <div class="status-label" style="color: #00ffcc;">🦆 Duck Hunter</div>
            <div class="status-val">${total_duck:,.0f}</div>
            <div class="status-state" style="color: {'#00ffcc' if state_duck == '🟢 ON' else '#ff3366'};">{state_duck}</div>
        </div>
        <div class="status-card">
            <div class="status-label" style="color: #ffaa00;">🦁 LionBot</div>
            <div class="status-val">${total_lion:,.0f}</div>
            <div class="status-state" style="color: {'#ffaa00' if state_lion == '🟢 ON' else '#ff3366'};">{state_lion}</div>
        </div>
        <div class="status-card">
            <div class="status-label" style="color: #ff4500;">🔥 Firebolt</div>
            <div class="status-val">${total_bot3:,.0f}</div>
            <div class="status-state" style="color: {'#ff4500' if state_sara == '🟢 ON' else '#ff3366'};">{state_sara}</div>
        </div>
    </div>
""", unsafe_allow_html=True)
