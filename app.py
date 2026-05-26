import streamlit as st
import asyncio
import os
from main import SabixaoSistemaUniversal

# Configuração da página Premium
st.set_page_config(
    page_title="Sabixão Search",
    page_icon="🧠",
    layout="centered"
)

# Injeção de CSS para emular a interface minimalista e limpa do Google
st.markdown("""
    <style>
    .block-container { padding-top: 5rem; max-width: 650px; }
    .stTextArea textarea {
        border-radius: 24px !important;
        padding-left: 20px !important;
        padding-right: 50px !important;
        border: 1px solid #dfe1e5 !important;
        box-shadow: none !important;
    }
    .stTextArea textarea:focus {
        border-color: transparent !important;
        box-shadow: 0 1px 6px rgba(32,33,36,0.28) !important;
    }
    div.stButton > button {
        border-radius: 4px !important;
        background-color: #f8f9fa !important;
        color: #3c4043 !important;
        border: 1px solid #f8f9fa !important;
        padding: 6px 16px !important;
        margin: 10px auto !important;
        display: block !important;
    }
    div.stButton > button:hover {
        border: 1px solid #dadce0 !important;
        color: #202124 !important;
        background-color: #f8f9fa !important;
    }
    </style>
""", unsafe_allow_html=True)

# Centralização da Marca
st.markdown("<h1 style='text-align: center; font-size: 4.5rem; font-weight: bold; margin-bottom: 0px;'>Sabixão</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #70757a; font-size: 14px; margin-bottom: 30px;'>O Motor de Respostas Universal Indestrutível</p>", unsafe_allow_html=True)

@st.cache_resource
def inicializar_sistema():
    return SabixaoSistemaUniversal()

sabixao = inicializar_sistema()

# Estado da interface para controlar se o "Google Lens" (Upload/Cam) está aberto
if "mostrar_lens" not in st.session_state:
    st.session_state.mostrar_lens = False

# Barra de pesquisa unificada
pergunta_input = st.text_area("", placeholder="Pesquise no Sabixão ou pergunte qualquer coisa...", label_visibility="collapsed")

# Botão simulando o Ícone do Google Lens logo abaixo/ao lado da busca
col1, col2 = st.columns([5, 1])
with col2:
    if st.button("📸 Lens"):
        st.session_state.mostrar_lens = not st.session_state.mostrar_lens

# Painel Expansível do Google Lens (SÓ APARECE SE CLICADO, RESOLVENDO O PROBLEMA DA CÂMERA)
midia_para_processar = None
caminho_temporario = "temp_captura.png"

if st.session_state.mostrar_lens:
    st.markdown("<div style='background-color: #f1f3f4; padding: 15px; border-radius: 12px; margin-bottom: 15px;'>", unsafe_allow_html=True)
    st.write("🤖 **Sabixão Lens Ativado**")
    
    tipo_entrada = st.radio("Escolha o modo de captura:", ["Upload de Imagem (Print/Arquivo)", "Usar Câmera Real"], horizontal=True)
    
    if tipo_entrada == "Usar Câmera Real":
        foto_camera = st.camera_input("Posicione o problema na câmera:")
        if foto_camera:
            midia_para_processar = foto_camera.getvalue()
    else:
        arquivo_upload = st.file_uploader("Arraste seu print ou arquivo aqui", type=["png", "jpg", "jpeg"])
        if arquivo_upload:
            midia_para_processar = arquivo_upload.getvalue()
    st.markdown("</div>", unsafe_allow_html=True)

# Botão Central de Execução (Estilo "Pesquisa Google")
if st.button("Pesquisa Sabixão"):
    # Validação de Chaves de Segurança ocultas no Streamlit Secrets
    if not os.getenv("GEMINI_API_KEY") and not os-getenv("GROQ_API_KEY"):
        st.error("Erro Crítico: Chaves de API não encontradas no Advanced Settings do Streamlit.")
    
    elif pergunta_input or midia_para_processar:
        with st.spinner("O Sabixão está varrendo o planeta e consolidando o conhecimento..."):
            
            # Se houver mídia capturada pelo Lens
            if midia_para_processar:
                with open(caminho_temporario, "wb") as f:
                    f.write(midia_para_processar)
                
                resposta = asyncio.run(sabixao.processar_requisicao(
                    pergunta_texto=pergunta_input, 
                    caminho_imagem=caminho_temporario
                ))
                
                if os.path.exists(caminho_temporario):
                    os.remove(caminho_temporario)
            
            # Se for apenas texto direto na barra
            else:
                resposta = asyncio.run(sabixao.processar_requisicao(pergunta_texto=pergunta_input))
            
            # Exibição Premium do Resultado
            st.markdown("---")
            st.markdown(f"### 🎯 Resposta Humana do Sabixão:\n{resposta}")
    else:
        st.warning("Insira uma pergunta ou ative o Lens para escanear uma imagem.")

# Rodapé minimalista corporativo
st.markdown("<br><br><br><hr><p style='text-align: center; color: #70757a; font-size: 12px;'>Sabixão v2.0 Global • Conexões Ocultas Ativas • Proteção Hidra</p>", unsafe_allow_html=True)
