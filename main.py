import pygame
import random
import sys

# 1. Iniciar Pygame
pygame.init()

# 2. Configurar la ventana
ancho, alto = 800, 600
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("StarShip Game")

# 3. Reloj para limitar los FPS
reloj = pygame.time.Clock()

# --- BUCLE PRINCIPAL ---
ejecutando = True
while ejecutando:
    
    # A) Capturar Eventos (ESTO evita que se trabe)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: # Si das clic en la X
            ejecutando = False

    # B) Lógica (Por ahora vacía)

    # C) Dibujo
    #pantalla.fill((50, 100, 200)) # Un color azul cielo
    
    # Actualizar la imagen en pantalla
    pygame.display.flip()

    # Limitar a 60 cuadros por segundo
    reloj.tick(60)

# Cerramos todo
pygame.quit()
sys.exit()