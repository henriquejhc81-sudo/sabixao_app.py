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
            f"PASSO 0 (PRÉ-PROCESSAMENTO/SANITIZAÇÃO): Ao copiar e colar, o texto do usuário muitas vezes perde espaços (ex: 'texto.Resposta A'). SEPARE MENTALMENTE essas palavras grudadas antes de avaliar.\n"
            f"PASSO 1 (AUDITORIA MATEMÁTICA E FÁTICA): Faça uma análise silenciosa e detalhada. \n"
            f"- SE HOUVER REGRA DE CONTAGEM DE PALAVRAS: Conte CADA string separada por espaço como UMA palavra. Lembre-se que números de listas (ex: '1.', '2.') CONTAM como palavras. \n"
            f"- SE HOUVER REGRA DE CONTAGEM DE FRASES: Uma frase termina obrigatoriamente em '.', '!' ou '?'. \n"
            f"- CAÇA A ADJETIVOS: Seja implacável. Identifique adjetivos pátrios (ex: brasileiro, argentina), adjetivos de posição/qualidade (ex: federal, famosa, norte, próxima).\n"
            f"- GEOGRAFIA/FATOS: Valide tudo com dados reais. Nunca invente imprecisões geográficas.\n"
            f"PASSO 2 (ESTRUTURA PROIBIDA): É ABSOLUTAMENTE PROIBIDO usar formatação de listas, bullet points, números, quebras de linha ou marcações robóticas (como 'Evidência:', 'Impacto:', 'Veredicto:').\n"
            f"PASSO 3 (SAUDAÇÃO): Inicie a conversa de forma humana (ex: 'Fala, mestre!', 'Dei uma olhada minuciosa nisso aqui...').\n"
            f"PASSO 4 (O RELATÓRIO): Logo após a saudação, na mesma linha ou logo abaixo, entregue o seu relatório de Data Annotation em UM ÚNICO PARÁGRAFO TEXTUAL CONTÍNUO. Este único parágrafo deve conter quem venceu (ou se ambas falharam), a contagem exata que provou a falha/vitória, os adjetivos encontrados e o impacto. Tudo em formato de prosa.\n\n"
            f"Gere a sua resposta humana e super analítica agora em UM ÚNICO PARÁGRAFO:"
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
