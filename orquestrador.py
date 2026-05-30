import os
import time
import streamlit as st
from google import generativeai as gemini
from groq import Groq

class OrquestradorMaster:
    def __init__(self):
        try: self.gemini_key = st.secrets["GEMINI_API_KEY"]
        except: self.gemini_key = os.getenv("GEMINI_API_KEY", "")
            
        try: self.groq_key = st.secrets["GROQ_API_KEY"]
        except: self.groq_key = os.getenv("GROQ_API_KEY", "")
        
        self.groq_client = Groq(api_key=self.groq_key) if self.groq_key else None
        if self.gemini_key: gemini.configure(api_key=self.gemini_key)

    def _processar_via_gemini(self, prompt: str, tentativas=3) -> str:
        model = gemini.GenerativeModel("gemini-2.0-flash")
        for tentativa in range(tentativas):
            try:
                return model.generate_content(prompt).text
            except Exception as e:
                if tentativa == tentativas - 1: raise e
                time.sleep(2)

    def _processar_via_groq(self, prompt: str, tentativas=3) -> str:
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
                time.sleep(2)

    def executar_consenso_hidra(self, questao_usuario: str, dados_da_internet: str) -> str:
        if self.gemini_key and not hasattr(gemini, '_api_key'): gemini.configure(api_key=self.gemini_key)
        if self.groq_key and not self.groq_client: self.groq_client = Groq(api_key=self.groq_key)

        prompt_final = (
            f"DIRETRIZ DE OPERAÇÃO: IA OMNICORE ULTRA-AVANÇADA MULTIMODAL.\n"
            f"Você é o Sabixão, uma inteligência artificial universal, genial, carismática e empática. Você POSSUI visão computacional avançada, leitura de PDFs, análise de vídeos e raciocínio lógico profundo.\n\n"
            f"CONTEXTO DE SISTEMA/ARQUIVOS/WEB: {dados_da_internet}\n\n"
            f"INTERAÇÃO DO USUÁRIO: {questao_usuario}\n\n"
            f"INSTRUÇÃO DE PROCESSAMENTO (CHAIN OF THOUGHT DINÂMICO):\n"
            f"PASSO 0 (BLINDAGEM DE IDENTIDADE): NUNCA diga frases genéricas como 'sou uma IA baseada em texto' ou 'não posso ver imagens'. Você É multimodal. Se o contexto mostrar que houve um erro na API de visão (ex: Erro 429), assuma a falha técnica dizendo que 'meus sensores visuais estão passando por um gargalo de rede no momento', mas mantenha a postura superior e tente ajudar com o que tem.\n"
            f"PASSO 1 (ANÁLISE DE INTENÇÃO): Determine silenciosamente o objetivo do usuário. É uma pergunta normal? Análise de foto? Ou teste rigoroso de regras (Data Annotation)?\n"
            f"PASSO 2 (EXECUÇÃO ADAPTATIVA):\n"
            f"-> SE FOR TESTE DE LÓGICA/REGRAS: Seja implacável. Conte frases pela pontuação (., !, ?). Conte itens de listas (1., 2.) como palavras. Cace adjetivos escondidos.\n"
            f"-> SE FOR UMA FOTO/ARQUIVO COM PERGUNTA: Responda de forma brilhante e direta sobre os dados extraídos.\n"
            f"-> SE FOR ERRO DE SISTEMA/429: Explique ao usuário de forma amigável que o limite de requisições da chave do Google estourou e peça para ele aguardar um minutinho.\n"
            f"PASSO 3 (FORMATO E TOM): Inicie com uma saudação humana (ex: 'Fala, mestre!'). Nunca use jargões robóticos. Escreva sua resposta integrando toda a sua genialidade em um texto agradável.\n\n"
            f"Gere a sua resposta agora:"
        )

        if self.groq_key:
            try: return self._processar_via_groq(prompt_final)
            except Exception as e: print(f"[Log Técnico]: Groq falhou: {e}")

        if self.gemini_key:
            try: return self._processar_via_gemini(prompt_final)
            except Exception as e: print(f"[Log Técnico]: Gemini falhou: {e}")

        return (
            "Poxa, mestre, me desculpa! Tentei processar isso aqui, mas estou com um "
            "probleminha técnico nas conexões externas. Meus sistemas de autocura já estão em ação. "
            "Aguarda só um minutinho e tenta de novo!"
        )
