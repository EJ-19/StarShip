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

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)

# Dimensiones
player_width = 70
player_height = 70
meteor_width = 30
meteor_height = 30

# Fuentes
font = pygame.font.Font(None, 28)
small_font = pygame.font.Font(None, 24)
title_font = pygame.font.Font(None, 72)
menu_font = pygame.font.Font(None, 48)

# Cargar iconos de botones
pause_icon = pygame.image.load('assets/images/PauseButton.png')
play_icon = pygame.image.load('assets/images/PlayButton.png')
home_icon = pygame.image.load('assets/images/HomeButton.png')
reload_icon = pygame.image.load('assets/images/ReloadButton.png')

# Redimensionar iconos
icon_size = 25
pause_icon = pygame.transform.scale(pause_icon, (icon_size, icon_size))
play_icon = pygame.transform.scale(play_icon, (icon_size, icon_size))
home_icon = pygame.transform.scale(home_icon, (icon_size, icon_size))
reload_icon = pygame.transform.scale(reload_icon, (icon_size, icon_size))

# Cargar imágenes del juego
starship_img = pygame.image.load('assets/images/starship.png')
starship_img = pygame.transform.scale(starship_img, (player_width, player_height))

# Cargar imágenes de meteoritos (GIF - tomaremos la primera como estática)
asteroid_images = [
    pygame.image.load('assets/images/meteo_grey.png'),
    pygame.image.load('assets/images/meteo_brown.png')
]

# Redimensionar asteroides
asteroid_images = [pygame.transform.scale(img, (meteor_width, meteor_height)) for img in asteroid_images]

# Posiciones de los botones
button_positions = {
    'pause': pygame.Rect(WIDTH - 110, 10, icon_size, icon_size),
    'play': pygame.Rect(WIDTH - 80, 10, icon_size, icon_size),
    'home': pygame.Rect(WIDTH - 50, 10, icon_size, icon_size),
    'reload': pygame.Rect(WIDTH - 20, 10, icon_size, icon_size)
}

