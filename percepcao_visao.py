import os
import time
from google import generativeai as genai
from PIL import Image
import PyPDF2
import pandas as pd

class PercepcaoVisao:
    def __init__(self):
        print("[Visão Quantum] Motor Multimodelo, Leitor de Documentos e Vídeos Ativado.")

    def extrair_texto_de_arquivo(self, caminho_arquivo: str) -> str:
        if not os.path.exists(caminho_arquivo):
            return "[Visão Local]: Arquivo não encontrado na base."
            
        extensao = caminho_arquivo.lower().split('.')[-1]
        
        try:
            if extensao == 'pdf':
                texto_extraido = ""
                with open(caminho_arquivo, 'rb') as f:
                    leitor_pdf = PyPDF2.PdfReader(f)
                    for pagina in leitor_pdf.pages:
                        texto = pagina.extract_text()
                        if texto: texto_extraido += texto + "\n"
                return f"[Dados Extraídos do PDF]: \n{texto_extraido[:15000]}"
                
            elif extensao == 'csv':
                df = pd.read_csv(caminho_arquivo)
                return f"[Dados Extraídos da Planilha CSV]: \n{df.to_string()[:15000]}"
                
            elif extensao == 'txt':
                with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                    return f"[Dados Extraídos do TXT]: \n{f.read()[:15000]}"
                
            elif extensao in ['png', 'jpg', 'jpeg', 'webp']:
                gemini_key = os.getenv("GEMINI_API_KEY")
                if not gemini_key: return "[Aviso]: Chave API ausente para visão."
                    
                genai.configure(api_key=gemini_key)
                # Forçando a versão mais estável para evitar o erro v1beta
                model = genai.GenerativeModel('models/gemini-1.5-flash')
                imagem_pil = Image.open(caminho_arquivo)
                
                response = model.generate_content([
                    "Descreva e extraia todos os textos, códigos ou elementos desta imagem com precisão máxima.", 
                    imagem_pil
                ])
                return response.text
                
            elif extensao in ['mp4', 'mov', 'avi', 'mkv']:
                gemini_key = os.getenv("GEMINI_API_KEY")
                if not gemini_key: return "[Aviso]: Chave API ausente para vídeo."
                
                genai.configure(api_key=gemini_key)
                arquivo_video = genai.upload_file(path=caminho_arquivo)
                
                while arquivo_video.state.name == "PROCESSING":
                    time.sleep(2)
                    arquivo_video = genai.get_file(arquivo_video.name)
                    
                if arquivo_video.state.name == "FAILED":
                    return "[Erro]: Falha no processamento do vídeo na nuvem."
                    
                model = genai.GenerativeModel('models/gemini-1.5-flash')
                response = model.generate_content([
                    "Assista a este vídeo com extrema atenção aos detalhes e transcreva/descreva as informações fundamentais.", 
                    arquivo_video
                ])
                genai.delete_file(arquivo_video.name) 
                return response.text
                
            else:
                return f"[Sistema]: O formato .{extensao} não é suportado nativamente."
                
        except Exception as e:
            return f"[Erro Técnico de Visão]: Ocorreu uma instabilidade na API (Possível falha de conexão ou modelo não suportado nesta região). Detalhe: {str(e)}"
