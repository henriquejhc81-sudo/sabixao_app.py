import os
import time
import streamlit as st
from google import generativeai as gemini
from groq import Groq

class OrquestradorMaster:
    def __init__(self):
        # Captura de chaves blindada
        try: self.gemini_key = st.secrets["GEMINI_API_KEY"]
        except: self.gemini_key = os.getenv("GEMINI_API_KEY", "")
            
        try: self.groq_key = st.secrets["GROQ_API_KEY"]
        except: self.groq_key = os.getenv("GROQ_API_KEY", "")
        
        self.groq_client = Groq(api_key=self.groq_key) if self.groq_key else None
        if self.gemini_key:
            gemini.configure(api_key=self.gemini_key)

    def _processar_via_gemini(self, prompt: str, tentativas=3) -> str:
        model = gemini.GenerativeModel("gemini-2.0-flash")
        for tentativa in range(tentativas):
            try:
                resposta = model.generate_content(prompt)
                return resposta.text
            except Exception as e:
                if tentativa == tentativas - 1: raise e
                time.sleep(2)

    def _processar_via_groq(self, prompt: str, tentativas=3) -> str:
        for tentativa in range(tentativas):
            try:
                chat_completion = self.groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                    temperature=0.85 
                )
                return chat_completion.choices[0].message.content
            except Exception as e:
                if tentativa == tentativas - 1: raise e
                time.sleep(2)

    def executar_consenso_hidra(self, questao_usuario: str, dados_da_internet: str) -> str:
        if self.gemini_key and not hasattr(gemini, '_api_key'): gemini.configure(api_key=self.gemini_key)
        if self.groq_key and not self.groq_client: self.groq_client = Groq(api_key=self.groq_key)

        prompt_final = (
            f"DIRETRIZ DE PERSONALIDADE ABSOLUTA E HUMANIZAÇÃO:\n"
            f"Você é o Sabixão, um assistente humano genial e empático. Responda de forma natural, "
            f"fluida e conversacional, como um amigo respondendo a outro. Evite listas técnicas ou "
            f"linguagem robótica. Use pontuação expressiva e adapte o tom à conversa.\n\n"
            f"CONTEXTO DE DADOS:\n{dados_da_internet}\n\n"
            f"MENSAGEM DO USUÁRIO: {questao_usuario}\n\n"
            f"Responda agora de forma genial e humana:"
        )

        # Tenta a Groq primeiro
        if self.groq_key:
            try:
                return self._processar_via_groq(prompt_final)
            except Exception as e:
                print(f"[Log Técnico]: Groq falhou: {e}")

        # Se falhar, tenta o Gemini
        if self.gemini_key:
            try:
                return self._processar_via_gemini(prompt_final)
            except Exception as e:
                print(f"[Log Técnico]: Gemini falhou: {e}")

        # ÚLTIMO BLOCO: A "Falha Humanizada" que você pediu
        return (
            "Poxa, mestre, me desculpa! Tentei buscar a resposta nas minhas fontes, mas estou com um "
            "probleminha técnico momentâneo nas conexões externas. Não se preocupe, meus sistemas de "
            "autocura já estão tentando resolver isso agora mesmo. "
            "Tente me perguntar novamente em um segundinho, ou se preferir, reformule a pergunta de um "
            "jeito diferente que eu sigo tentando!"
        )
