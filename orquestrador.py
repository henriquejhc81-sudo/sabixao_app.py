import os
import time
import streamlit as st
from google import generativeai as gemini
from groq import Groq

class OrquestradorMaster:
    def __init__(self):
        # 1. Busca Chave Gemini (Prioriza Manual com Senha -> Streamlit Secrets -> Var Ambiente Local)
        if 'chave_gemini_manual' in st.session_state and st.session_state['chave_gemini_manual']:
            self.gemini_key = st.session_state['chave_gemini_manual']
        else:
            try: self.gemini_key = st.secrets["GEMINI_API_KEY"]
            except: self.gemini_key = os.getenv("GEMINI_API_KEY", "")

        # 2. Busca Chave Groq (Prioriza Manual com Senha -> Streamlit Secrets -> Var Ambiente Local)
        if 'chave_groq_manual' in st.session_state and st.session_state['chave_groq_manual']:
            self.groq_key = st.session_state['chave_groq_manual']
        else:
            try: self.groq_key = st.secrets["GROQ_API_KEY"]
            except: self.groq_key = os.getenv("GROQ_API_KEY", "")
        
        self.groq_client = Groq(api_key=self.groq_key) if self.groq_key else None
        if self.gemini_key:
            gemini.configure(api_key=self.gemini_key)

    def _processar_via_gemini(self, prompt: str, tentativas=3) -> str:
        # ATUALIZAÇÃO MESTRE: O modelo 1.5 flash foi aposentado, atualizamos para o 2.0
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
                # CORREÇÃO CRÍTICA: Extraindo o item [0] da lista retornada pela API
                return chat_completion.choices[0].message.content
            except Exception as e:
                if tentativa == tentativas - 1: raise e
                time.sleep(2)

    def executar_consenso_hidra(self, questao_usuario: str, dados_da_internet: str) -> str:
        # Re-checagem das chaves caso tenham sido digitadas na barra lateral oculta
        if 'chave_gemini_manual' in st.session_state and st.session_state['chave_gemini_manual']:
            self.gemini_key = st.session_state['chave_gemini_manual']
        if 'chave_groq_manual' in st.session_state and st.session_state['chave_groq_manual']:
            self.groq_key = st.session_state['chave_groq_manual']
            
        if self.gemini_key and not hasattr(gemini, '_api_key'): gemini.configure(api_key=self.gemini_key)
        if self.groq_key and not self.groq_client: self.groq_client = Groq(api_key=self.groq_key)

        prompt_final = (
            f"DIRETRIZ DE PERSONALIDADE ABSOLUTA E HUMANIZAÇÃO:\n"
            f"Você é o Sabixão, um assistente humano genial, empático e com acesso ao conhecimento do planeta Terra. "
            f"Suas respostas devem ser extremamente naturais e fluidas. Aja como um consultor brilhante conversando com um amigo. "
            f"PROIBIDO: Usar jargões robóticos (ex: 'Como um modelo de linguagem...'), iniciar frases com 'Olá, eu sou...', ou agir de forma mecânica.\n\n"
            
            f"PROTOCOLO DE JULGAMENTO MULTI-DADOS:\n"
            f"O sistema de varredura invisível acaba de retornar os seguintes dados extraídos da rede global (perspectivas diversas):\n"
            f"EVIDÊNCIAS:\n{dados_da_internet}\n\n"
            f"Sua missão é analisar essas evidências, cruzar com seu próprio conhecimento neural, remover qualquer erro ou contradição, e formular a resposta mais correta possível.\n\n"
            
            f"MÓDULO DE TRADUÇÃO OCULTO (PROFICIÊNCIA C2):\n"
            f"Você DEVE responder com proficiência absoluta de nível C2 (Nativo/Fluente) no mesmo idioma em que o usuário perguntou, independente do idioma das evidências coletadas.\n\n"
            
            f"MENSAGEM DO USUÁRIO:\n"
            f"{questao_usuario}\n\n"
            
            f"Respire fundo, julgue as informações e converse com o usuário agora de forma genial e humana:"
        )

        erro_groq = "Não testado."
        erro_gemini = "Não testado."

        if self.groq_key:
            try:
                return self._processar_via_groq(prompt_final)
            except Exception as e:
                erro_groq = str(e)
        else:
            erro_groq = "Chave GROQ_API_KEY ausente ou incorreta."

        if self.gemini_key:
            try:
                return self._processar_via_gemini(prompt_final)
            except Exception as e:
                erro_gemini = str(e)
        else:
            erro_gemini = "Chave GEMINI_API_KEY ausente ou incorreta."

        return (
            f"⚠️ **DIAGNÓSTICO DO MOTOR NEURAL** ⚠️\n\n"
            f"O Sabixão foi bloqueado pelos servidores externos:\n"
            f"🔴 **Status Groq:** `{erro_groq}`\n"
            f"🔵 **Status Gemini:** `{erro_gemini}`\n\n"
            f"**Solução:** Abra o 'Painel Neural Secreto' na barra lateral no canto superior esquerdo e cole suas chaves manualmente para forçar a conexão de forma segura."
        )
