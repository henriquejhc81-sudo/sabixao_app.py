import streamlit as st
import asyncio
import os
from main import SabixaoSistemaUniversal

st.set_page_config(page_title="Sabixão Quantum Search", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #0a0f1d 0%, #030712 100%) !important; color: #e2e8f0 !important; }
    .block-container { padding-top: 3rem; max-width: 700px; }
    .stTextArea textarea {
        background-color: rgba(15, 23, 42, 0.6) !important; border: 2px solid #00f2fe !important;
        border-radius: 16px !important; color: #00f2fe !important; padding: 15px 20px !important;
        font-family: 'Courier New', Courier, monospace; box-shadow: 0 0 15px rgba(0, 242, 254, 0.2) !important;
    }
    .stTextArea textarea:focus { border-color: #4facfe !important; box-shadow: 0 0 25px rgba(79, 172, 254, 0.5) !important; }
    div.stButton > button {
        border-radius: 8px !important; background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
        color: #030712 !important; border: none !important; font-weight: bold !important;
        font-family: 'Courier New', Courier, monospace; letter-spacing: 1px; padding: 10px 20px !important;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.4) !important; transition: all 0.3s ease !important; width: 100% !important;
    }
    div.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 0 25px rgba(0, 242, 254, 0.8) !important; color: #ffffff !important; }
    .sub-panel { background-color: rgba(30, 41, 59, 0.5); border: 1px dashed #4facfe; padding: 20px; border-radius: 12px; margin-top: 15px; margin-bottom: 15px; box-shadow: inset 0 0 10px rgba(79, 172, 254, 0.1); }
    /* Estilização do balão de chat */
    .stChatMessage { background-color: rgba(15, 23, 42, 0.5); border-radius: 10px; border-left: 3px solid #00f2fe; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; font-size: 5rem; font-weight: 900; background: linear-gradient(to right, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0px; filter: drop-shadow(0 0 15px rgba(0,242,254,0.3));'>SABIXÃO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4facfe; font-family: monospace; font-size: 13px; letter-spacing: 3px; margin-bottom: 10px;'>QUANTUM OMNI SYSTEM v2.7</p>", unsafe_allow_html=True)

@st.cache_resource
def inicializar_sistema():
    return SabixaoSistemaUniversal()

sabixao = inicializar_sistema()

if "modo_camera" not in st.session_state: st.session_state.modo_camera = False
if "modo_arquivo" not in st.session_state: st.session_state.modo_arquivo = False
if "messages" not in st.session_state: st.session_state.messages = []

# Exibe o histórico de chat na tela
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

pergunta_input = st.text_area("", placeholder="[CONEXÃO SEGURA] Fale comigo naturalmente, envie links ou faça perguntas...", label_visibility="collapsed")
col_cam, col_file, col_search = st.columns([1, 1, 1.5])

with col_cam:
    if st.button("📷 LENS CAM"):
        st.session_state.modo_camera = not st.session_state.modo_camera
        st.session_state.modo_arquivo = False

with col_file:
    if st.button("📁 UPLOAD DATA"):
        st.session_state.modo_arquivo = not st.session_state.modo_arquivo
        st.session_state.modo_camera = False

with col_search:
    executar_busca = st.button("⚡ CONVERSAR")

midia_para_processar = None
caminho_temporario = "temp_captura.png"

if st.session_state.modo_camera:
    st.markdown("<div class='sub-panel'>", unsafe_allow_html=True)
    foto_camera = st.camera_input("Aponte para o problema físico ou documento:")
    if foto_camera: midia_para_processar = foto_camera.getvalue()
    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.modo_arquivo:
    st.markdown("<div class='sub-panel'>", unsafe_allow_html=True)
    arquivo_upload = st.file_uploader("Arraste qualquer tipo de arquivo (Imagens, Textos)", type=None)
    if arquivo_upload: midia_para_processar = arquivo_upload.getvalue()
    st.markdown("</div>", unsafe_allow_html=True)

if executar_busca:
    if pergunta_input or midia_para_processar:
        texto_exibicao = pergunta_input if pergunta_input else "[Arquivo Enviado]"
        
        # Adiciona a mensagem do usuário no chat
        st.session_state.messages.append({"role": "user", "content": texto_exibicao})
        st.rerun() # Atualiza a tela para mostrar a bolha do usuário
        
    else:
        st.warning("Fale algo comigo ou envie um arquivo para analisarmos.")

# Gatilho de Processamento da Resposta do Sabixão
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    ultima_mensagem = st.session_state.messages[-1]["content"]
    
    with st.spinner("Pensando..."):
        if midia_para_processar:
            with open(caminho_temporario, "wb") as f:
                f.write(midia_para_processar)
            resposta = asyncio.run(sabixao.processar_requisicao(pergunta_texto=ultima_mensagem, caminho_imagem=caminho_temporario))
            if os.path.exists(caminho_temporario): os.remove(caminho_temporario)
            midia_para_processar = None # Reseta a mídia
        else:
            resposta = asyncio.run(sabixao.processar_requisicao(pergunta_texto=ultima_mensagem))
        
        # Adiciona a resposta humanizada do Sabixão no chat
        st.session_state.messages.append({"role": "assistant", "content": resposta})
        st.rerun()

st.markdown("<br><br><br><hr style='border: 1px solid rgba(0, 242, 254, 0.1);'><p style='text-align: center; color: #4b5563; font-family: monospace; font-size: 11px;'>SABIXÃO OMNI SYSTEM • HIDRA PROTOCOL ACTIVE • HUMANIZED ENGINE</p>", unsafe_allow_html=True)
