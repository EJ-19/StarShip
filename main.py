"""
StarShip Game - Juego de esquivar meteoritos
Archivo principal que ejecuta el juego
"""

import pygame
import sys
import os

import settings
from entities import Player, Bullet
from simulation_logic import create_spawner


# ===== RUTAS =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")


def load_image(filename, size=None):
    """
    Carga una imagen de forma segura
    """
    path = os.path.join(IMAGES_DIR, filename)

    try:
        image = pygame.image.load(path).convert_alpha()

        if size:
            image = pygame.transform.scale(image, size)

        return image

    except Exception as e:
        print(f"Error cargando imagen: {path}")
        print(e)

        # Imagen de respaldo
        fallback = pygame.Surface((50, 50))
        fallback.fill((255, 0, 255))

        return fallback


def load_sound(filename):
    """
    Carga un sonido de forma segura
    """
    path = os.path.join(SOUNDS_DIR, filename)

    try:
        return pygame.mixer.Sound(path)

    except Exception as e:
        print(f"Error cargando sonido: {path}")
        print(e)
        return None


# ===== INICIALIZACIÓN =====
pygame.init()

# Inicializar audio sin romper el juego
audio_enabled = True

try:
    pygame.mixer.init()

except Exception as e:
    print("No se pudo iniciar el audio:")
    print(e)
    audio_enabled = False

settings.init_fonts()

# ===== AUDIO =====
home_theme = None
battle_theme = None
explosion_sound = None
gameover_theme = None

if audio_enabled:
    home_theme = load_sound("home_theme.wav")
    battle_theme = load_sound("battle_theme.wav")
    explosion_sound = load_sound("8bit_bomb_explosion.wav")
    gameover_theme = load_sound("final fight ost - ending.wav")

# ===== PANTALLA =====
screen = pygame.display.set_mode(
    (settings.WIDTH, settings.HEIGHT)
)

pygame.display.set_caption("StarShip Game")

clock = pygame.time.Clock()

# ===== ICONOS =====
pause_icon = load_image(
    "PauseButton.png",
    (settings.BUTTON_ICON_SIZE, settings.BUTTON_ICON_SIZE)
)

play_icon = load_image(
    "PlayButton.png",
    (settings.BUTTON_ICON_SIZE, settings.BUTTON_ICON_SIZE)
)

home_icon = load_image(
    "HomeButton.png",
    (settings.BUTTON_ICON_SIZE, settings.BUTTON_ICON_SIZE)
)

reload_icon = load_image(
    "ReloadButton.png",
    (settings.BUTTON_ICON_SIZE, settings.BUTTON_ICON_SIZE)
)

# ===== PLAYER =====
starship_img = load_image(
    "starship.png",
    (settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT)
)

# ===== METEOROS =====
asteroid_images = [
    load_image("meteo_grey.png", (30, 30)),
    load_image("meteo_brown.png", (30, 30))
]

# ===== BOTONES =====
button_positions = {
    'pause': pygame.Rect(
        settings.WIDTH - 140,
        10,
        settings.BUTTON_ICON_SIZE,
        settings.BUTTON_ICON_SIZE
    ),

    'play': pygame.Rect(
        settings.WIDTH - 100,
        10,
        settings.BUTTON_ICON_SIZE,
        settings.BUTTON_ICON_SIZE
    ),

    'home': pygame.Rect(
        settings.WIDTH - 60,
        10,
        settings.BUTTON_ICON_SIZE,
        settings.BUTTON_ICON_SIZE
    ),

    'reload': pygame.Rect(
        settings.WIDTH - 20,
        10,
        settings.BUTTON_ICON_SIZE,
        settings.BUTTON_ICON_SIZE
    )
}


# ===== FUNCIONES =====
def play_sound(sound, loops=0):
    if audio_enabled and sound:
        sound.play(loops)


def stop_sound(sound):
    if audio_enabled and sound:
        sound.stop()


