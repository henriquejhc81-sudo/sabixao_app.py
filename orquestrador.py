import os
import streamlit as st
from google import generativeai as gemini
from groq import Groq

class OrquestradorMaster:
    def __init__(self):
        # Captura as chaves diretamente do cofre Secrets do Streamlit Cloud de forma nativa e limpa
        self.gemini_key = st.secrets.get("GEMINI_API_KEY", "")
        self.groq_key = st.secrets.get("GROQ_API_KEY", "")
        
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
            temperature=0.1
        )
        return chat_completion.choices.message.content

    def ejecutar_consenso_hidra(self, questao_usuario: str, dados_da_internet: str) -> str:
        # Garante a atualização das chaves antes do processamento neural
        self.gemini_key = st.secrets.get("GEMINI_API_KEY", "")
        self.groq_key = st.secrets.get("GROQ_API_KEY", "")
        if self.gemini_key: 
            gemini.configure(api_key=self.gemini_key)
        if self.groq_key and not self.groq_client: 
            self.groq_client = Groq(api_key=self.groq_key)

        prompt_final = (
            f"Você é o Sabixão, inteligência analítica master superior planetária.\n"
            f"Sua missão é resolver o problem do usuário analisando minuciosamente os dados coletados na internet.\n\n"
            f"Problema do Usuário: {questao_usuario}\n"
            f"Evidências e Dados Coletados da Internet:\n{dados_da_internet}\n\n"
            f"Instrução Técnica: Filtre contradições, remova alucinações e gere uma resposta "
            f"definitiva, extremamente inteligente, detalhada e em tom natural humano."
        )

        # Cabeça 1 da Hidra: Aciona a infraestrutura Groq de altíssima velocidade
        if self.groq_key:
            try:
                print("[Hidra] Disparando nó Groq...")
                return self._processar_via_groq(prompt_final)
            except Exception as e:
                print(f"[-] Nó Groq falhou: {e}")

        # Cabeça 2 da Hidra: Contingência instantânea via Google Gemini
        if self.gemini_key:
            try:
                print("[Hidra] Acionando nó Gemini...")
                return self._processar_via_gemini(prompt_final)
            except Exception as e:
                print(f"[-] Nó Gemini falhou: {e}")

        # Retorno caso as cotas de testes gratuitos estejam zeradas na nuvem
        return (
            f"[Análise de Contingência Local Ativada]\n\n"
            f"O sistema realizou a varredura mas as APIs externas estão em manutenção de cota.\n"
            f"Aqui estão os dados extraídos diretamente da rede para a sua análise:\n\n{dados_da_internet}"
        )
