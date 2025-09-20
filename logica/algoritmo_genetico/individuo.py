"""
Módulo que define los individuos del algoritmo genético.

Contiene la clase EstrategiaDeJuego que representa un individuo (cromosoma)
en el algoritmo genético. Cada individuo encapsula los pesos utilizados
por la IA para evaluar movimientos, junto con operadores genéticos
para evolucionar estas estrategias.
"""

import random

class EstrategiaDeJuego:
    """
    Representa un individuo del algoritmo genético (estrategia de juego).
    
    Cada individuo contiene un cromosoma definido por pesos enteros (0-10)
    que determinan la importancia relativa de diferentes aspectos del juego.
    Estos pesos son utilizados por la IA para evaluar y seleccionar movimientos.
    
    Los genes (pesos) incluyen:
    - peso_ganar: Importancia de movimientos que ganan inmediatamente
    - peso_bloquear: Importancia de bloquear victorias del oponente  
    - peso_centro: Valor del control del centro del tablero
    - peso_esquina: Valor de ocupar las esquinas
    - peso_lado: Valor de ocupar los lados
    - peso_fork: Importancia de crear forks (múltiples amenazas)
    - peso_bloquear_fork: Importancia de bloquear forks del oponente
    """
    
    def __init__(self, diccionario_pesos=None):
        """
        Inicializa un individuo con pesos específicos o aleatorios.
        
        Args:
            diccionario_pesos (dict, optional): Diccionario con pesos predefinidos.
                                               Si es None, se generan pesos aleatorios.
        
        Note:
            Los pesos se mantienen en el rango [0, 10] donde:
            - 0 significa que el factor no es considerado
            - 10 significa máxima importancia para ese factor
        """
        if diccionario_pesos is None:
            # Generar pesos aleatorios para un nuevo individuo
            self.diccionario_pesos = {
                "peso_ganar": random.randint(5, 10),        # Ganar siempre debe ser importante
                "peso_bloquear": random.randint(5, 10),     # Bloquear también es crítico
                "peso_centro": random.randint(0, 10),       # Control del centro variable
                "peso_esquina": random.randint(0, 10),      # Importancia de esquinas variable
                "peso_lado": random.randint(0, 10),         # Importancia de lados variable
                "peso_fork": random.randint(0, 10),         # Crear forks variable
                "peso_bloquear_fork": random.randint(0, 10) # Bloquear forks variable
            }
        else:
            # Usar pesos proporcionados, asegurando que sean enteros
            self.diccionario_pesos = {}
            for clave_peso in diccionario_pesos:
                self.diccionario_pesos[clave_peso] = int(diccionario_pesos[clave_peso])
                
        self.aptitud_obtenida = 0.0  # Fitness del individuo (se calcula durante evaluación)

    def clonar_estrategia(self):
        """
        Crea una copia exacta de este individuo.
        
        Útil para preservar individuos exitosos durante la evolución
        genética (elitismo) o para crear copias de trabajo.
        
        Returns:
            EstrategiaDeJuego: Nueva instancia con los mismos pesos
        """
        return EstrategiaDeJuego(self.diccionario_pesos)

    def mutar_estrategia(self, probabilidad_mutacion=0.2, amplitud_cambio=3):
        """
        Aplica operador de mutación genética a los genes del individuo.
        
        Cada gen (peso) tiene una probabilidad de ser modificado por un valor
        aleatorio dentro de la amplitud especificada. Las mutaciones
        ayudan a explorar nuevas regiones del espacio de soluciones.
        
        Args:
            probabilidad_mutacion (float): Probabilidad (0.0-1.0) de que cada gen mute
            amplitud_cambio (int): Máximo cambio absoluto que puede aplicarse a un gen
        
        Note:
            Los genes se mantienen dentro del rango [0, 10] después de la mutación.
        """
        for clave_peso in self.diccionario_pesos:
            # Determinar si este gen específico debe mutar
            if random.random() < probabilidad_mutacion:
                # Generar variación aleatoria dentro de la amplitud
                variacion = random.randint(-amplitud_cambio, amplitud_cambio)
                nuevo_valor = self.diccionario_pesos[clave_peso] + variacion
                
                # Mantener el valor dentro de los límites válidos [0, 10]
                if nuevo_valor < 0:
                    nuevo_valor = 0
                if nuevo_valor > 10:
                    nuevo_valor = 10
                    
                self.diccionario_pesos[clave_peso] = nuevo_valor

    def cruzar_con_estrategia(self, otra_estrategia):
        """
        Crea un individuo hijo mediante operador de cruzamiento genético.
        
        Utiliza cruzamiento uniforme: para cada gen, elige aleatoriamente
        si heredarlo de este padre o del otro padre. Esto combina características
        de ambos individuos parentales.
        
        Args:
            otra_estrategia (EstrategiaDeJuego): El otro individuo parental
            
        Returns:
            EstrategiaDeJuego: Nuevo individuo que combina genes de ambos padres
        
        Note:
            El cruzamiento es simétrico: el orden de los padres no afecta
            la distribución probabilística de los genes heredados.
        """
        pesos_hijo = {}
        
        # Para cada gen, elegir aleatoriamente de cuál padre heredar
        for clave_peso in self.diccionario_pesos:
            if random.random() < 0.5:
                # Heredar gen del primer padre (self)
                pesos_hijo[clave_peso] = self.diccionario_pesos[clave_peso]
            else:
                # Heredar gen del segundo padre (otra_estrategia)
                pesos_hijo[clave_peso] = otra_estrategia.diccionario_pesos[clave_peso]
                
        return EstrategiaDeJuego(pesos_hijo)