def draw_menu_visual(selected=None):
    screen.fill(settings.BLACK)
    option_rects = {}

    # Dimensiones y posiciones adaptadas a la pantalla
    menu_width = int(settings.WIDTH * 0.4)
    menu_height = int(settings.HEIGHT * 0.12)
    sep = int(settings.HEIGHT * 0.06)
    start_y = settings.HEIGHT // 2 - menu_height - sep // 2

    # Colores
    rect_color = (40, 40, 60)
    hover_color = (80, 80, 160)
    border_color = (200, 200, 255)
    text_color = settings.WHITE
    hover_text_color = settings.YELLOW

    # Opciones
    options = [(1, "1 Player"), (2, "Multiplayer")]
    for idx, (opt, label) in enumerate(options):
        x = (settings.WIDTH - menu_width) // 2
        y = start_y + idx * (menu_height + sep)
        rect = pygame.Rect(x, y, menu_width, menu_height)
        is_hover = (selected == opt)
        # Fondo
        pygame.draw.rect(screen, hover_color if is_hover else rect_color, rect, border_radius=18)
        # Borde
        pygame.draw.rect(screen, border_color, rect, 4, border_radius=18)
        # Texto
        font = settings.FONT_MENU
        text = font.render(label, True, hover_text_color if is_hover else text_color)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
        option_rects[opt] = rect

    pygame.display.flip()
    return option_rects


