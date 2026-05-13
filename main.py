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

if audio_enabled:
    home_theme = load_sound("home_theme.wav")
    battle_theme = load_sound("battle_theme.wav")

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


def draw_menu():
    screen.fill(settings.BLACK)

    title = settings.FONT_TITLE.render(
        "STARSHIP GAME",
        True,
        settings.WHITE
    )

    screen.blit(
        title,
        title.get_rect(center=(settings.WIDTH // 2, 120))
    )

    options = [
        "1. Single Player",
        "2. Multiplayer",
        "3. Exit"
    ]

    y = 260

    for option in options:
        text = settings.FONT_MENU.render(
            option,
            True,
            settings.WHITE
        )

        screen.blit(
            text,
            text.get_rect(center=(settings.WIDTH // 2, y))
        )

        y += 90

    pygame.display.flip()


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
        "Presiona cualquier tecla",
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
        retry_text.get_rect(center=(settings.WIDTH // 2, 420))
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

    draw_game_over(score)

    waiting = True

    while waiting:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                waiting = False

    play_sound(home_theme, -1)

    return True


# ===== MAIN =====
def main():

    play_sound(home_theme, -1)

    running = True

    while running:

        draw_menu()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:

                    running = play_single_player()

                elif event.key == pygame.K_3:

                    running = False

        clock.tick(settings.FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()