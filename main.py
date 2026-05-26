import asyncio
import os
# Comando forçado para instalar o navegador invisível caso ele não exista no servidor
try:
    import playwright
    # Executa a instalação silenciosa do Chromium direto no servidor Linux
    os.system("python -m playwright install chromium")
except Exception:
    pass

from orquestrador import OrquestradorMaster
from varredura_invisivel import VarredorInvisivel
from percepcao_visao import PercepcaoVisao

class SabixaoSistemaUniversal:
    def __init__(self):
        print("\n=========================================================")
        print("          SABIXÃO - SISTEMA UNIVERSAL ATIVADO            ")
        print("=========================================================\n")
        
        # Inicializa todos os módulos interdependentes do ecossistema
        self.orquestrador = OrquestradorMaster()
        self.varredor = VarredorInvisivel()
        self.visao = PercepcaoVisao()

    async def processar_requisicao(self, pergunta_texto: str = None, caminho_imagem: str = None):
        """
        Fluxo unificado: Lê arquivos/imagens se houver, varre a internet 
        de forma oculta e decide a resposta através do algoritmo Hidra.
        """
        questao_final = ""

        # Passo 1: Se houver imagem (print ou câmera), passa pelo módulo de visão
        if caminho_imagem:
            print(f"[*] Detectada entrada visual. Processando arquivo: {caminho_imagem}")
            texto_da_imagem = self.visao.extrair_texto_de_arquivo(caminho_imagem)
            questao_final = f"{texto_da_imagem} | Contexto adicional: {pergunta_texto or ''}"
        else:
            questao_final = pergunta_texto

        if not questao_final:
            print("[-] Nenhuma pergunta ou imagem foi fornecida ao sistema.")
            return

        # Passo 2: Varredura furtiva e invisível nos concorrentes de mercado
        try:
            dados_capturados = await self.varredor.pesquisar_no_perplexity(questao_final)
        except Exception as e:
            dados_capturados = f"[Falha no Varredor]: Conexão direta necessária. Motivo: {e}"

        # Passo 3: O orquestrador assume e aplica o julgamento de IA (Gemini/Groq)
        print("[*] Consolidando informações recolhidas...")
        resposta_definitiva = self.orquestrador.executar_consenso_hidra(questao_final, dados_capturados)
        
        print("\n================ ANÁLISE FINAL DO SABIXÃO ================")
        print(resposta_definitiva)
        print("==========================================================\n")
        return resposta_definitiva

# Bloco de execução principal do sistema
if __name__ == "__main__":
    # Instancia o Sabixão
    sistema = SabixaoSistemaUniversal()
    
    # Exemplo 1: Processando uma dúvida complexa de conhecimentos gerais via texto
    pergunta = "Explique a teoria das cordas de forma simples e compare com a visão da computação quântica."
    
    # Executa o loop assíncrono exigido pelo motor do Playwright
    asyncio.run(sistema.processar_requisicao(pergunta_texto=pergunta))
