import time
import random
import re
import requests
from bs4 import BeautifulSoup

try:
    from duckduckgo_search import DDGS
    MODULO_DDGS = True
except ImportError:
    MODULO_DDGS = False

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    MODULO_YT = True
except ImportError:
    MODULO_YT = False

class VarredorInvisivel:
    def __init__(self):
        print("[Módulo Varredor Omnicore] Ativado com Sucesso.")

    def extrair_texto_de_link(self, url: str) -> str:
        """
        Engenharia extraída do NEXUS v9.1: Lê conteúdos de sites e transcreve vídeos do YouTube.
        """
        try:
            # 1. Farejador e Transcritor de Vídeos do YouTube
            if "youtube.com" in url or "youtu.be" in url:
                video_id = None
                match = re.search(r"(?:v=|\/|youtu\.be\/)([0-9A-Za-z_-]{11})", url)
                if match and MODULO_YT:
                    video_id = match.group(1)
                    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en', 'pt-BR'])
                    texto_video = " ".join([t['text'] for t in transcript])
                    return f"\n[Dados de Vídeo do YouTube Coletados]: {texto_video[:8000]}"
            
            # 2. Raspador de Sites Padrão via Requisição Limpa HTTP (Bypass de Bloqueio)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=8)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Limpa lixo visual do HTML
            for script in soup(["script", "style"]): 
                script.extract()
                
            texto_site = soup.get_text(separator=' ', strip=True)
            return f"\n[Dados Extraídos do Link]: {texto_site[:8000]}"
        except Exception as e:
            return f"\n[Aviso Conexão]: Não foi possível extrair dados diretos do link. Motivo: {str(e)}"

    async def pesquisar_no_perplexity(self, questao: str) -> str:
        """
        Realiza varredura híbrida: se houver links na pergunta, extrai o conteúdo deles.
        Caso contrário, realiza a busca global segura via DuckDuckGo.
        """
        contexto_total = ""
        
        # Identifica se o usuário colou algum link na pergunta (Tecnologia NEXUS)
        links = re.findall(r'(https?://[^\s]+)', questao)
        for link in links:
            contexto_total += self.extrair_texto_de_link(link)
            
        # Executa a busca geral na internet usando requisição HTTP estável
        if MODULO_DDGS:
            try:
                time.sleep(random.uniform(0.3, 0.8))
                with DDGS() as ddgs:
                    resultados = [r for r in ddgs.text(questao, max_results=3)]
                    if resultados:
                        contexto_total += " " + " ".join([f"{res['title']}: {res['body']}" for res in resultados])
            except Exception:
                pass
                
        if contexto_total.strip():
            return f"[Dados Vivos Capturados]: {contexto_total[:12000]}"
        return "[Aviso Coleta]: Nenhuma referência externa localizada. Processando via base local."
