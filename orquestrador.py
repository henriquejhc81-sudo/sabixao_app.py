import os
import random
from google import generativeai as gemini
from groq import Groq

class OrquestradorMaster:
    def __init__(self):
        # Captura as chaves reais das variáveis de ambiente prontas para produção
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")
        
        # Inicializa o cliente Groq se a chave existir
        self.groq_client = Groq(api_key=self.groq_key) if self.groq_key else None
        
        # Inicializa o cliente Gemini se a chave existir
        if self.gemini_key:
            gemini.configure(api_key=self.gemini_key)

    def _processar_via_gemini(self, prompt: str) -> str:
        """Processamento profundo via modelo nativo gratuito do Gemini."""
        if not self.gemini_key:
            raise ValueError("Chave do Gemini não configurada.")
        
        # Usamos o modelo Flash para respostas rápidas ou Pro para alta complexidade
        model = gemini.GenerativeModel("gemini-1.5-flash")
        resposta = model.generate_content(prompt)
        return resposta.text

    def _processar_via_groq(self, prompt: str) -> str:
        """Processamento ultraveloz na arquitetura LPU da Groq."""
        if not self.groq_client:
            raise ValueError("Chave da Groq não configurada.")
        
        # Usamos o Llama 3 gratuito de 70 bilhões de parâmetros hospedado na Groq
        chat_completion = self.groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192",
        )
        return chat_completion.choices[0].message.content

    def executar_consenso_hidra(self, questao_usuario: str, dados_da_internet: str) -> str:
        """
        Aplica o efeito Hidra. Tenta refinar a resposta usando inteligência de ponta.
        Se uma API falhar ou estiver sem créditos, a outra assume instantaneamente.
        """
        prompt_final = (
            f"Você é o Sabixão, analista master definitivo.\n"
            f"Analise o problema do usuário com base nos dados coletados na internet.\n\n"
            f"Problema do Usuário: {questao_usuario}\n"
            f"Dados Brutos Coletados: {dados_da_internet}\n\n"
            f"Instrução: Filtre erros, resuma os pontos críticos e responda de forma "
            f"extremamente inteligente, clara e idêntica a um humano experiente."
        )

        # Cabeça 1 da Hidra: Tenta a infraestrutura do Google
        try:
            print("[Hidra - Cabeça 1] Enviando para análise profunda do Gemini...")
            return self._processar_via_gemini(prompt_final)
            
        except Exception as erro_gemini:
            print(f"[-] Cabeça 1 (Gemini) falhou: {erro_gemini}")
            print("[Hidra - Cabeça 2] Ativando LPU Groq / Llama 3 imediatamente...")
            
            # Cabeça 2 da Hidra: Contingência imediata via Groq
            try:
                return self._processar_via_groq(prompt_final)
            except Exception as erro_groq:
                # Se ambas falharem, o sistema usa uma heurística local inteligente
                return (
                    f"[Modo Sobrevivência] Ambas as APIs principais falharam por limite de cota.\n"
                    f"Resultado local baseado nos dados capturados da internet: {dados_da_internet[:300]}..."
                )
