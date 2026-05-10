"""
Configuración general del juego StarShip Game
"""

import pygame

# ===== CONFIGURACIÓN DE VENTANA =====
WIDTH = 800
HEIGHT = 600
FPS = 60

# ===== COLORES =====
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)

# ===== DIMENSIONES DEL JUGADOR =====
PLAYER_WIDTH = 70
PLAYER_HEIGHT = 70

# ===== DIMENSIONES DE METEORITOS BASE =====
METEOR_WIDTH = 30
METEOR_HEIGHT = 30

# ===== CLASES DE METEORITOS =====
# Clase 1: Pequeños y Veloces (30%)
METEOR_CLASS_1 = {
    'name': 'Pequeños y Veloces',
    'probability': 0.30,
    'size_multiplier': 0.7,
    'velocity_multiplier': 1.5,
    'rotation_speed_range': (-8, 8),
    'color': (150, 150, 150)  # Gris claro
}

# Clase 2: Normales (50%)
METEOR_CLASS_2 = {
    'name': 'Normales',
    'probability': 0.50,
    'size_multiplier': 1.0,
    'velocity_multiplier': 1.0,
    'rotation_speed_range': (-5, 5),
    'color': (100, 100, 100)  # Gris medio
}

# Clase 3: Grandes y Pesados (20%)
METEOR_CLASS_3 = {
    'name': 'Grandes y Pesados',
    'probability': 0.20,
    'size_multiplier': 1.5,
    'velocity_multiplier': 0.5,
    'rotation_speed_range': (-2, 2),
    'color': (70, 50, 40)  # Marrón oscuro
}

METEOR_CLASSES = [METEOR_CLASS_1, METEOR_CLASS_2, METEOR_CLASS_3]

# ===== VELOCIDADES Y PARÁMETROS DE JUEGO =====
PLAYER_SPEED = 5
MAX_METEORS_SINGLE_PLAYER = 7
MAX_METEORS_MULTIPLAYER = 7

# ===== TAMAÑO DE BOTONES =====
BUTTON_ICON_SIZE = 25

# ===== FUENTES =====
FONT_REGULAR = None
FONT_SMALL = None
FONT_TITLE = None
FONT_MENU = None

def init_fonts():
    """Inicializa las fuentes. Debe llamarse después de pygame.init()"""
    global FONT_REGULAR, FONT_SMALL, FONT_TITLE, FONT_MENU
    FONT_REGULAR = pygame.font.Font(None, 28)
    FONT_SMALL = pygame.font.Font(None, 24)
    FONT_TITLE = pygame.font.Font(None, 72)
    FONT_MENU = pygame.font.Font(None, 48)