def draw_game_over(score):
    screen.fill(settings.BLACK)

    title = settings.FONT_TITLE.render(
        "GAME OVER",
        True,
        settings.RED
    )

    score_text = settings.FONT_MENU.render(
        f"Puntuación: {score}",
        True,
        settings.WHITE
    )

    retry_text = settings.FONT_REGULAR.render(
        "Presione SPACE",
        True,
        settings.GRAY
    )

    screen.blit(
        title,
        title.get_rect(center=(settings.WIDTH // 2, 200))
    )

    screen.blit(
        score_text,
        score_text.get_rect(center=(settings.WIDTH // 2, 320))
    )

    screen.blit(
        retry_text,
        retry_text.get_rect(center=(settings.WIDTH // 2, 600))
    )

    pygame.display.flip()


def handle_buttons(mouse_pos, paused):
    action = None

    if button_positions['pause'].collidepoint(mouse_pos):
        paused = True

    elif button_positions['play'].collidepoint(mouse_pos):
        paused = False

    elif button_positions['home'].collidepoint(mouse_pos):
        action = "home"

    elif button_positions['reload'].collidepoint(mouse_pos):
        action = "reload"

    return action, paused


# ===== SINGLE PLAYER =====
def play_single_player():

    stop_sound(home_theme)
    play_sound(battle_theme, -1)

    player = Player(
        settings.WIDTH // 4,
        settings.HEIGHT // 2,
        starship_img
    )

    meteors = []
    bullets = []

    score = 0

    paused = False

    spawner = create_spawner(lambda_param=0.15)

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    stop_sound(battle_theme)
                    play_sound(home_theme, -1)

                    return True

                elif event.key == pygame.K_SPACE:

                    bullets.append(Bullet(player.rect.right, player.rect.centery))

            if event.type == pygame.MOUSEBUTTONDOWN:

                action, paused = handle_buttons(
                    event.pos,
                    paused
                )

                if action == "home":

                    stop_sound(battle_theme)
                    play_sound(home_theme, -1)

                    return True

                elif action == "reload":

                    stop_sound(battle_theme)

                    return play_single_player()

        if not paused:

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                player.move_left()

            if keys[pygame.K_RIGHT]:
                player.move_right(settings.WIDTH)

            if keys[pygame.K_UP]:
                player.move_up()

            if keys[pygame.K_DOWN]:
                player.move_down(settings.HEIGHT)

            # Spawn meteoros
            if len(meteors) < settings.MAX_METEORS_SINGLE_PLAYER:

                if spawner.should_spawn():

                    meteor_img = asteroid_images[
                        score % len(asteroid_images)
                    ]

                    meteor = spawner.spawn_meteor(meteor_img)

                    meteors.append(meteor)

            # Actualizar balas
            for bullet in bullets[:]:
                bullet.move()
                if bullet.is_off_screen(settings.WIDTH):
                    bullets.remove(bullet)

            # Colisiones balas con meteoros
            for bullet in bullets[:]:
                for meteor in meteors[:]:
                    if bullet.rect.colliderect(meteor.rect):
                        if bullet in bullets:
                            bullets.remove(bullet)
                        if meteor in meteors:
                            meteors.remove(meteor)
                            score += 5  # Bonus por destruir meteoros
                            # Sonido de explosión
                            play_sound(explosion_sound)
                        break

            # Actualizar meteoros
            for meteor in meteors[:]:

                meteor.move()

                if meteor.is_off_screen(settings.WIDTH):

                    meteors.remove(meteor)
                    score += 1

            # Colisiones
            for meteor in meteors:

                if player.collides_with(meteor.rect):

                    running = False

        # ===== DIBUJO =====
        screen.fill(settings.BLACK)

        player.draw(screen)

        for bullet in bullets:
            bullet.draw(screen)

        for meteor in meteors:
            meteor.draw(screen)

        score_text = settings.FONT_SMALL.render(
            f"Puntuación: {score}",
            True,
            settings.WHITE
        )

        screen.blit(score_text, (10, 10))

        screen.blit(pause_icon, button_positions['pause'])
        screen.blit(play_icon, button_positions['play'])
        screen.blit(home_icon, button_positions['home'])
        screen.blit(reload_icon, button_positions['reload'])

        if paused:

            paused_text = settings.FONT_TITLE.render(
                "PAUSADO",
                True,
                settings.YELLOW
            )

            screen.blit(
                paused_text,
                paused_text.get_rect(
                    center=(settings.WIDTH // 2, settings.HEIGHT // 2)
                )
            )

        pygame.display.flip()

        clock.tick(settings.FPS)

    # ===== GAME OVER =====
    stop_sound(battle_theme)

    # Reproducir música de game over
    stop_sound(home_theme)
    play_sound(gameover_theme, -1)

    draw_game_over(score)

    waiting = True

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_sound(gameover_theme)
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

    stop_sound(gameover_theme)
    play_sound(home_theme, -1)
    return True


# ===== MAIN =====
def main():
    play_sound(home_theme, -1)

    running = True
    menu_stage = 0  # 0: pantalla de "Presione cualquier tecla", 1: menú visual
    option_rects = None


    while running:
        if menu_stage == 0:
            # Portada con título estilo StarFox y arte
            screen.fill(settings.BLACK)
            # Título grande
            font_title = settings.FONT_TITLE
            title_text = "StarShip"
            title = font_title.render(title_text, True, settings.WHITE)
            title_rect = title.get_rect(center=(settings.WIDTH // 2, 180))

            # Nave inclinada a la izquierda
            ship_img = pygame.transform.rotozoom(starship_img, 45, 5.0)
            ship_rect = ship_img.get_rect(midleft=(title_rect.left - 300, title_rect.centery + 200))
            screen.blit(ship_img, ship_rect)

            # Meteoritos a la derecha, varios tamaños
            meteo1 = pygame.transform.scale(asteroid_images[0], (70, 70))
            meteo2 = pygame.transform.scale(asteroid_images[1], (40, 40))
            meteo3 = pygame.transform.scale(asteroid_images[0], (30, 30))
            meteo4 = pygame.transform.scale(asteroid_images[1], (55, 55))
            screen.blit(meteo1, meteo1.get_rect(midleft=(title_rect.right + 40, title_rect.centery - 30)))
            screen.blit(meteo2, meteo2.get_rect(midleft=(title_rect.right + 100, title_rect.centery + 10)))
            screen.blit(meteo3, meteo3.get_rect(midleft=(title_rect.right + 80, title_rect.centery - 50)))
            screen.blit(meteo4, meteo4.get_rect(midleft=(title_rect.right + 60, title_rect.centery + 40)))

            # Título
            screen.blit(title, title_rect)

            # Mensaje minimalista
            msg = settings.FONT_MENU.render("Presione SPACE para continuar", True, settings.GRAY)
            screen.blit(msg, msg.get_rect(center=(settings.WIDTH // 2, 700)))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        menu_stage = 1
                        break
            clock.tick(settings.FPS)
            continue

        # Menú visual de modos con hover

        mouse_pos = pygame.mouse.get_pos()
        selected = None
        # Solo calcular hover y dibujar una vez
        temp_option_rects = draw_menu_visual(selected=None)
        for opt, rect in temp_option_rects.items():
            if rect.collidepoint(mouse_pos):
                selected = opt
                break
        option_rects = draw_menu_visual(selected=selected)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if selected is not None:
                    if selected == 1:
                        running = play_single_player()
                    elif selected == 2:
                        # Aquí iría la función de multijugador
                        pass
        clock.tick(settings.FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()