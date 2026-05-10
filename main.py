"""
StarShip Game - Juego de esquivar meteoritos
Archivo principal que ejecuta el juego
"""

import pygame
import sys

import settings
from entities import Player, Meteor
from simulation_logic import create_spawner


# ===== INICIALIZACIÓN =====
pygame.init()
pygame.mixer.init()
settings.init_fonts()

# Cargar audios
home_theme = pygame.mixer.Sound('assets/sounds/home_theme.wav')
battle_theme = pygame.mixer.Sound('assets/sounds/battle_theme.wav')

# Configurar pantalla
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption("StarShip Game")
clock = pygame.time.Clock()

# Cargar iconos de botones
pause_icon = pygame.image.load('assets/images/PauseButton.png')
play_icon = pygame.image.load('assets/images/PlayButton.png')
home_icon = pygame.image.load('assets/images/HomeButton.png')
reload_icon = pygame.image.load('assets/images/ReloadButton.png')

# Redimensionar iconos
pause_icon = pygame.transform.scale(pause_icon, (settings.BUTTON_ICON_SIZE, settings.BUTTON_ICON_SIZE))
play_icon = pygame.transform.scale(play_icon, (settings.BUTTON_ICON_SIZE, settings.BUTTON_ICON_SIZE))
home_icon = pygame.transform.scale(home_icon, (settings.BUTTON_ICON_SIZE, settings.BUTTON_ICON_SIZE))
reload_icon = pygame.transform.scale(reload_icon, (settings.BUTTON_ICON_SIZE, settings.BUTTON_ICON_SIZE))

# Cargar imágenes del juego
starship_img = pygame.image.load('assets/images/starship.png')
starship_img = pygame.transform.scale(starship_img, (settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT))

# Cargar imágenes de meteoritos
asteroid_images = [
    pygame.image.load('assets/images/meteo_grey.png'),
    pygame.image.load('assets/images/meteo_brown.png')
]
asteroid_images = [pygame.transform.scale(img, (30, 30)) for img in asteroid_images]

# Posiciones de los botones
button_positions = {
    'pause': pygame.Rect(settings.WIDTH - 110, 10, settings.BUTTON_ICON_SIZE, settings.BUTTON_ICON_SIZE),
    'play': pygame.Rect(settings.WIDTH - 80, 10, settings.BUTTON_ICON_SIZE, settings.BUTTON_ICON_SIZE),
    'home': pygame.Rect(settings.WIDTH - 50, 10, settings.BUTTON_ICON_SIZE, settings.BUTTON_ICON_SIZE),
    'reload': pygame.Rect(settings.WIDTH - 20, 10, settings.BUTTON_ICON_SIZE, settings.BUTTON_ICON_SIZE)
}


