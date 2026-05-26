import os
from google import generativeai as genai
from PIL import Image

class PercepcaoVisao:
    def __init__(self):
        print("[Visão Quantum] Motor Multimodelo Ativado.")

    def extrair_texto_de_arquivo(self, caminho_imagem: str) -> str:
        """
        Utiliza visão computacional de ponta para ler prints, fotos de câmera e arquivos.
        """
        gemini_key = os.getenv("GEMINI_API_KEY")
        if not gemini_key or not os.path.exists(caminho_imagem):
            return "[Visão Local]: Arquivo recebido. Aguardando processamento neural."
            
        try:
            # Configura e envia a imagem diretamente para a transcrição visual do Gemini
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            imagem_pil = Image.open(caminho_imagem)
            
            response = model.generate_content([
                "Atue como o transcritor de dados do Sabixão. Extraia com precisão cirúrgica "
                "cada palavra, código ou fórmula contida nesta imagem/documento.", 
                imagem_pil
            ])
            return f"[Texto Extraído dos Dados Visuais]: {response.text}"
        except Exception as e:
            return f"[Falha Visão]: Erro ao decodificar imagem via OCR Neural. Motivo: {str(e)}"
