"""
Módulo que implementa diferentes tipos de oponentes para el juego de triqui.

Contiene implementaciones de jugadores automáticos con diferentes niveles
de complejidad para entrenar y evaluar las estrategias de IA.
"""

import random

class OponenteAleatorio:
    """
    Oponente que elige movimientos completamente al azar.
    
    Este oponente básico es útil para:
    - Entrenar algoritmos genéticos (proporciona variabilidad)
    - Evaluaciones de línea base (cualquier IA debería superarlo)
    - Pruebas rápidas de funcionalidad
    """
    
    def elegir_movimiento(self, tablero, mi_marca):
        """
        Selecciona un movimiento aleatorio entre las posiciones disponibles.
        
        No considera ninguna estrategia; simplemente elige al azar
        entre todas las celdas vacías del tablero.
        
        Args:
            tablero (TableroTriqui): Estado actual del tablero de juego
            mi_marca (str): Marca asignada a este jugador ('X' o 'O')
                          (no se utiliza en esta implementación)
        
        Returns:
            int: Índice de la posición elegida (0-8) o -1 si no hay movimientos disponibles
        """
        lista_movimientos_disponibles = tablero.obtener_movimientos_disponibles()
        
        # Si no hay movimientos posibles, retornar código de error
        if len(lista_movimientos_disponibles) == 0:
            return -1
            
        # Seleccionar aleatoriamente una de las posiciones disponibles
        return random.choice(lista_movimientos_disponibles)