# ===== FUNCIONES DE INTERFAZ =====
def draw_menu():
    """Dibuja el menú principal"""
    screen.fill(settings.BLACK)
    
    title = settings.FONT_TITLE.render("STARSHIP GAME", True, settings.WHITE)
    title_rect = title.get_rect(center=(settings.WIDTH // 2, 100))
    screen.blit(title, title_rect)
    
    new_game_text = settings.FONT_MENU.render("1. New Game", True, settings.WHITE)
    multiplayer_text = settings.FONT_MENU.render("2. Multiplayer", True, settings.WHITE)
    exit_text = settings.FONT_MENU.render("3. Exit", True, settings.WHITE)
    
    new_game_rect = new_game_text.get_rect(center=(settings.WIDTH // 2, 250))
    multiplayer_rect = multiplayer_text.get_rect(center=(settings.WIDTH // 2, 350))
    exit_rect = exit_text.get_rect(center=(settings.WIDTH // 2, 450))
    
    screen.blit(new_game_text, new_game_rect)
    screen.blit(multiplayer_text, multiplayer_rect)
    screen.blit(exit_text, exit_rect)
    
    pygame.display.flip()


def draw_game_over(score):
    """Dibuja la pantalla de game over"""
    screen.fill(settings.BLACK)
    
    game_over_text = settings.FONT_TITLE.render("GAME OVER", True, settings.RED)
    final_score_text = settings.FONT_MENU.render(f"Puntuación: {score}", True, settings.WHITE)
    back_text = settings.FONT_REGULAR.render("Presiona cualquier tecla para volver al menú", True, settings.WHITE)
    
    screen.blit(game_over_text, game_over_text.get_rect(center=(settings.WIDTH // 2, 200)))
    screen.blit(final_score_text, final_score_text.get_rect(center=(settings.WIDTH // 2, 350)))
    screen.blit(back_text, back_text.get_rect(center=(settings.WIDTH // 2, 450)))
    
    pygame.display.flip()


def handle_button_clicks(mouse_pos, is_paused, battle_theme):
    """Maneja los clics de los botones"""
    action = None
    
    if button_positions['pause'].collidepoint(mouse_pos):
        is_paused = True
        battle_theme.set_volume(0.3)
    elif button_positions['play'].collidepoint(mouse_pos):
        is_paused = False
        battle_theme.set_volume(1.0)
    elif button_positions['home'].collidepoint(mouse_pos):
        action = 'home'
    elif button_positions['reload'].collidepoint(mouse_pos):
        action = 'reload'
    
    return action, is_paused


# ===== FUNCIÓN JUEGO SINGLE PLAYER =====
def play_single_player():
    """Juego de un jugador"""
    home_theme.stop()
    battle_theme.play(-1)
    
    player = Player(settings.WIDTH // 4 - settings.PLAYER_WIDTH // 2, settings.HEIGHT // 2 - settings.PLAYER_HEIGHT // 2, starship_img)
    meteors = []
    score = 0
    game_running = True
    is_paused = False
    
    # Crear spawner de meteoritos con distribución exponencial
    spawner = create_spawner(lambda_param=0.15)
    
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    battle_theme.stop()
                    home_theme.play(-1)
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                action, is_paused = handle_button_clicks(event.pos, is_paused, battle_theme)
                if action == 'home':
                    battle_theme.stop()
                    home_theme.play(-1)
                    return True
                elif action == 'reload':
                    battle_theme.stop()
                    return play_single_player()
        
        if not is_paused:
            # Movimiento del jugador
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.move_left()
            if keys[pygame.K_RIGHT]:
                player.move_right(settings.WIDTH)
            if keys[pygame.K_UP]:
                player.move_up()
            if keys[pygame.K_DOWN]:
                player.move_down(settings.HEIGHT)
            
            # Generar meteoritos usando la lógica de simulación
            if len(meteors) < settings.MAX_METEORS_SINGLE_PLAYER:
                if spawner.should_spawn():
                    meteor_img = asteroid_images[0] if score % 2 == 0 else asteroid_images[1]
                    new_meteor = spawner.spawn_meteor(meteor_img)
                    meteors.append(new_meteor)
            
            # Mover y actualizar meteoritos
            for meteor in meteors[:]:
                meteor.move()
                if meteor.is_off_screen(settings.WIDTH):
                    meteors.remove(meteor)
                    score += 1
            
            # Detectar colisiones
            for meteor in meteors:
                if player.collides_with(meteor.rect):
                    game_running = False
        
        # Dibujar
        screen.fill(settings.BLACK)
        player.draw(screen)
        for meteor in meteors:
            meteor.draw(screen)
        
        score_text = settings.FONT_SMALL.render(f"Puntuación: {score}", True, settings.WHITE)
        screen.blit(score_text, (10, 10))
        
        screen.blit(pause_icon, button_positions['pause'])
        screen.blit(play_icon, button_positions['play'])
        screen.blit(home_icon, button_positions['home'])
        screen.blit(reload_icon, button_positions['reload'])
        
        if is_paused:
            pause_text = settings.FONT_TITLE.render("PAUSADO", True, settings.YELLOW)
            screen.blit(pause_text, pause_text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2)))
        
        esc_text = settings.FONT_SMALL.render("Presiona ESC para volver al menú", True, settings.GRAY)
        screen.blit(esc_text, (10, settings.HEIGHT - 40))
        
        pygame.display.flip()
        clock.tick(settings.FPS)
    
    # Game Over
    battle_theme.stop()
    draw_game_over(score)
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                waiting = False
    
    home_theme.play(-1)
    return True


# ===== FUNCIÓN JUEGO MULTIPLAYER =====
def play_multiplayer():
    """Juego de dos jugadores"""
    home_theme.stop()
    battle_theme.play(-1)
    
    player1 = Player(settings.WIDTH // 4 - settings.PLAYER_WIDTH // 2, settings.HEIGHT - settings.PLAYER_HEIGHT - 10, starship_img)
    player2 = Player(3 * settings.WIDTH // 4 - settings.PLAYER_WIDTH // 2, settings.HEIGHT - settings.PLAYER_HEIGHT - 10, starship_img)
    meteors = []
    score1 = 0
    score2 = 0
    game_running = True
    is_paused = False
    
    spawner = create_spawner(lambda_param=0.15)
    
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    battle_theme.stop()
                    home_theme.play(-1)
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                action, is_paused = handle_button_clicks(event.pos, is_paused, battle_theme)
                if action == 'home':
                    battle_theme.stop()
                    home_theme.play(-1)
                    return True
                elif action == 'reload':
                    battle_theme.stop()
                    return play_multiplayer()
        
        if not is_paused:
            # Movimiento del jugador 1 (flechas)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player1.move_left()
            if keys[pygame.K_RIGHT]:
                player1.move_right(settings.WIDTH)
            if keys[pygame.K_UP]:
                player1.move_up()
            if keys[pygame.K_DOWN]:
                player1.move_down(settings.HEIGHT)
            
            # Movimiento del jugador 2 (WASD)
            if keys[pygame.K_a]:
                player2.move_left()
            if keys[pygame.K_d]:
                player2.move_right(settings.WIDTH)
            if keys[pygame.K_w]:
                player2.move_up()
            if keys[pygame.K_s]:
                player2.move_down(settings.HEIGHT)
            
            # Generar meteoritos
            if len(meteors) < settings.MAX_METEORS_MULTIPLAYER:
                if spawner.should_spawn():
                    meteor_img = asteroid_images[0] if score1 % 2 == 0 else asteroid_images[1]
                    new_meteor = spawner.spawn_meteor(meteor_img)
                    meteors.append(new_meteor)
            
            # Mover meteoritos
            for meteor in meteors[:]:
                meteor.move()
                if meteor.is_off_screen(settings.WIDTH):
                    meteors.remove(meteor)
                    score1 += 1
                    score2 += 1
            
            # Detectar colisiones
            for meteor in meteors:
                if player1.collides_with(meteor.rect) or player2.collides_with(meteor.rect):
                    game_running = False
        
        # Dibujar
        screen.fill(settings.BLACK)
        player1.draw(screen)
        player2.draw(screen)
        for meteor in meteors:
            meteor.draw(screen)
        
        score1_text = settings.FONT_REGULAR.render(f"P1 (Flechas): {score1}", True, settings.WHITE)
        score2_text = settings.FONT_REGULAR.render(f"P2 (WASD): {score2}", True, settings.YELLOW)
        screen.blit(score1_text, (10, 10))
        screen.blit(score2_text, (10, 50))
        
        screen.blit(pause_icon, button_positions['pause'])
        screen.blit(play_icon, button_positions['play'])
        screen.blit(home_icon, button_positions['home'])
        screen.blit(reload_icon, button_positions['reload'])
        
        if is_paused:
            pause_text = settings.FONT_TITLE.render("PAUSADO", True, settings.YELLOW)
            screen.blit(pause_text, pause_text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2)))
        
        esc_text = settings.FONT_REGULAR.render("Presiona ESC para volver al menú", True, settings.GRAY)
        screen.blit(esc_text, (10, settings.HEIGHT - 40))
        
        pygame.display.flip()
        clock.tick(settings.FPS)
    
    battle_theme.stop()
    return True


# ===== BUCLE PRINCIPAL =====
def main():
    """Función principal que ejecuta el bucle del menú"""
    menu_running = True
    first_time_menu = True
    
    while menu_running:
        if first_time_menu:
            home_theme.play(-1)
            first_time_menu = False
        
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
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()