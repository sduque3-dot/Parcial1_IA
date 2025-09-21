"""
Módulo que implementa la inteligencia artificial mejorada para el juego de triqui.

Versión mejorada que corrige problemas de priorización en la evaluación de movimientos.
"""

def obtener_marca_contraria(marca_actual):
    """
    Devuelve la marca contraria del jugador actual ('X' <-> 'O').
    
    Args:
        marca_actual (str): La marca actual ('X' o 'O')
        
    Returns:
        str: La marca contraria
    """
    if marca_actual == "X":
        return "O"
    return "X"

class IAConPesos:
    """
    IA que evalúa movimientos con sistema jerárquico de prioridades:
    1. Movimientos ganadores inmediatos
    2. Bloqueos de movimientos ganadores del rival
    3. Evaluación estratégica con pesos configurables
    """
    
    def __init__(self, estrategia_de_juego):
        """
        Inicializa la IA con pesos configurables para diferentes factores del juego.
        
        Args:
            estrategia_de_juego (EstrategiaDeJuego): Objeto con diccionario de pesos
        """
        self.estrategia_de_juego = estrategia_de_juego

    def elegir_movimiento(self, tablero, mi_marca):
        """
        Elige el mejor movimiento usando evaluación jerárquica por prioridades.
        
        Prioridades: 1) Ganar inmediatamente, 2) Bloquear victoria rival, 3) Evaluación estratégica
        
        Args:
            tablero (TableroTriqui): Estado actual del tablero
            mi_marca (str): Marca de esta IA ('X' o 'O')
            
        Returns:
            int: Índice de posición elegida (0-8) o -1 si no hay movimientos
        """
        marca_del_rival = obtener_marca_contraria(mi_marca)
        lista_movimientos_disponibles = tablero.obtener_movimientos_disponibles()
        
        if len(lista_movimientos_disponibles) == 0:
            return -1

        # PRIORIDAD 1: Buscar movimientos ganadores inmediatos
        for indice_posicion in lista_movimientos_disponibles:
            tablero_simulado = tablero.crear_copia_de_tablero()
            tablero_simulado.colocar_marca_en_posicion(mi_marca, indice_posicion)
            if tablero_simulado.obtener_ganador() == mi_marca:
                return indice_posicion

        # PRIORIDAD 2: Bloquear movimientos ganadores del rival
        for indice_posicion in lista_movimientos_disponibles:
            tablero_simulado = tablero.crear_copia_de_tablero()
            tablero_simulado.colocar_marca_en_posicion(marca_del_rival, indice_posicion)
            if tablero_simulado.obtener_ganador() == marca_del_rival:
                return indice_posicion

        # PRIORIDAD 3: Evaluación detallada con pesos estratégicos
        mejor_puntaje = None
        mejores_movimientos = []

        for indice_posicion in lista_movimientos_disponibles:
            puntaje = self.puntuar_movimiento_detallado(tablero, mi_marca, marca_del_rival, indice_posicion)
            
            if mejor_puntaje is None or puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
                mejores_movimientos = [indice_posicion]
            elif puntaje == mejor_puntaje:
                mejores_movimientos.append(indice_posicion)

        import random
        return random.choice(mejores_movimientos)

    def puntuar_movimiento_detallado(self, tablero, mi_marca, marca_del_rival, indice_posicion):
        """
        Calcula puntaje para un movimiento considerando posición, amenazas y bloqueos.
        
        Args:
            tablero (TableroTriqui): Estado actual del tablero
            mi_marca (str): Marca de esta IA
            marca_del_rival (str): Marca del oponente
            indice_posicion (int): Posición a evaluar (0-8)
            
        Returns:
            float: Puntaje calculado (mayor = mejor movimiento)
        """
        pesos = self.estrategia_de_juego.diccionario_pesos
        puntaje_total = 0

        # Simular el movimiento
        tablero_simulado = tablero.crear_copia_de_tablero()
        tablero_simulado.colocar_marca_en_posicion(mi_marca, indice_posicion)

        # Factor 1: Valor posicional (centro > esquinas > lados)
        if indice_posicion == 4:  # Centro
            puntaje_total += pesos["peso_centro"]
        elif indice_posicion in [0, 2, 6, 8]:  # Esquinas
            puntaje_total += pesos["peso_esquina"]
        elif indice_posicion in [1, 3, 5, 7]:  # Lados
            puntaje_total += pesos["peso_lado"]

        # Factor 2: Crear amenazas propias
        amenazas_propias = self.contar_dos_en_linea(tablero_simulado, mi_marca)
        puntaje_total += amenazas_propias * pesos["peso_fork"]

        # Factor 3: Bloquear amenazas del rival
        amenazas_rival_antes = self.contar_dos_en_linea(tablero, marca_del_rival)
        amenazas_rival_despues = self.contar_dos_en_linea(tablero_simulado, marca_del_rival)
        if amenazas_rival_despues < amenazas_rival_antes:
            puntaje_total += pesos["peso_bloquear_fork"]

        # Factor 4: Bonus por forks múltiples
        if amenazas_propias >= 2:
            puntaje_total += pesos["peso_fork"] * 2

        return puntaje_total

    def contar_dos_en_linea(self, tablero, marca_objetivo):
        """
        Cuenta líneas con 2 marcas del jugador y 1 espacio vacío (amenazas inmediatas).
        
        Args:
            tablero (TableroTriqui): Estado del tablero a evaluar
            marca_objetivo (str): Marca del jugador a contar ('X' o 'O')
            
        Returns:
            int: Número de amenazas inmediatas del jugador
        """
        total_lineas = 0
        
        for linea in tablero.lista_lineas_ganadoras:
            valores = [tablero.lista_celdas[linea[0]], 
                      tablero.lista_celdas[linea[1]], 
                      tablero.lista_celdas[linea[2]]]
            
            contador_marca = valores.count(marca_objetivo)
            contador_vacios = valores.count(" ")
            contador_rival = 3 - contador_marca - contador_vacios
            
            # 2 marcas propias + 1 vacío + 0 rival = amenaza
            if contador_marca == 2 and contador_vacios == 1 and contador_rival == 0:
                total_lineas += 1
                
        return total_lineas

    def contar_forks(self, tablero, marca_objetivo):
        """
        Alias de contar_dos_en_linea para mayor claridad semántica.
        
        Args:
            tablero (TableroTriqui): Estado actual del tablero
            marca_objetivo (str): Marca del jugador a evaluar
            
        Returns:
            int: Número de amenazas del jugador
        """
        return self.contar_dos_en_linea(tablero, marca_objetivo)

    def contar_forks_potenciales_del_rival(self, tablero, marca_del_rival):
        """
        Calcula amenazas totales que el rival podría crear en sus próximos movimientos.
        
        Args:
            tablero (TableroTriqui): Estado actual del tablero
            marca_del_rival (str): Marca del oponente
            
        Returns:
            int: Total de amenazas potenciales del rival
        """
        lista_movimientos_disponibles = tablero.obtener_movimientos_disponibles()
        total_forks_potenciales = 0
        
        for indice_posicion in lista_movimientos_disponibles:
            tablero_prueba = tablero.crear_copia_de_tablero()
            tablero_prueba.colocar_marca_en_posicion(marca_del_rival, indice_posicion)
            total_forks_potenciales += self.contar_forks(tablero_prueba, marca_del_rival)
            
        return total_forks_potenciales