"""
Módulo que implementa la inteligencia artificial para el juego de triqui.

Contiene la clase IAConPesos que evalúa movimientos basándose en diferentes
estrategias ponderadas, y funciones auxiliares para el manejo de marcas.
"""

def obtener_marca_contraria(marca_actual):
    """
    Devuelve la marca contraria del jugador.
    
    Args:
        marca_actual (str): La marca actual ('X' o 'O')
        
    Returns:
        str: La marca contraria ('X' <-> 'O')
    """
    if marca_actual == "X":
        return "O"
    return "X"

class IAConPesos:
    """
    IA que evalúa movimientos usando un diccionario de pesos para diferentes estrategias.
    
    Esta clase implementa una IA que considera múltiples factores para elegir el mejor
    movimiento: ganar inmediatamente, bloquear al oponente, controlar el centro,
    ocupar esquinas, crear forks, etc.
    """
    
    def __init__(self, estrategia_de_juego):
        """
        Inicializa la IA con una estrategia de juego específica.
        
        Args:
            estrategia_de_juego (EstrategiaDeJuego): Objeto que contiene los pesos
                para evaluar diferentes aspectos del juego
        """
        self.estrategia_de_juego = estrategia_de_juego  # Estrategia con pesos para la evaluación

    def elegir_movimiento(self, tablero, mi_marca):
        """
        Elige el mejor movimiento disponible basándose en la evaluación de pesos.
        
        Evalúa todos los movimientos posibles, calcula un puntaje para cada uno
        usando los pesos de la estrategia, y retorna uno de los mejores movimientos
        (si hay empate, elige aleatoriamente entre los mejores).
        
        Args:
            tablero (TableroTriqui): El estado actual del tablero
            mi_marca (str): La marca que representa a esta IA ('X' o 'O')
            
        Returns:
            int: Índice de la posición elegida (0-8) o -1 si no hay movimientos disponibles
        """
        marca_del_rival = obtener_marca_contraria(mi_marca)
        lista_movimientos_disponibles = tablero.obtener_movimientos_disponibles()
        
        # Si no hay movimientos disponibles, retornar -1
        if len(lista_movimientos_disponibles) == 0:
            return -1

        mejor_puntaje_encontrado = None  # El mejor puntaje encontrado hasta ahora
        lista_mejores_movimientos = []   # Lista de movimientos con el mejor puntaje

        indice_lista = 0
        # Evaluar cada movimiento disponible
        while indice_lista < len(lista_movimientos_disponibles):
            indice_posicion = lista_movimientos_disponibles[indice_lista]
            # Calcular puntaje del movimiento usando los pesos de la estrategia
            puntaje_movimiento = self.puntuar_movimiento(tablero, mi_marca, marca_del_rival, indice_posicion)
            
            # Actualizar la lista de mejores movimientos
            if mejor_puntaje_encontrado is None or puntaje_movimiento > mejor_puntaje_encontrado:
                mejor_puntaje_encontrado = puntaje_movimiento
                lista_mejores_movimientos = [indice_posicion]
            elif puntaje_movimiento == mejor_puntaje_encontrado:
                lista_mejores_movimientos.append(indice_posicion)
            indice_lista += 1

        # Si hay múltiples movimientos con el mismo puntaje, elegir uno aleatoriamente
        import random
        return random.choice(lista_mejores_movimientos)

    def puntuar_movimiento(self, tablero, mi_marca, marca_del_rival, indice_posicion):
        """
        Calcula el puntaje de un movimiento específico basándose en múltiples factores.
        
        Evalúa factores como: ganar inmediatamente, bloquear al rival, controlar
        posiciones estratégicas (centro, esquinas, lados), crear forks, y bloquear forks rivales.
        
        Args:
            tablero (TableroTriqui): Estado actual del tablero
            mi_marca (str): Marca de esta IA
            marca_del_rival (str): Marca del oponente
            indice_posicion (int): Posición a evaluar (0-8)
            
        Returns:
            float: Puntaje calculado para este movimiento
        """
        pesos = self.estrategia_de_juego.diccionario_pesos
        puntaje_total = 0

        # Simular el movimiento para evaluar sus consecuencias
        tablero_simulado = tablero.crear_copia_de_tablero()
        tablero_simulado.colocar_marca_en_posicion(mi_marca, indice_posicion)

        # FACTOR 1: Ganar inmediatamente tiene alta prioridad
        if tablero_simulado.obtener_ganador() == mi_marca:
            puntaje_total += 10 * pesos["peso_ganar"]

        # FACTOR 2: Evaluar si el rival puede ganar en el próximo turno
        tablero_para_rival = tablero.crear_copia_de_tablero()
        lista_movimientos_rival = tablero_para_rival.obtener_movimientos_disponibles()
        rival_tiene_victoria_inmediata = False
        indice_mov_rival = 0
        
        # Verificar si el rival tiene algún movimiento ganador
        while indice_mov_rival < len(lista_movimientos_rival):
            indice_posicion_rival = lista_movimientos_rival[indice_mov_rival]
            tablero_tentativo_rival = tablero_para_rival.crear_copia_de_tablero()
            tablero_tentativo_rival.colocar_marca_en_posicion(marca_del_rival, indice_posicion_rival)
            if tablero_tentativo_rival.obtener_ganador() == marca_del_rival:
                rival_tiene_victoria_inmediata = True
                break
            indice_mov_rival += 1

        # Si el rival puede ganar, evaluar si nuestro movimiento lo bloquea
        if rival_tiene_victoria_inmediata:
            tablero_despues_de_mi = tablero.crear_copia_de_tablero()
            tablero_despues_de_mi.colocar_marca_en_posicion(mi_marca, indice_posicion)
            lista_movimientos_posteriores = tablero_despues_de_mi.obtener_movimientos_disponibles()
            rival_aun_puede_ganar = False
            indice_mov_posterior = 0
            
            # Verificar si después de nuestro movimiento, el rival aún puede ganar
            while indice_mov_posterior < len(lista_movimientos_posteriores):
                indice_posicion_rival_2 = lista_movimientos_posteriores[indice_mov_posterior]
                tablero_prueba = tablero_despues_de_mi.crear_copia_de_tablero()
                tablero_prueba.colocar_marca_en_posicion(marca_del_rival, indice_posicion_rival_2)
                if tablero_prueba.obtener_ganador() == marca_del_rival:
                    rival_aun_puede_ganar = True
                    break
                indice_mov_posterior += 1
                
            # Si bloqueamos la victoria del rival, sumar puntos por bloqueo
            if not rival_aun_puede_ganar:
                puntaje_total += 8 * pesos["peso_bloquear"]

        # FACTOR 3: Posiciones estratégicas del tablero
        if indice_posicion == 4:  # Centro del tablero (posición más estratégica)
            puntaje_total += pesos["peso_centro"]
        if indice_posicion in [0, 2, 6, 8]:  # Esquinas (segunda posición más estratégica)
            puntaje_total += pesos["peso_esquina"]
        if indice_posicion in [1, 3, 5, 7]:  # Lados (menos estratégicos)
            puntaje_total += pesos["peso_lado"]

        # FACTOR 4: Crear forks (situaciones donde se puede ganar de dos maneras)
        cantidad_forks_propios = self.contar_forks(tablero_simulado, mi_marca)
        if cantidad_forks_propios >= 1:
            puntaje_total += cantidad_forks_propios * pesos["peso_fork"]

        # FACTOR 5: Bloquear forks potenciales del rival
        forks_rival_antes = self.contar_forks_potenciales_del_rival(tablero, marca_del_rival)
        if forks_rival_antes >= 1:
            forks_rival_despues = self.contar_forks_potenciales_del_rival(tablero_simulado, marca_del_rival)
            # Si reducimos los forks del rival, sumar puntos por bloqueo de fork
            if forks_rival_despues < forks_rival_antes:
                puntaje_total += pesos["peso_bloquear_fork"]

        return puntaje_total

    def contar_dos_en_linea(self, tablero, marca_objetivo):
        """
        Cuenta cuántas líneas tienen exactamente 2 marcas de un jugador y 1 espacio vacío.
        
        Estas líneas representan oportunidades de victoria inmediata o amenazas
        que deben ser bloqueadas.
        
        Args:
            tablero (TableroTriqui): Estado del tablero a evaluar
            marca_objetivo (str): Marca del jugador a evaluar ('X' o 'O')
            
        Returns:
            int: Número de líneas con 2 marcas del jugador y 1 espacio vacío
        """
        total_lineas_con_dos = 0
        indice_linea = 0
        
        # Revisar cada línea ganadora posible
        while indice_linea < len(tablero.lista_lineas_ganadoras):
            linea = tablero.lista_lineas_ganadoras[indice_linea]
            valor_a = tablero.lista_celdas[linea[0]]
            valor_b = tablero.lista_celdas[linea[1]]
            valor_c = tablero.lista_celdas[linea[2]]
            
            # Contadores para analizar el contenido de la línea
            contador_de_mi_marca = 0
            contador_de_espacios = 0
            arreglo_valores = [valor_a, valor_b, valor_c]
            indice_valor = 0
            
            # Contar marcas y espacios en la línea
            while indice_valor < 3:
                celda_actual = arreglo_valores[indice_valor]
                if celda_actual == marca_objetivo:
                    contador_de_mi_marca += 1
                if celda_actual == " ":
                    contador_de_espacios += 1
                indice_valor += 1
                
            # Si hay exactamente 2 marcas propias y 1 espacio, es una oportunidad
            if contador_de_mi_marca == 2 and contador_de_espacios == 1:
                total_lineas_con_dos += 1
            indice_linea += 1
        return total_lineas_con_dos

    def contar_forks(self, tablero, marca_objetivo):
        """
        Cuenta los forks (bifurcaciones) disponibles para un jugador.
        
        Un fork es una situación donde un jugador tiene múltiples líneas
        con 2 marcas propias y 1 espacio, creando múltiples amenazas simultáneas.
        
        Args:
            tablero (TableroTriqui): Estado del tablero a evaluar
            marca_objetivo (str): Marca del jugador a evaluar
            
        Returns:
            int: Número de forks disponibles
        """
        return self.contar_dos_en_linea(tablero, marca_objetivo)

    def contar_forks_potenciales_del_rival(self, tablero, marca_del_rival):
        """
        Cuenta cuántos forks podría crear el rival en sus próximos movimientos.
        
        Simula cada movimiento posible del rival y cuenta cuántos forks
        podría generar, lo cual es útil para estrategias defensivas.
        
        Args:
            tablero (TableroTriqui): Estado actual del tablero
            marca_del_rival (str): Marca del oponente
            
        Returns:
            int: Número total de forks que el rival podría crear
        """
        lista_movimientos_disponibles = tablero.obtener_movimientos_disponibles()
        total_forks_detectados = 0
        indice_lista = 0
        
        # Simular cada movimiento posible del rival
        while indice_lista < len(lista_movimientos_disponibles):
            indice_posicion = lista_movimientos_disponibles[indice_lista]
            tablero_prueba = tablero.crear_copia_de_tablero()
            tablero_prueba.colocar_marca_en_posicion(marca_del_rival, indice_posicion)
            # Contar forks que se crearían con este movimiento
            total_forks_detectados += self.contar_forks(tablero_prueba, marca_del_rival)
            indice_lista += 1
        return total_forks_detectados
