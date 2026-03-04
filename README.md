Juego de motos de luz estilo TRON para dos jugadores, desarrollado con el Arcade Machine SDK. Parte del proyecto integrador de la materia Taller de Objetos y Abstracción de Datos.

🎮 Características
Dos modos de juego: Clásico y Arcade (con obstáculos y estela desvaneciente)

Controles configurables para ambos jugadores

Música dinámica: aleatoria en menú, dos canciones en partida

Efectos de sonido (inicio, colisión, botones, game over)

Interfaz retro con sprites y efectos de neón

📋 Requisitos
Python 3.11 o superior

Pygame 2.6.0 o superior

Arcade Machine SDK

🚀 Instalación rápida
Clona el repositorio:

bash
git clone https://github.com/tu-usuario/tron-light-cycles.git
cd tron-light-cycles
Instala dependencias:

bash
pip install -r requirements.txt
Ejecuta el juego:

bash
python game.py
También puede ejecutarse dentro de la máquina arcade principal.

🎯 Cómo jugar
Jugador 1: W A S D

Jugador 2: ⬆️ ⬇️ ⬅️ ➡️

Pausa: P

Modo debug: F3

El objetivo es sobrevivir más que el oponente, evitando chocar con paredes, tu propia estela, la del rival y (en modo arcade) los obstáculos.

📁 Estructura
text
tron_game/
├── assets/          # Imágenes, sonidos, fuentes
├── states/           # Estados del juego (menú, partida, etc.)
├── game.py           # Punto de entrada
├── player.py         # Lógica del jugador
├── settings.py       # Constantes y configuraciones
└── ...
👥 Créditos
Grupo 4

Victor Alcala

Ricardo Trevison

📌 Nota
Este juego cumple estrictamente con la interfaz del Arcade Machine SDK, permitiendo su integración directa en la máquina arcade unificada.

<div align="center"> ¡Que gane el mejor jinete de luz! ⚡ </div>
