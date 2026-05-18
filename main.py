"""
StarShip Game - Juego de esquivar meteoritos
Archivo principal que ejecuta el juego
"""

import pygame
import sys
import os
import json
import random
import math

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


# ===== SISTEMA DE CARATULA (INDEPENDIENTE DEL JUEGO) =====
class TitleStar:
    """Estrella del fondo de la caratula"""
    def __init__(self, x, y, brightness):
        self.x = x
        self.y = y
        self.brightness = brightness
        self.max_brightness = brightness
        self.pulse_speed = random.uniform(0.02, 0.08)
        self.pulse_direction = random.choice([-1, 1])
    
    def update(self):
        """Anima el brillo de la estrella"""
        self.brightness += self.pulse_speed * self.pulse_direction
        if self.brightness >= self.max_brightness or self.brightness <= self.max_brightness * 0.3:
            self.pulse_direction *= -1
    
    def draw(self, surface):
        """Dibuja la estrella"""
        color = (int(self.brightness), int(self.brightness), int(self.brightness))
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), 1)


class StarsField:
    """Campo de estrellas animadas"""
    def __init__(self, width, height, num_stars=200):
        self.width = width
        self.height = height
        self.stars = []
        
        for _ in range(num_stars):
            x = random.uniform(0, width)
            y = random.uniform(0, height)
            brightness = random.uniform(80, 255)
            self.stars.append(TitleStar(x, y, brightness))
    
    def update(self):
        """Actualiza todas las estrellas"""
        for star in self.stars:
            star.update()
    
    def draw(self, surface):
        """Dibuja todas las estrellas"""
        for star in self.stars:
            star.draw(surface)


class TitleMeteor:
    """Meteorito de la caratula con movimiento independiente"""
    def __init__(self, x, y, image, speed, size_scale, rotation_speed):
        self.x = x
        self.y = y
        self.original_image = image
        self.speed = speed
        self.size_scale = size_scale
        self.rotation_speed = rotation_speed
        self.rotation = 0
        self.rect = self.original_image.get_rect(center=(int(x), int(y)))
    
    def update(self):
        """Actualiza posición y rotación"""
        self.x += self.speed
        self.rotation += self.rotation_speed
        self.rect.center = (int(self.x), int(self.y))
    
    def draw(self, surface):
        """Dibuja el meteorito rotado"""
        scaled_image = pygame.transform.scale(
            self.original_image,
            (int(self.original_image.get_width() * self.size_scale),
             int(self.original_image.get_height() * self.size_scale))
        )
        rotated_image = pygame.transform.rotate(scaled_image, self.rotation)
        rotated_rect = rotated_image.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated_image, rotated_rect)
    
    def is_off_screen(self, width):
        """Verifica si el meteorito salió de la pantalla"""
        return self.x > width + 100 or self.x < -100


class TitleMeteorsSystem:
    """Sistema de meteoritos para la caratula"""
    def __init__(self, width, height, asteroid_images):
        self.width = width
        self.height = height
        self.asteroid_images = asteroid_images
        self.meteors = []
        self.spawn_timer = 0
        self.spawn_interval = 40  # frames entre spawns
    
    def update(self):
        """Actualiza y gestiona meteoritos"""
        self.spawn_timer += 1
        
        # Spawnear nuevos meteoritos
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_meteor()
            self.spawn_timer = 0
        
        # Actualizar meteoritos existentes
        for meteor in self.meteors[:]:
            meteor.update()
            if meteor.is_off_screen(self.width):
                self.meteors.remove(meteor)
    
    def spawn_meteor(self):
        """Crea un nuevo meteorito"""
        y = random.uniform(50, self.height - 100)
        image = random.choice(self.asteroid_images)
        speed = random.uniform(1.5, 4.0)
        size_scale = random.uniform(0.5, 2.5)
        rotation_speed = random.uniform(-8, 8)
        
        meteor = TitleMeteor(-50, y, image, speed, size_scale, rotation_speed)
        self.meteors.append(meteor)
    
    def draw(self, surface):
        """Dibuja todos los meteoritos"""
        for meteor in self.meteors:
            meteor.draw(surface)


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

# ===== SISTEMA DE CARATULA =====
stars_field = StarsField(settings.WIDTH, settings.HEIGHT, num_stars=200)
title_meteors_system = TitleMeteorsSystem(settings.WIDTH, settings.HEIGHT, asteroid_images)

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


# ===== SCORES =====
SCORES_FILE = os.path.join(BASE_DIR, "scores.json")

def load_scores():
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {}

