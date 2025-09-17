"""
Módulo que evalúa el rendimiento de estrategias de juego.

Contiene funciones para medir qué tan efectiva es una estrategia
jugando contra diferentes tipos de oponentes y convertir resultados
de juego en puntuaciones numéricas.
"""

from .tablero import TableroTriqui
from .ia import IAConPesos
from .oponentes import OponenteAleatorio
from .simulador import jugar_partida_en_tablero

def convertir_resultado_a_puntos(resultado_final, mi_marca_referencia):
    """
    Convierte el resultado de una partida en una puntuación numérica.
    
    Este sistema de puntuación incentiva las victorias, penaliza las derrotas,
    y otorga puntos moderados por empates.
    
    Args:
        resultado_final (str): Resultado de la partida ('X', 'O', o 'D')
        mi_marca_referencia (str): Marca del jugador desde cuya perspectiva se evalúa
        
    Returns:
        int: Puntuación obtenida:
            - 3 puntos por victoria
            - 1 punto por empate  
            - 0 puntos por derrota
    """
    if resultado_final == "D":  # Empate (Draw)
        return 1
    if resultado_final == mi_marca_referencia:  # Victoria
        return 3
    return 0  # Derrota

def evaluar_estrategia_contra_aleatorio(estrategia_de_juego, numero_partidas=8):
    """
    Evalúa el rendimiento de una estrategia jugando múltiples partidas contra un oponente aleatorio.
    
    La estrategia juega tanto como 'X' (iniciando) como 'O' (segundo turno)
    para obtener una evaluación equilibrada y robusta. El oponente aleatorio
    proporciona variabilidad en los juegos y sirve como línea base.
    
    Args:
        estrategia_de_juego (EstrategiaDeJuego): La estrategia a evaluar
        numero_partidas (int): Número de rondas de evaluación (default: 8)
                              Cada ronda incluye 2 partidas (como X y como O)
    
    Returns:
        float: Puntuación total acumulada a través de todas las partidas
               Rango típico: 0.0 (perdió todas) a 6*numero_partidas (ganó todas)
    
    Note:
        - Cada ronda incluye 2 partidas para balancear la ventaja del primer turno
        - Una estrategia perfecta contra oponente aleatorio debería obtener ~4-5 puntos por ronda
        - El número total de partidas jugadas es 2 * numero_partidas
    """
    # Crear instancias necesarias para la evaluación
    tablero_de_pruebas = TableroTriqui()  # Tablero reutilizable para todas las partidas
    ia_a_evaluar = IAConPesos(estrategia_de_juego)  # IA con la estrategia a evaluar
    oponente_basico = OponenteAleatorio()  # Oponente de control aleatorio

    puntaje_acumulado = 0  # Puntuación total acumulada
    indice_partida = 0
    
    # Ejecutar el número especificado de rondas de evaluación
    while indice_partida < numero_partidas:
        # Partida 1: IA juega como 'X' (inicia primero)
        resultado_cuando_inicia_X = jugar_partida_en_tablero(
            tablero_de_pruebas, 
            ia_a_evaluar,     # IA como jugador X
            oponente_basico,  # Oponente como jugador O
            marca_que_inicia="X"
        )
        
        # Partida 2: IA juega como 'O' (inicia segundo)  
        resultado_cuando_inicia_O = jugar_partida_en_tablero(
            tablero_de_pruebas,
            oponente_basico,  # Oponente como jugador X
            ia_a_evaluar,     # IA como jugador O
            marca_que_inicia="X"  # El oponente (X) inicia
        )
        
        # Convertir resultados a puntuaciones y acumular
        puntaje_acumulado += convertir_resultado_a_puntos(resultado_cuando_inicia_X, "X")
        puntaje_acumulado += convertir_resultado_a_puntos(resultado_cuando_inicia_O, "O")
        
        indice_partida += 1

    return float(puntaje_acumulado)
