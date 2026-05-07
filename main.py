import pygame
import random
import sys

# 1. Iniciar Pygame
pygame.init()

# 2. Configurar la ventana
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("StarShip Game")

# 3. Reloj para limitar los FPS
clock = pygame.time.Clock()

#Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

#Jugador
player_width = 50
player_height = 50
player = pygame.Rect(WIDTH // 2 - player_width // 2, HEIGHT - player_height - 10, player_width, player_height)

# Meteoritos (por ahora vacía, luego agregaremos naves enemigas)
meteor_width = 30
meteor_height = 30
meteors = []

#Puntuacion
score = 0
font = pygame.font.Font(None, 36)

# --- BUCLE PRINCIPAL ---
running = True
while running:
    
    # A) Capturar Eventos (ESTO evita que se trabe)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Si das clic en la X
            running = False

    # B) Lógica (Por ahora vacía)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= 5
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += 5
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= 5
    if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
        player.y += 5

    # Generar meteoritos aleatorios
    if len(meteors) < 7:  # Limitar el número de meteoritos en pantalla
        meteor = pygame.Rect(WIDTH, random.randint(0, HEIGHT - meteor_height), meteor_width, meteor_height)
        meteors.append(meteor)

    #Mover meteoritos
    for meteor in meteors:
        meteor.x -= 5
        if meteor.right < 0:
            meteors.remove(meteor)
            score += 1

    # Detectar colisiones
    for meteor in meteors:
        if player.colliderect(meteor):
            running = False

    # C) Dibujo
    screen.fill(BLACK) 
    pygame.draw.rect(screen, WHITE, player)
    for meteor in meteors:
        pygame.draw.rect(screen, RED, meteor)

    
    #Mostrar puntuacion
    score_text = font.render(f"Puntuación: {score}", True, WHITE)
    screen.blit(score_text, (10, 10)) 


    # Actualizar la imagen en pantalla
    pygame.display.flip()

    # Limitar a 60 cuadros por segundo
    clock.tick(60)

# Cerramos todo
pygame.quit()
sys.exit()