def save_score(name, score):
    scores = load_scores()
    name = name.strip()
    if not name:
        name = "Anon"
        
    if name in scores:
        scores[name] = max(scores[name], score)
    else:
        scores[name] = score
        
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f, indent=4)

def get_player_name(score):
    name = ""
    while True:
        screen.fill(settings.BLACK)
        
        title = settings.FONT_TITLE.render("GAME OVER", True, settings.RED)
        score_text = settings.FONT_MENU.render(f"Puntuación: {score}", True, settings.WHITE)
        prompt_text = settings.FONT_REGULAR.render("Ingresa tu nombre y presiona ENTER:", True, settings.GRAY)
        name_text = settings.FONT_MENU.render(name + "_", True, settings.YELLOW)
        
        screen.blit(title, title.get_rect(center=(settings.WIDTH // 2, 200)))
        screen.blit(score_text, score_text.get_rect(center=(settings.WIDTH // 2, 320)))
        screen.blit(prompt_text, prompt_text.get_rect(center=(settings.WIDTH // 2, 450)))
        screen.blit(name_text, name_text.get_rect(center=(settings.WIDTH // 2, 500)))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 15 and event.unicode.isprintable():
                        name += event.unicode
        clock.tick(settings.FPS)

def show_leaderboard():
    scores = load_scores()
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    title_font = settings.FONT_TITLE
    
    while True:
        screen.fill(settings.BLACK)
        
        title_surf = title_font.render("RANKING", True, settings.YELLOW)
        title_surf = pygame.transform.scale(title_surf, (int(title_surf.get_width()*0.4), int(title_surf.get_height()*0.4)))
        screen.blit(title_surf, title_surf.get_rect(center=(settings.WIDTH // 2, 100)))
        
        y_offset = 220
        if not sorted_scores:
            txt = settings.FONT_MENU.render("No hay puntajes aún.", True, settings.WHITE)
            screen.blit(txt, txt.get_rect(center=(settings.WIDTH // 2, y_offset)))
        else:
            for i, (n, s) in enumerate(sorted_scores[:10]):
                color = settings.WHITE if i > 0 else settings.YELLOW
                txt = settings.FONT_MENU.render(f"{i+1}. {n} - {s}", True, color)
                screen.blit(txt, txt.get_rect(center=(settings.WIDTH // 2, y_offset)))
                y_offset += 45
            
        prompt = settings.FONT_REGULAR.render("Presione SPACE para continuar", True, settings.GRAY)
        screen.blit(prompt, prompt.get_rect(center=(settings.WIDTH // 2, 700)))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        clock.tick(settings.FPS)


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
    lives = 3.0
    level = 1

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

            # Sistema de niveles
            if score >= 100 and level < 3:
                level = 3
                spawner.lambda_param = 0.60
            elif score >= 50 and score < 100 and level < 2:
                level = 2
                spawner.lambda_param = 0.40

            # Spawn meteoros - Solo 1 a la vez en pantalla
            if len(meteors) < 1:

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
                    lives -= 0.5
                    
                    if lives <= 0:
                        running = False

            # Colisiones
            for meteor in meteors[:]:

                if player.collides_with(meteor.rect):
                    meteors.remove(meteor)
                    lives -= 1.0
                    play_sound(explosion_sound)
                    
                    if lives <= 0:
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

        level_text = settings.FONT_SMALL.render(
            f"Nivel: {level}",
            True,
            settings.YELLOW
        )

        lives_text = settings.FONT_SMALL.render(
            f"Vidas: {lives}",
            True,
            settings.RED
        )

        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 40))
        screen.blit(lives_text, (10, 70))

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

    name = get_player_name(score)
    if name is not False:
        save_score(name, score)
        show_leaderboard()

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
            # ===== PORTADA CON FONDO ESTRELLADO Y METEORITOS ANIMADOS =====
            screen.fill(settings.BLACK)
            
            # Dibujar campo de estrellas
            stars_field.update()
            stars_field.draw(screen)
            
            # Actualizar y dibujar meteoritos de la caratula
            title_meteors_system.update()
            title_meteors_system.draw(screen)
            
            # Título en amarillo bonito
            font_title = settings.FONT_TITLE
            title_text = "StarShip"
            # Amarillo bonito (#FFD700 - Gold)
            title = font_title.render(title_text, True, (255, 215, 0))
            title_rect = title.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 - 50))
            screen.blit(title, title_rect)
            
            # Mensaje en la parte inferior
            msg = settings.FONT_MENU.render("Presione SPACE para continuar", True, settings.GRAY)
            screen.blit(msg, msg.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT - 80)))
            
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