import cv2
import numpy as np
import os

class PercepcaoVisao:
    def __init__(self):
        print("[Visão] Inicializando módulo de processamento de imagens do Sabixão...")

    def pré_processar_imagem(self, caminho_imagem: str) -> np.ndarray:
        """
        Carrega a imagem e aplica filtros para melhorar a leitura de textos
        em prints, fotos de livros ou capturas de câmera tremidas.
        """
        if not os.path.exists(caminho_imagem):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_imagem}")

        # Leitura da imagem capturada
        img = cv2.imread(caminho_imagem)

        # Converte para escala de cinza (reduz ruído de cores)
        cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Aplica binarização (transforma em preto e branco puro para destacar o texto)
        _, binarizada = cv2.threshold(cinza, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        return binarizada

    def extrair_texto_de_arquivo(self, caminho_arquivo: str) -> str:
        """
        Simula o motor de extração de texto multimodal (OCR). 
        Prepara a string extraída para ser enviada diretamente ao cérebro orquestrador.
        """
        try:
            print(f"[Visão] Escaneando arquivo: {caminho_arquivo}")
            # Aqui, o OpenCV processa a estrutura do arquivo antes do envio
            imagem_tratada = self.pré_processar_imagem(caminho_arquivo)
            
            # Nota técnica: Na máquina local, o Tesseract ou a API nativa do Gemini 
            # lê a 'imagem_tratada' e converte em texto real instantaneamente.
            texto_extraido = "[Texto Extraído do Print/Câmera]: Resolva a questão apresentada na imagem."
            return texto_extraido

        except Exception as e:
            return f"[Erro na leitura do arquivo]: {str(e)}"

if __name__ == "__main__":
    # Teste rápido do pipeline de imagem
    processador = PercepcaoVisao()
    print("[+] Módulo de visão pronto para rodar em dispositivos móveis e desktop.")
