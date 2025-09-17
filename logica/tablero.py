"""
Módulo que implementa el tablero de triqui (3x3).

Contiene la clase TableroTriqui que maneja el estado del juego,
los movimientos válidos, y la detección de ganadores.
"""

class TableroTriqui:
    """
    Tablero 3x3 para el juego de Triqui.
    
    Representa el estado del juego usando una lista de 9 elementos,
    donde cada posición corresponde a una celda del tablero numerada de 0 a 8:
    
    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8
    """
    
    def __init__(self):
        """
        Inicializa un tablero vacío de 3x3.
        
        Crea las estructuras de datos necesarias:
        - lista_celdas: Estado de cada celda (espacio vacío = " ")
        - lista_lineas_ganadoras: Todas las combinaciones posibles de victoria
        """
        self.lista_celdas = [" "] * 9  # 9 celdas inicialmente vacías
        # Definir todas las líneas ganadoras posibles (filas, columnas, diagonales)
        self.lista_lineas_ganadoras = [
            [0, 1, 2],  # Fila superior
            [3, 4, 5],  # Fila media
            [6, 7, 8],  # Fila inferior
            [0, 3, 6],  # Columna izquierda
            [1, 4, 7],  # Columna central
            [2, 5, 8],  # Columna derecha
            [0, 4, 8],  # Diagonal principal
            [2, 4, 6]   # Diagonal secundaria
        ]

    def reiniciar_tablero(self):
        """
        Reinicia el tablero a su estado inicial vacío.
        
        Limpia todas las celdas para permitir comenzar una nueva partida.
        """
        self.lista_celdas = [" "] * 9

    def crear_copia_de_tablero(self):
        """
        Crea una copia independiente del tablero actual.
        
        Útil para simular movimientos sin afectar el estado real del juego.
        La copia incluye el mismo estado de todas las celdas.
        
        Returns:
            TableroTriqui: Nueva instancia con el mismo estado que el tablero actual
        """
        copia_tablero = TableroTriqui()
        copia_tablero.lista_celdas = self.lista_celdas[:]  # Copia superficial de la lista
        return copia_tablero

    def obtener_movimientos_disponibles(self):
        """
        Obtiene todos los movimientos válidos (celdas vacías) en el tablero actual.
        
        Recorre todas las celdas y retorna los índices de las que están vacías.
        
        Returns:
            list: Lista de índices (0-8) correspondientes a celdas vacías
        """
        lista_movimientos_disponibles = []
        indice_posicion = 0
        
        # Revisar cada celda del tablero
        while indice_posicion < 9:
            if self.lista_celdas[indice_posicion] == " ":  # Celda vacía
                lista_movimientos_disponibles.append(indice_posicion)
            indice_posicion += 1
        return lista_movimientos_disponibles

    def colocar_marca_en_posicion(self, marca, indice_posicion):
        """
        Coloca una marca ('X' o 'O') en la posición especificada.
        
        Valida que la posición sea válida y esté vacía antes de colocar la marca.
        
        Args:
            marca (str): La marca a colocar ('X' o 'O')
            indice_posicion (int): Índice de la posición donde colocar (0-8)
            
        Returns:
            bool: True si el movimiento fue exitoso, False si fue inválido
        """
        # Validar que la posición esté dentro del rango válido
        if indice_posicion < 0 or indice_posicion > 8:
            return False
        # Validar que la celda esté vacía
        if self.lista_celdas[indice_posicion] != " ":
            return False
        # Colocar la marca en la posición
        self.lista_celdas[indice_posicion] = marca
        return True

    def esta_lleno_el_tablero(self):
        """
        Verifica si el tablero está completamente lleno (no hay movimientos disponibles).
        
        Recorre todas las celdas buscando espacios vacíos.
        
        Returns:
            bool: True si todas las celdas están ocupadas, False si hay al menos una vacía
        """
        indice_posicion = 0
        while indice_posicion < 9:
            if self.lista_celdas[indice_posicion] == " ":  # Encontró una celda vacía
                return False
            indice_posicion += 1
        return True  # No se encontraron celdas vacías

    def obtener_ganador(self):
        """
        Determina el ganador del juego o si hay empate.
        
        Revisa todas las líneas ganadoras posibles para ver si algún jugador
        ha completado una línea. Si no hay ganador pero el tablero está lleno,
        declara empate.
        
        Returns:
            str or None: 
                - 'X' si gana el jugador X
                - 'O' si gana el jugador O  
                - 'D' si hay empate (tablero lleno sin ganador)
                - None si el juego continúa
        """
        indice_linea = 0
        
        # Revisar cada línea ganadora posible
        while indice_linea < len(self.lista_lineas_ganadoras):
            linea = self.lista_lineas_ganadoras[indice_linea]
            valor_a = self.lista_celdas[linea[0]]  # Primera posición de la línea
            valor_b = self.lista_celdas[linea[1]]  # Segunda posición de la línea
            valor_c = self.lista_celdas[linea[2]]  # Tercera posición de la línea
            
            # Si los tres valores son iguales y no vacíos, hay un ganador
            if valor_a != " " and valor_a == valor_b and valor_b == valor_c:
                return valor_a  # Retornar la marca ganadora ('X' o 'O')
            indice_linea += 1
            
        # Si no hay ganador pero el tablero está lleno, es empate
        if self.esta_lleno_el_tablero():
            return "D"  # D = Draw (empate)
            
        return None  # El juego continúa
