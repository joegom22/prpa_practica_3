Programación Paralela: Práctica 3

"""
**Práctica de Programación Distribuida**
"""

Idioma: Python

Creadores:

    Joel Gómez Santos
    
    Sergio Monzon Garces
    
    Celeste Rhodes Rodríguez

**1. Motivación**

El objetivo es realizar un juego interactivo en el que juegan a la vez dos personas desde ordenadores diferentes. De este modo tenemos un programa que tiene información distribuida y que se comparte entre los clientes, en este caso, los jugadores.

**2. Descripción**

Se trata de un juego para 2 personas en el que, moviendo tu personaje por el tablero sin caerte, debes conseguir 3 banderas antes que tu contrincante.

El juego tiene dos variantes:

-En Sala_1_bandera y player_1_bandera una aparece una bandera cada vez. Es decir, se inicia el juego y aparece una bandera; cuando uno de los dos jugadores la captura, ambos vuelven a la casilla de salida y aparece una nueva bandera en el tablero.

-En Sala_todas_banderas y player_todas_banderas aparecen todas las banderas desde el inicio del juego, desapareciendo una al ser capturada y manteniéndose las demás.

Se evita el acceso simultáneo a funciones que no deben efectuarse a la vez con un mutex, como por ejemplo la función de obtención de una bandera.

**3. Modo de uso**

Un sistema actuará como sala, que será quien espere a que se conecten los jugadores e inicializa el juego. Los dos jugadores pueden estar en el mismo ordenador que la sala o en otro, no tienen por qué estar en el mismo entre sí tampoco.

El usuario que desee ejecutar un programa de jugador debe descargarse los módulos multiprocessing, pygame, traceback, time, sys, os y json; los cuales se instalan fácilmente en el ordenador. Además, es necesario tener descargado el archivo settings que se incluye en este repositorio y donde se encuentran importantes datos del juego, así como las imágenes de los sprites del juego que se incluyen en la carpeta fotos.


**Jugar:**

El archivo de la sala y el del jugador admiten una dirección ip como parámetro, deben proporcionar la adecuada si desean jugar.

Para jugar es necesario que en un ordenador esté el programa de la sala ejecutándose, basta con ejecutar el programa con las condiciones que hemos descrito anteriormente y la sala se ejecuta. Además, cada usuario que desee jugar como personaje debe ejecutar el programa de jugador asegurándose de cumplir las condiciones arriba mencionadas. Una vez comience el juego el usuario manejará a su personaje con las flechas de su teclado.

Para que las imagenes se muestren correctamente, es necesario que en la misma carpeta se encuentren:
    1. los archivos settings.py, los archivos de la sala y del player.
    2. las fotos descargadas (se encuentran en la carpeta 'fotos' de este repositorio)
    
Los diferentes archivos .py a destacar son los siguientes:
1. sala_1_bandera_ip_parametro.py y player_1_bandera_ip_parametro.py : es el juego donde solo aparece 1 bandera por conquista. Para ello, es necesario iniciar el juego poniendo en la terminal:     _python3 sala_1_bandera_ip_parametro.py + (numero ip del ordenador que ejecuta la sala) / python3 player_1_bandera_ip_parametro.py + (numero ip del ordenador que ejecuta la sala)_
1. sala_todas_banderas_ip_parametro.py y player_todas_banderas_ip_parametro.py : es el juego donde aparecen todas las banders por conquista. Para ello, es necesario iniciar el juego poniendo en la terminal: _python3 sala_todas_banderas_ip_parametro.py + (numero ip del ordenador que ejecuta la sala)  / python3 player_todas_banderas_ip_parametro.py + (numero ip del ordenador que ejecuta la sala) _
