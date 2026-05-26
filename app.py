import streamlit as st
import asyncio
import os
from main import SabixaoSistemaUniversal

# Configuração da página Web/Mobile
st.set_page_config(
    page_title="Sabixão - Sistema Universal",
    page_icon="🧠",
    layout="centered"
)

# Estilização básica para o título
st.title("🧠 Sabixão")
st.subheader("O Sabichão Universal - Conhecimento Global Multimodal")
st.write("Resolva qualquer questão por texto, arquivos ou capturas de câmera.")

# Inicializa o sistema do Sabixão em cache para não recarregar do zero a cada clique
@st.cache_resource
def inicializar_sistema():
    return SabixaoSistemaUniversal()

sabixao = inicializar_sistema()

# Interface de Abas: Uma para Texto Puro e outra para Mídia (Imagens/Câmera)
aba_texto, aba_midia = st.tabs(["💬 Pergunta em Texto", "📸 Entrada por Imagem / Cam"])

with aba_texto:
    pergunta_input = st.text_area("Digite sua dúvida ou problema (do simples ao mais complexo):", placeholder="Ex: Explique como funciona o motor de dobra espacial...")
    
    if st.button("Executar Análise Master", key="btn_texto"):
        if pergunta_input:
            with st.spinner("O Sabixão está varrendo as redes e orquestrando as IAs..."):
                # Executa o fluxo assíncrono do Sabixão dentro da interface web
                resposta = asyncio.run(sabixao.processar_requisicao(pergunta_texto=pergunta_input))
                st.success("Análise Concluída!")
                st.markdown(f"### 🤖 Resposta Humana do Sabixão:\n{resposta}")
        else:
            st.warning("Por favor, digite uma pergunta.")

with aba_midia:
    st.write("Envie um print de tela ou use a câmera do seu PC/Celular:")
    
    # Opção 1: Upload de Arquivo/Print
    arquivo_upload = st.file_uploader("Escolha um arquivo de imagem (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
    
    # Opção 2: Captura direta da Câmera (funciona em Mobile e Desktop)
    foto_camera = st.camera_input("Ou tire uma foto em tempo real:")
    
    texto_adicional = st.text_input("Algum contexto ou comando adicional para a imagem? (Opcional)")

    if st.button("Escanear e Resolver", key="btn_midia"):
        midia_para_processar = None
        caminho_temporario = "temp_captura.png"

        # Verifica qual entrada de mídia o usuário escolheu
        if foto_camera is not None:
            midia_para_processar = foto_camera.getvalue()
        elif arquivo_upload is not None:
            midia_para_processar = arquivo_upload.getvalue()

        if midia_para_processar:
            with st.spinner("Tratando imagem via OpenCV e escaneando conteúdo..."):
                # Salva a imagem temporariamente na máquina para o módulo OpenCV ler
                with open(caminho_temporario, "wb") as f:
                    f.write(midia_para_processar)
                
                # Envia o caminho da imagem salva para o pipeline do Sabixão
                resposta = asyncio.run(sabixao.processar_requisicao(
                    pergunta_texto=texto_adicional, 
                    caminho_imagem=caminho_temporario
                ))
                
                st.success("Imagem decodificada com sucesso!")
                st.markdown(f"### 🤖 Resposta Humana do Sabixão:\n{resposta}")
                
                # Remove o arquivo temporário após o uso para não entulhar o sistema
                if os.path.exists(caminho_temporario):
                    os.remove(caminho_temporario)
        else:
            st.warning("Por favor, envie um arquivo ou tire uma foto com a câmera.")

# Rodapé do sistema
st.markdown("---")
st.caption("Sabixão v1.0 • Sistema Híbrido Hidra (Gemini + Groq) • Conexões Invisíveis Ativas")
