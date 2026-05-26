import asyncio
import os
import streamlit as st

from orquestrador import OrquestradorMaster
from varredura_invisivel import VarredorInvisivel
from percepcao_visao import PercepcaoVisao

class SabixaoSistemaUniversal:
    def __init__(self):
        print("\n=========================================================")
        print("          SABIXÃO - SISTEMA UNIVERSAL ATIVADO            ")
        print("=========================================================\n")
        
        self.orquestrador = OrquestradorMaster()
        self.varredor = VarredorInvisivel()
        self.visao = PercepcaoVisao()

    async def processar_requisicao(self, pergunta_texto: str = None, caminho_imagem: str = None):
        """
        Fluxo unificado: Lê arquivos/imagens se houver, varre a internet 
        de forma oculta e decide a resposta através do algoritmo Hidra.
        """
        questao_final = ""

        # Passo 1: Processamento de dados visuais via OCR integrado
        if caminho_imagem:
            print(f"[*] Detectada entrada visual. Processando arquivo: {caminho_imagem}")
            texto_da_imagem = self.visao.extrair_texto_de_arquivo(caminho_imagem)
            questao_final = f"{texto_da_imagem} | Contexto adicional: {pergunta_texto or ''}"
        else:
            questao_final = pergunta_texto

        if not questao_final:
            return "[Aviso] Nenhuma diretriz de dados ou questão foi fornecida ao Sabixão."

        # Passo 2: Varredura leve via API HTTP pública (Módulo DDGS do AETHER)
        try:
            dados_capturados = await self.varredor.pesquisar_no_perplexity(questao_final)
        except Exception as e:
            dados_capturados = f"[Falha no Varredor]: Conexão direta necessária. Motivo: {e}"

        # Passo 3: Força a reinicialização dos nós puxando do cofre do Streamlit antes do disparo
        self.orquestrador.gemini_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
        self.orquestrador.groq_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

        # Passo 4: O orquestrador assume e aplica o julgamento de IA (Gemini/Groq)
        print("[*] Consolidando informações recolhidas...")
        resposta_definitiva = self.orquestrador.executar_consenso_hidra(questao_final, dados_capturados)
        
        return resposta_definitiva

# Bloco de execução principal do sistema
if __name__ == "__main__":
    sistema = SabixaoSistemaUniversal()
