import os
import streamlit as st
from google import generativeai as gemini
from groq import Groq

class OrquestradorMaster:
    def __init__(self):
        # Captura segura priorizando a nuvem (Streamlit Cloud), com fallback para variáveis locais
        self.gemini_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
        self.groq_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
        
        self.groq_client = Groq(api_key=self.groq_key) if self.groq_key else None
        if self.gemini_key:
            gemini.configure(api_key=self.gemini_key)

    def _processar_via_gemini(self, prompt: str) -> str:
        if not self.gemini_key:
            raise ValueError("Chave Gemini ausente.")
        model = gemini.GenerativeModel("gemini-1.5-flash")
        resposta = model.generate_content(prompt)
        return resposta.text

    def _processar_via_groq(self, prompt: str) -> str:
        if not self.groq_client:
            raise ValueError("Chave Groq ausente.")
        chat_completion = self.groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.7 # Aumentado para 0.7 para gerar textos mais criativos e humanos
        )
        return chat_completion.choices.message.content

    def executar_consenso_hidra(self, questao_usuario: str, dados_da_internet: str) -> str:
        self.gemini_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
        self.groq_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
        
        if self.gemini_key: gemini.configure(api_key=self.gemini_key)
        if self.groq_key and not self.groq_client: self.groq_client = Groq(api_key=self.groq_key)

        # A MÁGICA ACONTECE AQUI: O PROMPT DE PERSONALIDADE ABSOLUTA E TRADUÇÃO C2
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

        # Cabeça Principal: Llama 3 via Groq (Raciocínio Humanizado Ultra Rápido)
        if self.groq_key:
            try:
                print("[Hidra] Disparando nó de Raciocínio Groq...")
                return self._processar_via_groq(prompt_final)
            except Exception as e:
                print(f"[-] Nó Groq falhou: {e}")

        # Cabeça Secundária: Gemini (Contingência e Leitura Profunda)
        if self.gemini_key:
            try:
                print("[Hidra] Acionando nó de Contingência Gemini...")
                return self._processar_via_gemini(prompt_final)
            except Exception as e:
                print(f"[-] Nó Gemini falhou: {e}")

        # Falha Crítica
        return (
            f"Poxa, mestre. Minhas conexões neurais externas estão em manutenção agora. "
            f"Mas eu consegui extrair essas anotações cruas da rede para você dar uma olhada:\n\n{dados_da_internet}"
        )