# --- FUNCIONES DEL MENÚ ---
def draw_menu():
    """Dibuja el menú principal"""
    screen.fill(BLACK)
    
    # Título
    title = title_font.render("STARSHIP GAME", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, 100))
    screen.blit(title, title_rect)
    
    # Opciones
    new_game_text = menu_font.render("1. New Game", True, WHITE)
    multiplayer_text = menu_font.render("2. Multiplayer", True, WHITE)
    exit_text = menu_font.render("3. Exit", True, WHITE)
    
    new_game_rect = new_game_text.get_rect(center=(WIDTH // 2, 250))
    multiplayer_rect = multiplayer_text.get_rect(center=(WIDTH // 2, 350))
    exit_rect = exit_text.get_rect(center=(WIDTH // 2, 450))
    
    screen.blit(new_game_text, new_game_rect)
    screen.blit(multiplayer_text, multiplayer_rect)
    screen.blit(exit_text, exit_rect)
    
    pygame.display.flip()

# --- FUNCIÓN JUEGO SINGLE PLAYER ---
def play_single_player():
    """Juego de un jugador"""
    # Inicializar variables
    player = pygame.Rect(WIDTH // 4 - player_width // 2, HEIGHT // 2 - player_height // 2, player_width, player_height)
    meteors = []
    score = 0
    game_running = True
    is_paused = False
    
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Botón Pausa
                if button_positions['pause'].collidepoint(mouse_pos):
                    is_paused = True
                # Botón Play
                elif button_positions['play'].collidepoint(mouse_pos):
                    is_paused = False
                # Botón Home
                elif button_positions['home'].collidepoint(mouse_pos):
                    return True
                # Botón Reiniciar
                elif button_positions['reload'].collidepoint(mouse_pos):
                    return play_single_player()
        
        if not is_paused:
            # Movimiento del jugador
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
            if len(meteors) < 7:
                # Variar el tamaño de los asteroides
                size_variation = random.uniform(0.7, 1.3)
                varied_width = int(meteor_width * size_variation)
                varied_height = int(meteor_height * size_variation)
                meteor_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT - varied_height), varied_width, varied_height)
                meteor_img = random.choice(asteroid_images)
                meteor_img = pygame.transform.scale(meteor_img, (varied_width, varied_height))
                rotation_speed = random.uniform(-5, 5)
                meteors.append((meteor_rect, meteor_img, 0, rotation_speed, varied_width, varied_height))
            
            # Mover meteoritos
            for i, (meteor, meteor_img, angle, rotation_speed, varied_width, varied_height) in enumerate(meteors):
                # La velocidad horizontal depende de la velocidad de rotación
                velocity_x = -5 * (0.5 + abs(rotation_speed) / 10)
                meteor.x += velocity_x
                angle += rotation_speed
                meteors[i] = (meteor, meteor_img, angle, rotation_speed, varied_width, varied_height)
                if meteor.right < 0:
                    meteors.pop(i)
                    score += 1
            
            # Detectar colisiones
            for meteor, meteor_img, angle, rotation_speed, varied_width, varied_height in meteors:
                if player.colliderect(meteor):
                    game_running = False
        
        # Dibujar
        screen.fill(BLACK)
        screen.blit(starship_img, player)
        for meteor, meteor_img, angle, rotation_speed, varied_width, varied_height in meteors:
            rotated_img = pygame.transform.rotate(meteor_img, angle)
            rotated_rect = rotated_img.get_rect(center=meteor.center)
            screen.blit(rotated_img, rotated_rect)
        
        score_text = small_font.render(f"Puntuación: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Dibujar botones
        screen.blit(pause_icon, button_positions['pause'])
        screen.blit(play_icon, button_positions['play'])
        screen.blit(home_icon, button_positions['home'])
        screen.blit(reload_icon, button_positions['reload'])
        
        # Mostrar indicador de pausa
        if is_paused:
            pause_text = title_font.render("PAUSADO", True, YELLOW)
            screen.blit(pause_text, pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        
        esc_text = small_font.render("Presiona ESC para volver al menú", True, GRAY)
        screen.blit(esc_text, (10, HEIGHT - 40))
        
        pygame.display.flip()
        clock.tick(60)
    
    # Mostrar Game Over
    game_over_text = title_font.render(f"GAME OVER", True, RED)
    final_score_text = menu_font.render(f"Puntuación: {score}", True, WHITE)
    back_text = font.render("Presiona cualquier tecla para volver al menú", True, WHITE)
    
    screen.fill(BLACK)
    screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH // 2, 200)))
    screen.blit(final_score_text, final_score_text.get_rect(center=(WIDTH // 2, 350)))
    screen.blit(back_text, back_text.get_rect(center=(WIDTH // 2, 450)))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                waiting = False
    
    return True

# --- FUNCIÓN JUEGO MULTIPLAYER ---
def play_multiplayer():
    """Juego de dos jugadores"""
    # Inicializar variables
    player1 = pygame.Rect(WIDTH // 4 - player_width // 2, HEIGHT - player_height - 10, player_width, player_height)
    player2 = pygame.Rect(3 * WIDTH // 4 - player_width // 2, HEIGHT - player_height - 10, player_width, player_height)
    meteors = []
    score1 = 0
    score2 = 0
    game_running = True
    is_paused = False
    
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Botón Pausa
                if button_positions['pause'].collidepoint(mouse_pos):
                    is_paused = True
                # Botón Play
                elif button_positions['play'].collidepoint(mouse_pos):
                    is_paused = False
                # Botón Home
                elif button_positions['home'].collidepoint(mouse_pos):
                    return True
                # Botón Reiniciar
                elif button_positions['reload'].collidepoint(mouse_pos):
                    return play_multiplayer()
        
        if not is_paused:
            # Movimiento del jugador 1 (flechas)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player1.left > 0:
                player1.x -= 5
            if keys[pygame.K_RIGHT] and player1.right < WIDTH:
                player1.x += 5
            if keys[pygame.K_UP] and player1.top > 0:
                player1.y -= 5
            if keys[pygame.K_DOWN] and player1.bottom < HEIGHT:
                player1.y += 5
            
            # Movimiento del jugador 2 (WASD)
            if keys[pygame.K_a] and player2.left > 0:
                player2.x -= 5
            if keys[pygame.K_d] and player2.right < WIDTH:
                player2.x += 5
            if keys[pygame.K_w] and player2.top > 0:
                player2.y -= 5
            if keys[pygame.K_s] and player2.bottom < HEIGHT:
                player2.y += 5
            
            # Generar meteoritos aleatorios
            if len(meteors) < 7:
                meteor = pygame.Rect(WIDTH, random.randint(0, HEIGHT - meteor_height), meteor_width, meteor_height)
                meteors.append(meteor)
            
            # Mover meteoritos
            for meteor in meteors:
                meteor.x -= 5
                if meteor.right < 0:
                    meteors.remove(meteor)
                    score1 += 1
                    score2 += 1
            
            # Detectar colisiones
            for meteor in meteors:
                if player1.colliderect(meteor):
                    game_running = False
                if player2.colliderect(meteor):
                    game_running = False
        
        # Dibujar
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, player1)
        pygame.draw.rect(screen, YELLOW, player2)
        for meteor in meteors:
            pygame.draw.rect(screen, RED, meteor)
        
        score1_text = font.render(f"P1 (Flechas): {score1}", True, WHITE)
        score2_text = font.render(f"P2 (WASD): {score2}", True, YELLOW)
        screen.blit(score1_text, (10, 10))
        screen.blit(score2_text, (10, 50))
        
        # Dibujar botones
        screen.blit(pause_icon, button_positions['pause'])
        screen.blit(play_icon, button_positions['play'])
        screen.blit(home_icon, button_positions['home'])
        screen.blit(reload_icon, button_positions['reload'])
        
        # Mostrar indicador de pausa
        if is_paused:
            pause_text = title_font.render("PAUSADO", True, YELLOW)
            screen.blit(pause_text, pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        
        esc_text = font.render("Presiona ESC para volver al menú", True, GRAY)
        screen.blit(esc_text, (10, HEIGHT - 40))
        
        pygame.display.flip()
        clock.tick(60)
    
    return True

# --- BUCLE PRINCIPAL DEL MENÚ ---
menu_running = True
while menu_running:
    draw_menu()
    
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                waiting_for_input = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    menu_running = play_single_player()
                    waiting_for_input = False
                elif event.key == pygame.K_2:
                    menu_running = play_multiplayer()
                    waiting_for_input = False
                elif event.key == pygame.K_3:
                    menu_running = False
                    waiting_for_input = False

# Cerramos todo
pygame.quit()
sys.exit()