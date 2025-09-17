"""
Módulo que implementa un algoritmo genético para evolucionar estrategias de juego de triqui.

El algoritmo genético utiliza selección por torneo, cruzamiento y mutación para
evolucionar una población de estrategias de juego hacia mejores rendimientos.
"""

import random
from .estrategia import EstrategiaDeJuego
from .evaluacion import evaluar_estrategia_contra_aleatorio

class AlgoritmoGenetico:
    """
    Implementación de un algoritmo genético para evolucionar estrategias de triqui.
    
    Este algoritmo mantiene una población de estrategias de juego, las evalúa
    jugando contra un oponente aleatorio, y utiliza operadores genéticos para
    evolucionar mejores estrategias a lo largo de múltiples generaciones.
    """
    
    def __init__(self, tamano_poblacion=20, total_generaciones=40, probabilidad_mutacion=0.2, cantidad_elite=2):
        """
        Inicializa el algoritmo genético con los parámetros especificados.
        
        Args:
            tamano_poblacion (int): Número de individuos en cada generación (default: 20)
            total_generaciones (int): Número total de generaciones a evolucionar (default: 40)
            probabilidad_mutacion (float): Probabilidad de mutación para cada hijo (0.0-1.0) (default: 0.2)
            cantidad_elite (int): Número de mejores individuos que pasan directamente a la siguiente generación (default: 2)
        """
        self.tamano_poblacion = tamano_poblacion  # Tamaño de la población en cada generación
        self.total_generaciones = total_generaciones  # Número total de generaciones a ejecutar
        self.probabilidad_mutacion = probabilidad_mutacion  # Probabilidad de que un individuo mute
        self.cantidad_elite = cantidad_elite  # Número de individuos élite que se preservan

        self.lista_poblacion = []  # Lista que contiene todos los individuos de la población actual
        self.mejor_estrategia_encontrada = None  # La mejor estrategia encontrada en toda la evolución
        self.mejor_aptitud_encontrada = 0.0  # La mejor aptitud (fitness) encontrada
        self.historial_de_entrenamiento = []  # Registro del progreso por generación

    def iniciar_poblacion_inicial(self):
        """
        Crea la población inicial con estrategias de juego aleatorias.
        
        Genera tantos individuos como indique tamano_poblacion, cada uno
        con pesos aleatorios para las diferentes características del juego.
        """
        self.lista_poblacion = []
        indice_individuo = 0
        # Crear individuos hasta alcanzar el tamaño de población deseado
        while indice_individuo < self.tamano_poblacion:
            self.lista_poblacion.append(EstrategiaDeJuego())  # Cada estrategia se inicializa aleatoriamente
            indice_individuo += 1

    def evaluar_poblacion_actual(self):
        """
        Evalúa la aptitud de cada individuo en la población actual.
        
        Cada estrategia juega múltiples partidas contra un oponente aleatorio
        para determinar su efectividad. También actualiza la mejor estrategia
        encontrada si se encuentra una mejor.
        """
        indice_individuo = 0
        while indice_individuo < len(self.lista_poblacion):
            estrategia_actual = self.lista_poblacion[indice_individuo]
            # Evaluar estrategia jugando 8 partidas contra oponente aleatorio
            estrategia_actual.aptitud_obtenida = evaluar_estrategia_contra_aleatorio(estrategia_actual, numero_partidas=8)
            
            # Actualizar la mejor estrategia encontrada si es necesario
            if self.mejor_estrategia_encontrada is None or estrategia_actual.aptitud_obtenida > self.mejor_aptitud_encontrada:
                self.mejor_estrategia_encontrada = estrategia_actual.clonar_estrategia()
                self.mejor_aptitud_encontrada = estrategia_actual.aptitud_obtenida
            indice_individuo += 1

    def seleccionar_progenitor_por_torneo(self):
        """
        Selecciona un progenitor utilizando selección por torneo.
        
        Escoge aleatoriamente 3 candidatos de la población y retorna
        el que tenga la mayor aptitud. Este método favorece individuos
        más aptos pero mantiene diversidad genética.
        
        Returns:
            EstrategiaDeJuego: El individuo ganador del torneo
        """
        lista_candidatos = []
        cantidad_participantes = 3  # Tamaño del torneo
        indice_candidato = 0
        
        # Seleccionar candidatos aleatorios para el torneo
        while indice_candidato < cantidad_participantes:
            lista_candidatos.append(random.choice(self.lista_poblacion))
            indice_candidato += 1
            
        # Encontrar el candidato con mayor aptitud
        mejor_candidato = lista_candidatos[0]
        indice_candidato = 1
        while indice_candidato < len(lista_candidatos):
            if lista_candidatos[indice_candidato].aptitud_obtenida > mejor_candidato.aptitud_obtenida:
                mejor_candidato = lista_candidatos[indice_candidato]
            indice_candidato += 1
        return mejor_candidato

    def construir_siguiente_generacion(self):
        """
        Construye la siguiente generación utilizando elitismo, cruzamiento y mutación.
        
        - Preserva los mejores individuos (elitismo)
        - Genera nuevos individuos mediante cruzamiento de progenitores seleccionados por torneo
        - Aplica mutación a los hijos generados
        """
        # Ordenar población por aptitud (mayor a menor)
        poblacion_ordenada = sorted(self.lista_poblacion, key=lambda e: e.aptitud_obtenida, reverse=True)

        nueva_poblacion = []
        indice_elite = 0
        
        # Preservar individuos élite (los mejores pasan directamente)
        while indice_elite < self.cantidad_elite and indice_elite < len(poblacion_ordenada):
            nueva_poblacion.append(poblacion_ordenada[indice_elite].clonar_estrategia())
            indice_elite += 1

        # Generar el resto de la población mediante cruzamiento y mutación
        while len(nueva_poblacion) < self.tamano_poblacion:
            # Seleccionar dos progenitores mediante torneo
            progenitor_a = self.seleccionar_progenitor_por_torneo()
            progenitor_b = self.seleccionar_progenitor_por_torneo()
            
            # Crear hijo mediante cruzamiento
            hijo_generado = progenitor_a.cruzar_con_estrategia(progenitor_b)
            
            # Aplicar mutación con amplitud de cambio de 3
            hijo_generado.mutar_estrategia(probabilidad_mutacion=self.probabilidad_mutacion, amplitud_cambio=3)
            nueva_poblacion.append(hijo_generado)

        self.lista_poblacion = nueva_poblacion

    def ejecutar_entrenamiento(self, callback_progreso=None, callback_permitir_eventos=None):
        """
        Ejecuta el algoritmo genético completo durante todas las generaciones.
        
        Args:
            callback_progreso (function, optional): Función que se llama después de cada generación
                para reportar progreso. Recibe (generacion, mejor_aptitud, aptitud_promedio, mejores_pesos)
            callback_permitir_eventos (function, optional): Función que se llama al inicio de cada
                generación para permitir el procesamiento de eventos de la interfaz gráfica
        """
        # Crear población inicial aleatoria
        self.iniciar_poblacion_inicial()

        generacion_actual = 0
        while generacion_actual < self.total_generaciones:
            # Permitir procesamiento de eventos de la GUI si se proporciona callback
            if callback_permitir_eventos is not None:
                callback_permitir_eventos()

            # Evaluar aptitud de todos los individuos en la población actual
            self.evaluar_poblacion_actual()

            # Calcular aptitud promedio de la generación actual
            suma_aptitudes = 0.0
            indice_individuo = 0
            while indice_individuo < len(self.lista_poblacion):
                suma_aptitudes += self.lista_poblacion[indice_individuo].aptitud_obtenida
                indice_individuo += 1
            aptitud_promedio = suma_aptitudes / float(len(self.lista_poblacion))

            # Registrar estadísticas de esta generación en el historial
            self.historial_de_entrenamiento.append({
                "generacion": generacion_actual + 1,
                "mejor": self.mejor_aptitud_encontrada,
                "promedio": aptitud_promedio
            })

            # Reportar progreso si se proporciona callback
            if callback_progreso is not None:
                callback_progreso(
                    generacion_actual + 1,
                    self.mejor_aptitud_encontrada,
                    aptitud_promedio,
                    self.mejor_estrategia_encontrada.diccionario_pesos
                )

            # Generar siguiente generación (excepto en la última iteración)
            if generacion_actual < self.total_generaciones - 1:
                self.construir_siguiente_generacion()

            generacion_actual += 1
