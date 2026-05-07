import pygame
import random
import sys

pygame.init()


ancho, alto = 800, 600
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("StarShip Game")

ejecutando = True
while ejecutando:
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: 
            ejecutando = False

# Cerramos todo
pygame.quit()
sys.exit()