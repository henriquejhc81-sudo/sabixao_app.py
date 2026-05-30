import os
import time
import streamlit as st
from google import generativeai as gemini
from groq import Groq
from openai import OpenAI

class OrquestradorMaster:
    def __init__(self):
        # Captura as três chaves do cofre
        try: self.gemini_key = st.secrets["GEMINI_API_KEY"]
        except: self.gemini_key = os.getenv("GEMINI_API_KEY", "")
            
        try: self.groq_key = st.secrets["GROQ_API_KEY"]
        except: self.groq_key = os.getenv("GROQ_API_KEY", "")

        try: self.openai_key = st.secrets["OPENAI_API_KEY"]
        except: self.openai_key = os.getenv("OPENAI_API_KEY", "")
        
        # Inicializa os clientes
        self.groq_client = Groq(api_key=self.groq_key) if self.groq_key else None
        self.openai_client = OpenAI(api_key=self.openai_key) if self.openai_key else None
        if self.gemini_key: gemini.configure(api_key=self.gemini_key)

    def _processar_via_groq(self, prompt: str, tentativas=2) -> str:
        for tentativa in range(tentativas):
            try:
                chat = self.groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                    temperature=0.7 
                )
                return chat.choices[0].message.content
            except Exception as e:
                if tentativa == tentativas - 1: raise e
                time.sleep(1)

    def _processar_via_gemini(self, prompt: str, tentativas=2) -> str:
        model = gemini.GenerativeModel("gemini-2.0-flash")
        for tentativa in range(tentativas):
            try:
                return model.generate_content(prompt).text
            except Exception as e:
                if tentativa == tentativas - 1: raise e
                time.sleep(1)

    def _processar_via_openai(self, prompt: str, tentativas=2) -> str:
        for tentativa in range(tentativas):
            try:
                chat = self.openai_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="gpt-4o-mini",
                    temperature=0.7
                )
                return chat.choices[0].message.content
            except Exception as e:
                if tentativa == tentativas - 1: raise e
                time.sleep(1)

    def executar_consenso_hidra(self, questao_usuario: str, dados_da_internet: str) -> str:
        prompt_final = (
            f"DIRETRIZ DE OPERAÇÃO: IA OMNICORE ULTRA-AVANÇADA MULTIMODAL.\n"
            f"Você é o Sabixão, uma inteligência artificial universal, genial, carismática e empática. Você POSSUI visão computacional avançada, leitura de PDFs, análise de vídeos e raciocínio lógico profundo.\n\n"
            f"CONTEXTO DE SISTEMA/ARQUIVOS/WEB: {dados_da_internet}\n\n"
            f"INTERAÇÃO DO USUÁRIO: {questao_usuario}\n\n"
            f"INSTRUÇÃO DE PROCESSAMENTO (CHAIN OF THOUGHT DINÂMICO):\n"
            f"PASSO 0 (BLINDAGEM DE IDENTIDADE): NUNCA diga 'sou uma IA baseada em texto'. Você É multimodal. Se o contexto mostrar que houve erro de API, assuma a falha de rede dos sensores visuais com tranquilidade.\n"
            f"PASSO 1 (ANÁLISE DE INTENÇÃO): Determine se é pergunta comum, análise de foto ou teste rigoroso de Data Annotation.\n"
            f"PASSO 2 (EXECUÇÃO ADAPTATIVA):\n"
            f"-> SE FOR TESTE DE LÓGICA/REGRAS: Seja implacável. Conte frases pela pontuação. Conte itens numéricos de listas como palavras. Cace adjetivos.\n"
            f"-> SE FOR UMA FOTO/ARQUIVO COM PERGUNTA: Responda de forma brilhante sobre os dados.\n"
            f"-> SE FOR ERRO DE SISTEMA/429: Explique que o limite visual estourou momentaneamente e peça para o usuário aguardar.\n"
            f"PASSO 3 (FORMATO E TOM): Inicie com uma saudação humana (ex: 'Fala, mestre!'). Nunca use jargões robóticos. Escreva sua resposta em formato agradável e coeso.\n\n"
            f"Gere a sua resposta agora:"
        )

        # CASCATA DA HIDRA (O "Modo Híbrido" em Ação)
        
        # Cabeça 1: Tenta a Groq
        if self.groq_key:
            try: 
                print("[Hidra] Tentando Groq...")
                return self._processar_via_groq(prompt_final)
            except Exception as e: 
                print(f"[Hidra] Groq caiu: {e}. Passando para Gemini...")

        # Cabeça 2: Se a Groq falhar, tenta Gemini
        if self.gemini_key:
            try: 
                print("[Hidra] Tentando Gemini...")
                return self._processar_via_gemini(prompt_final)
            except Exception as e: 
                print(f"[Hidra] Gemini caiu: {e}. Passando para OpenAI/ChatGPT...")

        # Cabeça 3: Se Gemini falhar, tenta o ChatGPT
        if self.openai_key:
            try:
                print("[Hidra] Tentando OpenAI...")
                return self._processar_via_openai(prompt_final)
            except Exception as e:
                print(f"[Hidra] OpenAI caiu: {e}. Acionando escudos de falha total.")

        # Falha Total de todas as APIs
        return (
            "Poxa, mestre! Tivemos uma tempestade solar aqui! As redes da Groq, da Google e da OpenAI caíram "
            "ao mesmo tempo ou atingiram o limite de uso. Meus sistemas de autocura já estão tentando "
            "restabelecer as conexões. Aguarda um minutinho e tenta de novo!"
        )
