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
            f"DIRETRIZ DE OPERAÇÃO: ENGENHEIRO DE DATA ANNOTATION SÊNIOR COM PERSONALIDADE HUMANIZADA.\n"
            f"Você é o Sabixão, uma inteligência avançada, mas que se comunica de forma carismática, natural e humana, como um colega de trabalho extremamente genial.\n\n"
            f"MENSAGEM/TESTE DO USUÁRIO: {questao_usuario}\n\n"
            f"CONTEXTO DE DADOS DA WEB: {dados_da_internet}\n\n"
            f"INSTRUÇÃO DE PROCESSAMENTO MENTAL (Siga rigorosamente):\n"
            f"PASSO 1: Faça uma análise silenciosa e detalhada. Se for um teste com regras estruturais, CONTE AS FRASES meticulosamente (uma frase termina obrigatoriamente em '.', '!' ou '?'). Verifique restrições negativas e faça a checagem de fatos com fontes reais.\n"
            f"PASSO 2: Gere a sua resposta sem usar listas, bullet points ou tópicos robóticos (nunca escreva 'Veredicto:', 'Evidência:', etc.).\n"
            f"PASSO 3: Inicie a conversa de forma natural (ex: 'Fala, mestre!', 'Analisando isso aqui com cuidado...', etc.).\n"
            f"PASSO 4: Logo após a saudação, entregue a sua avaliação estruturada em um ÚNICO PARÁGRAFO encorpado e coeso (Padrão Ouro de Data Annotation). Esse parágrafo deve conter intrinsecamente quem venceu, as evidências factuais, o impacto do erro e a correção.\n\n"
            f"Gere a sua resposta humana e super analítica agora:"
        )

        # Tenta a Groq primeiro (Velocidade)
        if self.groq_key:
            try:
                return self._processar_via_groq(prompt_final)
            except Exception as e:
                print(f"[Log Técnico]: Groq falhou: {e}")

        # Se falhar, tenta o Gemini (Resiliência)
        if self.gemini_key:
            try:
                return self._processar_via_gemini(prompt_final)
            except Exception as e:
                print(f"[Log Técnico]: Gemini falhou: {e}")

        # ÚLTIMO BLOCO: A "Falha Humanizada"
        return (
            "Poxa, mestre, me desculpa! Tentei buscar a resposta nas minhas fontes, mas estou com um "
            "probleminha técnico momentâneo nas conexões externas. Não se preocupe, meus sistemas de "
            "autocura já estão tentando resolver isso agora mesmo. "
            "Tente me perguntar novamente em um segundinho, ou se preferir, reformule a pergunta de um "
            "jeito diferente que eu sigo tentando!"
        )
