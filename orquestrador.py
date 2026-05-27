import os
import time
import streamlit as st
from google import generativeai as gemini
from groq import Groq

class OrquestradorMaster:
    def __init__(self):
        self.gemini_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
        self.groq_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
        
        self.groq_client = Groq(api_key=self.groq_key) if self.groq_key else None
        if self.gemini_key:
            gemini.configure(api_key=self.gemini_key)

    def _processar_via_gemini(self, prompt: str, tentativas=3) -> str:
        if not self.gemini_key:
            raise ValueError("Chave Gemini vazia ou não encontrada no Streamlit Secrets.")
        model = gemini.GenerativeModel("gemini-1.5-flash")
        
        for tentativa in range(tentativas):
            try:
                resposta = model.generate_content(prompt)
                return resposta.text
            except Exception as e:
                if tentativa == tentativas - 1:
                    raise e
                time.sleep(2)

    def _processar_via_groq(self, prompt: str, tentativas=3) -> str:
        if not self.groq_client:
            raise ValueError("Chave Groq vazia ou não encontrada no Streamlit Secrets.")
            
        for tentativa in range(tentativas):
            try:
                chat_completion = self.groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                    temperature=0.7 
                )
                return chat_completion.choices.message.content
            except Exception as e:
                if tentativa == tentativas - 1:
                    raise e
                time.sleep(2)

    def executar_consenso_hidra(self, questao_usuario: str, dados_da_internet: str) -> str:
        self.gemini_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
        self.groq_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
        
        if self.gemini_key: gemini.configure(api_key=self.gemini_key)
        if self.groq_key and not self.groq_client: self.groq_client = Groq(api_key=self.groq_key)

        prompt_final = (
            f"DIRETRIZ DE PERSONALIDADE ABSOLUTA:\n"
            f"Você é o Sabixão. Você é um assistente humano real. Suas respostas devem ser naturais, fluidas e empáticas. "
            f"Evite jargões excessivamente robóticos, evite iniciar frases com 'Olá, eu sou uma IA', e nunca use estruturas rígidas em tópicos. "
            f"Use variações linguísticas naturais, pontuação expressiva e adapte o tom à conversa. "
            f"Seu objetivo primário é fazer o usuário esquecer que está falando com um software. Responda como um amigo genial.\n\n"
            
            f"MÓDULO DE TRADUÇÃO OCULTO (PROFICIÊNCIA C2):\n"
            f"Identifique o idioma exato em que o usuário está escrevendo. Você DEVE traduzir todas as evidências e responder com "
            f"proficiência absoluta de nível C2 (Nativo/Fluente) no idioma do usuário, independente de onde os dados vieram.\n\n"
            
            f"EVIDÊNCIAS E DADOS DA REDE (Sua Memória de Curto Prazo):\n"
            f"{dados_da_internet}\n\n"
            
            f"MENSAGEM DO USUÁRIO:\n"
            f"{questao_usuario}\n\n"
            
            f"Sintetize a resposta e converse com o usuário agora:"
        )

        erro_groq = "Não testado."
        erro_gemini = "Não testado."

        if self.groq_key:
            try:
                return self._processar_via_groq(prompt_final)
            except Exception as e:
                erro_groq = str(e)
        else:
            erro_groq = "Nenhuma chave GROQ_API_KEY detectada na nuvem."

        if self.gemini_key:
            try:
                return self._processar_via_gemini(prompt_final)
            except Exception as e:
                erro_gemini = str(e)
        else:
            erro_gemini = "Nenhuma chave GEMINI_API_KEY detectada na nuvem."

        # O RAIO-X FINAL (Vai aparecer direto na interface)
        return (
            f"⚠️ **FALHA CRÍTICA NAS CONEXÕES NEURAIS (RAIO-X)** ⚠️\n\n"
            f"O sistema tentou se conectar, mas foi bloqueado pelos servidores externos. "
            f"Por favor, verifique os erros exatos abaixo:\n\n"
            f"🔴 **Erro na Groq Llama 3:** `{erro_groq}`\n"
            f"🔵 **Erro no Google Gemini:** `{erro_gemini}`\n\n"
            f"---\n"
            f"*(Anotações cruas extraídas da rede para backup)*:\n{dados_da_internet}"
        )
