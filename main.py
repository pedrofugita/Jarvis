import threading
import pygame
import random
import math
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- CONFIGURAÇÕES INICIAIS ---
load_dotenv()
CHAVE_API = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=CHAVE_API)

# Configuração de Voz
maquina = pyttsx3.init()
try:
    vozes = maquina.getProperty('voices')
    # Tenta pegar uma voz em português se disponível, senão usa a padrão
    maquina.setProperty('voice', vozes[0].id) 
except:
    pass

# --- ESTADO GLOBAL ---
ESTADO = {
    "falando": False,
    "ouvindo": False,
    "texto_tela": "Inicializando sistemas..."
}

# --- PARTE 1: O CÉREBRO ---
def cerebro_jarvis():
    print("--- INICIANDO CÉREBRO ---")
    rec = sr.Recognizer()
    
    # Tentativa de modelo (Priorizando o Lite/Flash)
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-lite-preview-02-05')
    except:
        print("Modelo Lite falhou, tentando fallback...")
        model = genai.GenerativeModel('gemini-flash-latest')

    # Configuração de Microfone Travada (Modo Engenheiro)
    rec.dynamic_energy_threshold = False
    rec.energy_threshold = 400 
    rec.pause_threshold = 0.6

    prompt_sistema = "Você é o Jarvis. Responda em PT-BR. Máximo 1 frase curta."

    def falar(texto):
        print(f"DEBUG: Falando -> {texto}")
        ESTADO["falando"] = True
        ESTADO["texto_tela"] = texto
        try:
            maquina.say(texto)
            maquina.runAndWait()
        except Exception as e:
            print(f"Erro TTS: {e}")
        ESTADO["falando"] = False
        ESTADO["texto_tela"] = "Ouvindo..."

    falar("Interface visual limpa carregada.")

    while True:
        try:
            with sr.Microphone() as source:
                ESTADO["ouvindo"] = True
                print(f"--- AGUARDANDO COMANDO ---")
                
                audio = rec.listen(source, timeout=None, phrase_time_limit=5)
                
                ESTADO["ouvindo"] = False
                ESTADO["texto_tela"] = "Processando..."
                
                try:
                    texto_usuario = rec.recognize_google(audio, language="pt-BR")
                    print(f"Ouvi: '{texto_usuario}'")
                    
                    if "jarvis" in texto_usuario.lower():
                        response = model.generate_content(prompt_sistema + texto_usuario)
                        if response.text:
                            resposta_limpa = response.text.replace("*", "").strip()
                            falar(resposta_limpa)
                    else:
                        print("Ignorado (Não chamou Jarvis)")
                        ESTADO["texto_tela"] = "Aguardando..."
                        
                except sr.UnknownValueError:
                    print("Ruído...")
                    ESTADO["texto_tela"] = "Aguardando..."
                except Exception as e:
                    print(f"Erro API: {e}")
                    falar("Erro de conexão.")
                    
        except Exception as e:
            print(f"Erro Geral: {e}")
            ESTADO["ouvindo"] = False

# --- PARTE 2: O VISUAL MODERNO (PLEXUS LIMPO) ---
def interface_visual():
    pygame.init()
    LARGURA, ALTURA = 800, 600
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("J.A.R.V.I.S. Neural Net")
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont("Arial", 16)

    # Cores
    COR_FUNDO = (5, 8, 15)       # Azul Deep Space
    COR_IDLE = (0, 200, 255)     # Ciano (Padrão)
    COR_FALANDO = (255, 50, 50)  # Vermelho (Jarvis Falando)
    COR_OUVINDO = (0, 255, 100)  # Verde (Jarvis Ouvindo)

    # Configuração Plexus
    QTD_PARTICULAS = 80          # Aumentei um pouquinho já que tiramos o centro
    CONEXAO_DISTANCIA = 130      # Distância para criar linha

    class Particula:
        def __init__(self):
            self.x = random.randint(0, LARGURA)
            self.y = random.randint(0, ALTURA)
            self.vx = random.uniform(-1, 1) * 0.5
            self.vy = random.uniform(-1, 1) * 0.5
            self.tamanho = random.randint(2, 3)
        
        def mover(self, velocidade_mult):
            # Move baseado na velocidade atual
            self.x += self.vx * velocidade_mult
            self.y += self.vy * velocidade_mult

            # Rebater nas bordas
            if self.x <= 0 or self.x >= LARGURA: self.vx *= -1
            if self.y <= 0 or self.y >= ALTURA: self.vy *= -1

        def desenhar_ponto(self, surface, cor):
            pygame.draw.circle(surface, cor, (int(self.x), int(self.y)), self.tamanho)

    # Criar Enxame Inicial
    particulas = [Particula() for _ in range(QTD_PARTICULAS)]

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        tela.fill(COR_FUNDO)

        # 1. DEFINIR O ESTADO ATUAL (Cor e Velocidade)
        cor_alvo = COR_IDLE
        velocidade_mult = 1.0
        
        if ESTADO["falando"]:
            cor_alvo = COR_FALANDO
            velocidade_mult = 4.0 # Fica MUITO agitado quando fala
            
        elif ESTADO["ouvindo"]:
            cor_alvo = COR_OUVINDO
            velocidade_mult = 0.1 # Quase para no tempo (Matrix style) para ouvir
        
        else:
            # Estado Normal
            velocidade_mult = 0.8

        # 2. DESENHAR LINHAS E PONTOS
        for i in range(len(particulas)):
            p1 = particulas[i]
            p1.mover(velocidade_mult)
            p1.desenhar_ponto(tela, cor_alvo)

            for j in range(i + 1, len(particulas)):
                p2 = particulas[j]
                
                # Cálculo de Distância
                dist = math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
                
                if dist < CONEXAO_DISTANCIA:
                    # A linha fica mais transparente quanto mais longe
                    intensidade = int((1 - dist / CONEXAO_DISTANCIA) * 255)
                    if intensidade > 0:
                        # Truque para cor com Alpha no Pygame
                        # Criamos a cor baseada na cor_alvo mas mais escura
                        cor_linha = (
                            max(0, cor_alvo[0] - 80), 
                            max(0, cor_alvo[1] - 80), 
                            max(0, cor_alvo[2] - 80)
                        )
                        pygame.draw.line(tela, cor_linha, (p1.x, p1.y), (p2.x, p2.y), 1)

        # Texto de Status (Canto inferior)
        texto = fonte.render(ESTADO["texto_tela"], True, (100, 100, 100))
        tela.blit(texto, (20, ALTURA - 30))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    os._exit(0)

# --- EXECUÇÃO ---
if __name__ == "__main__":
    t = threading.Thread(target=cerebro_jarvis, daemon=True)
    t.start()
    interface_visual()