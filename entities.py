"""
Entidades del juego: Jugador y Meteoritos
"""

import pygame
import settings


class Player:
    """Clase que representa el jugador"""
    
    def __init__(self, x, y, img=None):
        self.rect = pygame.Rect(x, y, settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT)
        self.img = img
        self.speed = settings.PLAYER_SPEED
    
    def move_left(self, max_x=0):
        if self.rect.left > max_x:
            self.rect.x -= self.speed
    
    def move_right(self, max_x):
        if self.rect.right < max_x:
            self.rect.x += self.speed
    
    def move_up(self, max_y=0):
        if self.rect.top > max_y:
            self.rect.y -= self.speed
    
    def move_down(self, max_y):
        if self.rect.bottom < max_y:
            self.rect.y += self.speed
    
    def draw(self, screen):
        if self.img:
            screen.blit(self.img, self.rect)
        else:
            pygame.draw.rect(screen, settings.WHITE, self.rect)
    
    def collides_with(self, meteor_rect):
        return self.rect.colliderect(meteor_rect)


class Meteor:
    """Clase que representa un meteorito con su clase asociada"""
    
    def __init__(self, x, y, meteor_class, img=None):
        self.meteor_class = meteor_class
        self.size_multiplier = meteor_class['size_multiplier']
        self.velocity_multiplier = meteor_class['velocity_multiplier']
        self.rotation_speed_range = meteor_class['rotation_speed_range']
        self.color = meteor_class['color']
        
        # Dimensiones ajustadas según la clase
        self.width = int(settings.METEOR_WIDTH * self.size_multiplier)
        self.height = int(settings.METEOR_HEIGHT * self.size_multiplier)
        
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.img = img
        self.angle = 0
        self.rotation_speed = 0  # Se asignará en simulation_logic
    
    def move(self, base_velocity=-5):
        """Mueve el meteorito según su clase"""
        velocity_x = base_velocity * self.velocity_multiplier
        self.rect.x += velocity_x
        self.angle += self.rotation_speed
    
    def is_off_screen(self, screen_width):
        return self.rect.right < 0
    
    def draw(self, screen):
        if self.img:
            rotated_img = pygame.transform.rotate(self.img, self.angle)
            rotated_rect = rotated_img.get_rect(center=self.rect.center)
            screen.blit(rotated_img, rotated_rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
