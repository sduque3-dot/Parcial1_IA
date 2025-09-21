"""
Motor principal del algoritmo genético para evolucionar estrategias de Triqui.

Este módulo implementa la clase AlgoritmoGenetico que coordina todo el proceso
evolutivo: población, selección por torneo, cruzamiento uniforme, mutación
gaussiana y elitismo para evolucionar estrategias de juego hacia mejores rendimientos.
"""

import random
from ..algoritmo_genetico.individuo import EstrategiaDeJuego
from .fitness import evaluar_estrategia_contra_aleatorio

class AlgoritmoGenetico:
    """
    Motor principal del algoritmo genético para evolucionar estrategias de Triqui.
    
    Este algoritmo mantiene una población de individuos (estrategias de juego),
    los evalúa usando una función de fitness, y utiliza operadores genéticos
    para evolucionar mejores estrategias a lo largo de múltiples generaciones.
    
    Operadores evolutivos implementados:
    - Selección: Torneo de 3 individuos
    - Cruzamiento: Uniforme (50% probabilidad por gen)  
    - Mutación: Gaussiana acotada (±3 puntos, límites 0-10)
    - Reemplazo: Elitismo + Reemplazo generacional
    """
    
    def __init__(self, tamano_poblacion=80, total_generaciones=150, probabilidad_mutacion=0.1, cantidad_elite=12):
        """
        Inicializa el motor del algoritmo genético con los parámetros especificados.
        
        Args:
            tamano_poblacion (int): Número de individuos en cada generación (default: 20)
            total_generaciones (int): Número total de generaciones a evolucionar (default: 40)
            probabilidad_mutacion (float): Probabilidad de mutación para cada descendiente (0.0-1.0) (default: 0.2)
            cantidad_elite (int): Número de mejores individuos que pasan directamente a la siguiente generación (default: 2)
        """
        self.tamano_poblacion = tamano_poblacion  # Tamaño de la población en cada generación
        self.total_generaciones = total_generaciones  # Número total de generaciones a ejecutar
        self.probabilidad_mutacion = probabilidad_mutacion  # Probabilidad de que un individuo mute
        self.cantidad_elite = cantidad_elite  # Número de individuos élite que se preservan

        self.lista_poblacion = []  # Lista que contiene todos los individuos de la población actual
        self.mejor_estrategia_encontrada = None  # El mejor individuo encontrado en toda la evolución
        self.mejor_aptitud_encontrada = 0.0  # La mejor aptitud (fitness) encontrada
        self.historial_de_entrenamiento = []  # Registro del progreso evolutivo por generación

    def iniciar_poblacion_inicial(self):
        """
        Crea la población inicial con individuos aleatorios.
        
        Genera tantos individuos como indique tamano_poblacion, cada uno
        con genes (pesos) aleatorios para las diferentes características del juego.
        Esta población inicial proporciona diversidad genética para la evolución.
        """
        self.lista_poblacion = []
        indice_individuo = 0
        # Crear individuos hasta alcanzar el tamaño de población deseado
        while indice_individuo < self.tamano_poblacion:
            self.lista_poblacion.append(EstrategiaDeJuego())  # Cada individuo se inicializa aleatoriamente
            indice_individuo += 1

    def evaluar_poblacion_actual(self):
        """
        Evalúa la aptitud (fitness) de cada individuo en la población actual.
        
        Cada individuo juega múltiples partidas contra un oponente aleatorio
        para determinar su efectividad. También actualiza el mejor individuo
        encontrado si se encuentra uno superior (hall of fame).
        """
        indice_individuo = 0
        while indice_individuo < len(self.lista_poblacion):
            individuo_actual = self.lista_poblacion[indice_individuo]
            # Evaluar fitness del individuo jugando partidas contra oponente aleatorio
            individuo_actual.aptitud_obtenida = evaluar_estrategia_contra_aleatorio(individuo_actual, numero_partidas=8)
            
            # Actualizar el hall of fame si es necesario
            if self.mejor_estrategia_encontrada is None or individuo_actual.aptitud_obtenida > self.mejor_aptitud_encontrada:
                self.mejor_estrategia_encontrada = individuo_actual.clonar_estrategia()
                self.mejor_aptitud_encontrada = individuo_actual.aptitud_obtenida
            indice_individuo += 1

    def seleccionar_progenitor_por_torneo(self):
        """
        Operador de selección: selecciona un progenitor utilizando selección por torneo.
        
        Escoge aleatoriamente 3 candidatos de la población y retorna
        el que tenga la mayor aptitud. Este método favorece individuos
        más aptos pero mantiene diversidad genética al incluir aleatoriedad.
        
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
            
        # Encontrar el candidato con mayor aptitud (fitness)
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
        
        Proceso evolutivo:
        1. Preserva los mejores individuos (elitismo)
        2. Genera nuevos individuos mediante cruzamiento de progenitores seleccionados por torneo
        3. Aplica mutación a los descendientes generados
        4. Reemplaza la población anterior con la nueva generación
        """
        # Ordenar población por aptitud (mayor a menor) para elitismo
        poblacion_ordenada = sorted(self.lista_poblacion, key=lambda e: e.aptitud_obtenida, reverse=True)

        nueva_poblacion = []
        indice_elite = 0
        
        # ELITISMO: Preservar individuos élite (los mejores pasan directamente)
        while indice_elite < self.cantidad_elite and indice_elite < len(poblacion_ordenada):
            nueva_poblacion.append(poblacion_ordenada[indice_elite].clonar_estrategia())
            indice_elite += 1

        # REPRODUCCIÓN: Generar el resto de la población mediante cruzamiento y mutación
        while len(nueva_poblacion) < self.tamano_poblacion:
            # Seleccionar dos progenitores mediante torneo
            progenitor_a = self.seleccionar_progenitor_por_torneo()
            progenitor_b = self.seleccionar_progenitor_por_torneo()
            
            # Crear descendiente mediante cruzamiento uniforme
            hijo_generado = progenitor_a.cruzar_con_estrategia(progenitor_b)
            
            # Aplicar mutación con amplitud de cambio de 3
            hijo_generado.mutar_estrategia(probabilidad_mutacion=self.probabilidad_mutacion, amplitud_cambio=3)
            nueva_poblacion.append(hijo_generado)

        # Reemplazar población anterior con la nueva generación
        self.lista_poblacion = nueva_poblacion

    def ejecutar_entrenamiento(self, callback_progreso=None, callback_permitir_eventos=None):
        """
        Ejecuta el algoritmo genético completo durante todas las generaciones.
        
        Ciclo evolutivo principal:
        1. Inicializar población aleatoria
        2. Para cada generación:
           a. Evaluar fitness de todos los individuos
           b. Registrar estadísticas de la generación
           c. Crear siguiente generación (excepto en la última)
        3. Retornar el mejor individuo encontrado
        
        Args:
            callback_progreso (function, optional): Función que se llama después de cada generación
                para reportar progreso. Recibe (generacion, mejor_aptitud, aptitud_promedio, mejores_pesos)
            callback_permitir_eventos (function, optional): Función que se llama al inicio de cada
                generación para permitir el procesamiento de eventos de la interfaz gráfica
        """
        # INICIALIZACIÓN: Crear población inicial aleatoria
        self.iniciar_poblacion_inicial()

        generacion_actual = 0
        while generacion_actual < self.total_generaciones:
            # Permitir procesamiento de eventos de la GUI si se proporciona callback
            if callback_permitir_eventos is not None:
                callback_permitir_eventos()

            # EVALUACIÓN: Calcular fitness de todos los individuos en la población actual
            self.evaluar_poblacion_actual()

            # ESTADÍSTICAS: Calcular aptitud promedio de la generación actual
            suma_aptitudes = 0.0
            indice_individuo = 0
            while indice_individuo < len(self.lista_poblacion):
                suma_aptitudes += self.lista_poblacion[indice_individuo].aptitud_obtenida
                indice_individuo += 1
            aptitud_promedio = suma_aptitudes / float(len(self.lista_poblacion))

            # REGISTRO: Guardar estadísticas de esta generación en el historial
            self.historial_de_entrenamiento.append({
                "generacion": generacion_actual + 1,
                "mejor": self.mejor_aptitud_encontrada,
                "promedio": aptitud_promedio
            })

            # REPORTE: Informar progreso si se proporciona callback
            if callback_progreso is not None:
                callback_progreso(
                    generacion_actual + 1,
                    self.mejor_aptitud_encontrada,
                    aptitud_promedio,
                    self.mejor_estrategia_encontrada.diccionario_pesos
                )

            # EVOLUCIÓN: Generar siguiente generación (excepto en la última iteración)
            if generacion_actual < self.total_generaciones - 1:
                self.construir_siguiente_generacion()

            generacion_actual += 1
