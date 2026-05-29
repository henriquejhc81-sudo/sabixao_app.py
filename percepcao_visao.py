import os
from google import generativeai as genai
from PIL import Image
import PyPDF2
import pandas as pd

class PercepcaoVisao:
    def __init__(self):
        print("[Visão Quantum] Motor Multimodelo e Leitor de Documentos Ativado.")

    def extrair_texto_de_arquivo(self, caminho_arquivo: str) -> str:
        """
        Utiliza rotas dinâmicas para ler imagens, PDFs, planilhas (CSV) e textos.
        """
        if not os.path.exists(caminho_arquivo):
            return "[Visão Local]: Arquivo não encontrado na base."
            
        extensao = caminho_arquivo.lower().split('.')[-1]
        
        try:
            # 1. Rota para Documentos PDF
            if extensao == 'pdf':
                texto_extraido = ""
                with open(caminho_arquivo, 'rb') as f:
                    leitor_pdf = PyPDF2.PdfReader(f)
                    for pagina in leitor_pdf.pages:
                        texto = pagina.extract_text()
                        if texto:
                            texto_extraido += texto + "\n"
                return f"[Dados Extraídos do PDF]: \n{texto_extraido[:15000]}"
                
            # 2. Rota para Planilhas CSV
            elif extensao == 'csv':
                df = pd.read_csv(caminho_arquivo)
                texto_csv = df.to_string()
                return f"[Dados Extraídos da Planilha CSV]: \n{texto_csv[:15000]}"
                
            # 3. Rota para Arquivos de Texto Comum
            elif extensao == 'txt':
                with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                    texto_txt = f.read()
                return f"[Dados Extraídos do TXT]: \n{texto_txt[:15000]}"
                
            # 4. Rota Neural para Imagens (OCR via Gemini)
            elif extensao in ['png', 'jpg', 'jpeg', 'webp']:
                gemini_key = os.getenv("GEMINI_API_KEY")
                if not gemini_key:
                    return "[Visão Local]: Arquivo de imagem recebido. Aguardando processamento neural (Chave ausente)."
                    
                genai.configure(api_key=gemini_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                imagem_pil = Image.open(caminho_arquivo)
                
                response = model.generate_content([
                    "Atue como o transcritor de dados do Sabixão. Extraia com precisão cirúrgica "
                    "cada palavra, código, tabela ou fórmula contida nesta imagem/documento.", 
                    imagem_pil
                ])
                return f"[Texto Extraído dos Dados Visuais]: {response.text}"
                
            else:
                return f"[Aviso do Sistema]: O formato .{extensao} ainda não é suportado nativamente."
                
        except Exception as e:
            return f"[Falha no Processamento do Arquivo]: Erro na decodificação. Motivo: {str(e)}"
