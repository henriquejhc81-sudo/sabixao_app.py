import os
import random
import streamlit as st
from google import generativeai as gemini
from groq import Groq

class OrquestradorMaster:
    def __init__(self):
        # Transplante tecnológico: Captura as chaves diretamente do cofre oculto Secrets do Streamlit Cloud
        self.gemini_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
        self.groq_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
        
        # Inicializa o cliente Groq se a chave secreta estiver ativa
        self.groq_client = Groq(api_key=self.groq_key) if self.groq_key else None
        
        # Inicializa a infraestrutura Google se a chave secreta estiver ativa
        if self.gemini_key:
            gemini.configure(api_key=self.gemini_key)

    def _processar_via_gemini(self, prompt: str) -> str:
        """Processamento profundo via modelo nativo gratuito do Gemini."""
        if not self.gemini_key:
            raise ValueError("Chave do Gemini não localizada no cofre.")
        
        model = gemini.GenerativeModel("gemini-1.5-flash")
        resposta = model.generate_content(prompt)
        return resposta.text

    def _processar_via_groq(self, prompt: str) -> str:
        """Processamento ultraveloz na arquitetura LPU da Groq."""
        if not self.groq_client:
            raise ValueError("Chave da Groq não localizada no cofre.")
        
        chat_completion = self.groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192",
        )
        return chat_completion.choices.message.content

    def ejecutar_consenso_hidra(self, questao_usuario: str, dados_da_internet: str) -> str:
        """
        Aplica o efeito Hidra de Lerna.
        Se um nó falhar por limite de requisições, o outro assume imediatamente em segundo plano.
        """
        prompt_final = (
            f"Você é o Sabixão, analista master definitivo.\n"
            f"Analise o problema do usuário com base nos dados coletados na internet.\n\n"
            f"Problema do Usuário: {questao_usuario}\n"
            f"Dados Brutos Coletados: {dados_da_internet}\n\n"
            f"Instrução: Filtre erros, resuma os pontos críticos e responda de forma "
            f"extremamente inteligente, clara e idêntica a um humano experiente."
        )

        # Cabeça 1 da Hidra: Tenta puxar a inteligência do Google Gemini
        try:
            if not self.gemini_key:
                raise ValueError("Nó Gemini inativo.")
            print("[Hidra - Cabeça 1] Enviando para análise profunda do Gemini...")
            return self._processar_via_gemini(prompt_final)
            
        except Exception as erro_gemini:
            print(f"[-] Cabeça 1 (Gemini) indisponível: {erro_gemini}")
            print("[Hidra - Cabeça 2] Ativando LPU Groq / Llama 3 imediatamente...")
            
            # Cabeça 2 da Hidra: Contingência instantânea via Groq LPU
            try:
                if not self.groq_key:
                    raise ValueError("Nó Groq inativo.")
                return self._processar_via_groq(prompt_final)
            except Exception as erro_groq:
                # Retorno de segurança caso ocorra queda global em ambas as pontas externas
                return (
                    f"[Modo Sobrevivência] Ambas as APIs principais falharam temporariamente por limite de cota.\n"
                    f"Análise local baseada nos fragmentos coletados na internet:\n\n{dados_da_internet}"
                )
