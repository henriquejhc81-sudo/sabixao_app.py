import asyncio
import random
from playwright.async_api import async_playwright

class VarredorInvisivel:
    def __init__(self):
        # Lista de User-Agents comuns de navegadores reais (Windows e Mac) para mascarar o Sabixão
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"
        ]

    async def _simular_movimento_humano(self, page):
        """Move o mouse e rola a tela de forma aleatória para enganar sistemas anti-bot."""
        try:
            # Simula pequenas rolagens de página como um humano lendo
            for _ in range(random.randint(1, 3)):
                await page.mouse.wheel(0, random.randint(100, 300))
                await asyncio.sleep(random.uniform(0.5, 1.5))
        except Exception:
            pass

    async def pesquisar_no_perplexity(self, questao: str) -> str:
        """
        Acessa o Perplexity AI simulando um humano na busca em tempo real.
        """
        print(f"[Invisível] Iniciando busca humana no Perplexity para: '{questao[:20]}...'")
        
        async with async_playwright() as p:
            # Inicializa o navegador em modo 'headless' (oculto) com flags anti-detecção
            browser = await p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled", "--no-sandbox", "--disable-setuid-sandbox"]
            )

            
            # Define o contexto simulando uma tela residencial padrão
            context = await browser.new_context(
                user_agent=random.choice(self.user_agents),
                viewport={"width": 1920, "height": 1080},
                locale="pt-BR"
            )
            
            page = await context.new_page()
            
            try:
                # Altera propriedades de JavaScript que revelam automação
                await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                # Acessa a URL pública de busca direta do Perplexity
                url_busca = f"https://perplexity.ai{questao.replace(' ', '+')}"
                await page.goto(url_busca, wait_until="domcontentloaded", timeout=30000)
                
                # Aguarda o carregamento simulando tempo de leitura
                await asyncio.sleep(random.uniform(4.0, 7.0))
                await self._simular_movimento_humano(page)
                
                # Extrai o bloco de texto onde o Perplexity gera a resposta limpa
                # (O seletor captura o container principal de resposta)
                elemento_resposta = await page.query_selector("div.prose")
                
                if elemento_resposta:
                    texto_resposta = await elemento_resposta.inner_text()
                    await browser.close()
                    return texto_resposta
                else:
                    await browser.close()
                    return "[Aviso] Estrutura da página mudou ou fomos desafiados por um Captcha. Ativando redundância."
                    
            except Exception as e:
                await browser.close()
                return f"[Erro na Varredura]: {str(e)}. A Hidra vai redirecionar a tarefa."

# Bloco de teste assíncrono isolado
if __name__ == "__main__":
    varredor = VarredorInvisivel()
    pergunta_teste = "Qual o evento científico mais importante anunciado esta semana?"
    
    # Roda o teste localmente se necessário
    resposta_coletada = asyncio.run(varredor.pesquisar_no_perplexity(pergunta_teste))
    print("\n[+] Captura Oculta Concluída com Sucesso:")
    print(resposta_coletada)
