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
        questao_final = ""

        # Passo 1: Processamento Visual Aprimorado
        if caminho_imagem:
            print(f"[*] Detectada entrada visual. Processando arquivo: {caminho_imagem}")
            texto_da_imagem = self.visao.extrair_texto_de_arquivo(caminho_imagem)
            # Interliga a foto com a caixa de texto de forma contextualizada
            questao_final = f"[DADOS DO ARQUIVO/IMAGEM]: {texto_da_imagem}\n\n[PERGUNTA/COMANDO DO USUÁRIO SOBRE O ARQUIVO]: {pergunta_texto or 'Descreva detalhadamente o que há neste arquivo.'}"
        else:
            questao_final = pergunta_texto

        if not questao_final:
            return "[Aviso] Nenhuma diretriz de dados ou questão foi fornecida ao Sabixão."

        # Passo 2: Varredura
        try:
            dados_capturados = await self.varredor.pesquisar_no_perplexity(questao_final)
        except Exception as e:
            dados_capturados = f"[Falha no Varredor]: Conexão direta necessária. Motivo: {e}"

        # Passo 3: Força chaves
        self.orquestrador.gemini_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
        self.orquestrador.groq_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

        # Passo 4: Orquestração Universal
        print("[*] Consolidando informações recolhidas...")
        resposta_definitiva = self.orquestrador.executar_consenso_hidra(questao_final, dados_capturados)
        
        return resposta_definitiva

if __name__ == "__main__":
    sistema = SabixaoSistemaUniversal()
