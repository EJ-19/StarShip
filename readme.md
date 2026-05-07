# StarShip

**`StarShip`** es un videojuego desarrollado en Python con Pygame, inspirado en la esencia clásica de Star Fox 64, pero reinterpretado en una experiencia completamente original en 2D. El proyecto toma como referencia la dinámica espacial, el combate rápido y la sensación arcade del juego clásico, sin buscar recrearlo directamente.

En *`StarShip`*, el jugador pilota una nave de combate interestelar encargada de defender la galaxia de una amenaza creciente: el despiadado **Fredy Therian Alexander**, un conquistador galáctico decidido a dominar todos los mundos conocidos mediante un ejército mecanizado y tecnología avanzada.

El juego se desarrolla en escenarios espaciales dinámicos donde los enemigos, bombas, mejoras de láser, monedas y distintos eventos aparecen de manera aleatoria utilizando modelos probabilísticos y distribuciones estadísticas. Entre los métodos implementados se encuentran:

* Distribución uniforme
* Distribución exponencial
* Distribución t-inversa
* Generación aleatoria controlada
* Eventos probabilísticos adaptativos

Gracias a este sistema, cada partida ofrece una experiencia distinta, aumentando la rejugabilidad y permitiendo analizar cómo las matemáticas y la estadística pueden aplicarse al diseño de videojuegos.

## Características principales

* Combate espacial en 2D con estilo arcade.
* Inspiración en la jugabilidad clásica de Star Fox.
* Sistema de aparición aleatoria basado en distribuciones estadísticas.
* Mejoras de armas y potenciadores durante la partida.
* Enemigos con diferentes patrones de ataque.
* Recolección de monedas y recursos.
* Batallas contra jefes espaciales.
* Historia original con ambientación galáctica futurista.
* Desarrollo realizado en Python usando Pygame.

## Objetivo del jugador

El jugador deberá sobrevivir a oleadas de enemigos, mejorar su nave y recorrer distintos sectores espaciales hasta enfrentarse al gran enemigo final: **Fredy Therian Alexander**, cuyo objetivo es someter toda la galaxia bajo su control.

*`StarShip`* busca combinar programación, matemáticas y diseño de videojuegos en un proyecto interactivo que mezcle acción, aleatoriedad y estrategia en tiempo real.

## Seguir los pasos del README:
1. Clona el repositorio.
2. CD StarShip.
2. Crea un entorno virtual: 
    ```
    python -m venv .venv
3. Activa el entorno virtual: 
    ```bash
    .\.venv\Scripts\Activate.ps1
4. Instala ***requirements.txt***:
    ```bash
    pip install -r requirements.txt

## Prueba de Pygame
Ejecuta el archivo ***prueba.py*** que servirá para ver si Pygame fue instalado y es ejecutado correctamente.

## Estructura del código
```
StarShip-Game/
│
├── main.py # Punto de entrada (donde corre el juego)
├── aleatoriedad.py # Lógica de aleatoriedad y simulaciones
├── entidades.py # Clases: jugador, enemigos y mejoras
├── configuraciones.py # Configuración general (resolución, colores, velocidad)
│
├── assets/ # Recursos del juego
│ ├── images/ # Sprites (.png)
│ ├── sounds/ # Efectos de sonido (.wav)
│ └── fonts/ # Tipografías (.ttf)
|
└── .gitignore #Excluye archivos temporales y entornos virtuales
└── requirements.txt # Dependencias del proyecto (Pygame)