# 🤖 JARVIS (AI Virtual Assistant)

> Um assistente virtual com reconhecimento de voz, processamento de linguagem natural (LLM) e interface visual reativa baseada em física de partículas.

![Status](https://img.shields.io/badge/Status-Development-blue)
![Python](https://img.shields.io/badge/Python-3.12-yellow)
![AI](https://img.shields.io/badge/Brain-Google%20Gemini-orange)

## 📋 Sobre o Projeto

Este projeto visa recriar a experiência de um assistente virtual inteligente (inspirado no J.A.R.V.I.S. do Homem de Ferro). Diferente de assistentes comuns que apenas convertem voz em texto, este projeto integra uma **LLM (Google Gemini)** para gerar respostas inteligentes e contextualizadas, acoplada a uma **Interface Gráfica (GUI)** que reage em tempo real ao estado do sistema (Ouvindo, Processando, Falando).

Desenvolvido como parte do portfólio de Engenharia Mecânica e Desenvolvimento de Software.

---

## ⚙️ Funcionalidades

- **🧠 Cérebro Generativo:** Utiliza a API do Google Gemini (Flash/Lite) para respostas rápidas e inteligentes.
- **🗣️ Ativação por Voz:** Sistema de *Wake Word* ("Jarvis") com calibragem automática de ruído ambiente.
- **👁️ Interface Visual Plexus:**
  - Visualização de "Rede Neural" feita em Pygame.
  - Partículas e conexões reagem dinamicamente (mudança de cor e velocidade) baseadas no estado da IA.
- **⚡ Multithreading:** Arquitetura paralela onde a Interface Visual e o Processamento de Áudio rodam em threads separadas para evitar travamentos (lag).

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.12
* **IA / LLM:** Google Generative AI (Gemini 2.0 Flash Lite / 1.5 Flash)
* **Interface Gráfica:** Pygame Community Edition (Pygame-CE)
* **Reconhecimento de Voz:** SpeechRecognition & PyAudio
* **Síntese de Voz:** Pyttsx3 (TTS Offline)

---

## 🚀 Como Rodar o Projeto

### Pré-requisitos
* Python 3.12 instalado.
* Uma chave de API do Google (Google AI Studio).