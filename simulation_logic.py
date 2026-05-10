"""
Lógica de simulación: distribuciones probabilísticas para meteoritos
"""

import random
import numpy as np
import settings
from entities import Meteor


class MeteorSpawner:
    """
    Generador de meteoritos usando distribuciones probabilísticas.
    - Distribución exponencial para el tiempo entre llegadas
    - Distribución uniforme discreta para clases de meteoritos
    """
    
    def __init__(self, lambda_param=0.1):
        """
        Inicializa el spawner.
        
        Args:
            lambda_param: Parámetro lambda de la distribución exponencial.
                         Mayor valor = más meteoritos por unidad de tiempo
        """
        self.lambda_param = lambda_param
        self.time_since_last_spawn = 0
        self.next_spawn_time = self._get_next_spawn_time()
        self.frame_count = 0
    
    def _get_next_spawn_time(self):
        """
        Calcula el siguiente tiempo de aparición usando distribución exponencial.
        
        La distribución exponencial modela bien el tiempo entre eventos en procesos
        aleatorios (como llegada de meteoritos).
        
        Returns:
            float: Próximo tiempo de aparición en frames
        """
        # Generar número desde distribución exponencial
        time_interval = np.random.exponential(1 / self.lambda_param)
        # Convertir a frames (escalar por 60 para aproximar a segundos)
        return time_interval * 30  # Aproximadamente frames
    
    def _select_meteor_class(self):
        """
        Selecciona la clase de meteorito usando distribución uniforme discreta.
        
        Probabilidades:
        - Clase 1 (Pequeños y Veloces): 30%
        - Clase 2 (Normales): 50%
        - Clase 3 (Grandes y Pesados): 20%
        
        Returns:
            dict: La clase de meteorito seleccionada
        """
        # Distribución uniforme discreta - selecciona índice ponderado
        probabilities = [mc['probability'] for mc in settings.METEOR_CLASSES]
        class_index = np.random.choice(len(settings.METEOR_CLASSES), p=probabilities)
        return settings.METEOR_CLASSES[class_index]
    
    def should_spawn(self):
        """
        Determina si es momento de generar un nuevo meteorito.
        
        Returns:
            bool: True si debe generarse un meteorito
        """
        self.frame_count += 1
        
        if self.frame_count >= self.next_spawn_time:
            self.next_spawn_time = self._get_next_spawn_time()
            self.frame_count = 0
            return True
        
        return False
    
    def spawn_meteor(self, meteor_img=None):
        """
        Crea un nuevo meteorito con parámetros aleatorios.
        
        Args:
            meteor_img: Imagen del meteorito (opcional)
        
        Returns:
            Meteor: Nueva instancia de meteorito
        """
        # Seleccionar clase
        meteor_class = self._select_meteor_class()
        
        # Posición aleatoria en el borde derecho
        y_pos = random.randint(0, settings.HEIGHT - int(settings.METEOR_HEIGHT * meteor_class['size_multiplier']))
        
        # Crear meteorito
        meteor = Meteor(settings.WIDTH, y_pos, meteor_class, meteor_img)
        
        # Asignar velocidad de rotación aleatoria dentro del rango de la clase
        rotation_min, rotation_max = meteor.rotation_speed_range
        meteor.rotation_speed = random.uniform(rotation_min, rotation_max)
        
        return meteor


def create_spawner(lambda_param=0.1):
    """
    Factory function para crear un spawner de meteoritos.
    
    Args:
        lambda_param: Parámetro de la distribución exponencial
    
    Returns:
        MeteorSpawner: Instancia del generador
    """
    return MeteorSpawner(lambda_param)
