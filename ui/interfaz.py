"""
Interfaz gráfica principal para el juego de Triqui con Algoritmo Genético.

Implementa una ventana de juego completa con controles para entrenar la IA
y jugar partidas contra una estrategia evolutiva.
"""

import sys
import time

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel,
    QGridLayout, QVBoxLayout, QHBoxLayout, QGroupBox, QSpinBox,
    QTextEdit, QProgressBar, QMessageBox, QComboBox
)

from PyQt6.QtGui import QIcon

# Importar desde el directorio padre
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logica.tablero import TableroTriqui
from logica.ia import IAConPesos
from logica.algoritmo_genetico.individuo import EstrategiaDeJuego
from logica.algoritmo_genetico.motor_ag import AlgoritmoGenetico

class VentanaDeJuego(QMainWindow):
    """
    Ventana principal del juego de Triqui con entrenamiento de IA.
    
    Proporciona una interfaz completa que incluye:
    - Tablero de juego interactivo
    - Panel de estadísticas
    - Controles de entrenamiento del algoritmo genético
    - Visualización del progreso evolutivo
    """
    
    def __init__(self):
        """
        Inicializa la ventana principal y todos sus componentes.
        
        Configura el modelo de juego, la IA inicial, y construye
        la interfaz gráfica completa.
        """
        super().__init__()
        self.setWindowTitle("Triqui con el Algoritmo Genético")
        
        # Agregar icono de la ventana
        self.setWindowIcon(QIcon("ui/img/UTP.png"))
        
        # Color de fondo de toda la ventana
        self.setStyleSheet("background-color: #2d313f;")

        # Modelo de juego
        self.tablero_de_juego = TableroTriqui()
        self.marca_humana = "X"
        self.marca_de_la_computadora = "O"

        # Estrategia inicial y IA
        self.estrategia_actual = EstrategiaDeJuego({
            "peso_ganar": 9, "peso_bloquear": 9, "peso_centro": 5, "peso_esquina": 3,
            "peso_lado": 1, "peso_fork": 4, "peso_bloquear_fork": 3
        })
        self.ia_con_pesos = IAConPesos(self.estrategia_actual)

        # Estadísticas básicas
        self.estadisticas_juego = {"humano": 0, "computadora": 0, "empates": 0}

        # Definir estilos consistentes para las celdas
        self._definir_estilos_celdas()

        # Construcción de la interfaz
        self._construir_interfaz()
        self._reiniciar_interfaz_tablero()

    def _definir_estilos_celdas(self):
        """
        Define los estilos CSS consistentes para las diferentes estados de las celdas.
        """
        self.ESTILO_CELDA_VACIA = """
            QPushButton {
                font-size: 35px; 
                font-weight: bold; 
                background-color: #ffffff; 
                border: 2px solid #cccccc; 
                border-radius: 8px;
                color: #666666;
            }
            QPushButton:hover {
                background-color: #f8f9fa;
                border-color: #dc3545;
            }
            QPushButton:pressed {
                background-color: #e9ecef;
            }
        """
        
        self.ESTILO_CELDA_X = """
            QPushButton {
                font-size: 34px; 
                font-weight: bold; 
                color: #dc3545; 
                background-color: #fff5f5; 
                border: 2px solid #dc3545; 
                border-radius: 8px;
            }
        """
        
        self.ESTILO_CELDA_O = """
            QPushButton {
                font-size: 34px; 
                font-weight: bold; 
                color: #007bff; 
                background-color: #f8f9ff; 
                border: 2px solid #007bff; 
                border-radius: 8px;
            }
        """

    # ----------------- Construcción de la GUI -----------------

    def _construir_interfaz(self):
        """
        Construye todos los elementos de la interfaz gráfica.
        
        Crea el layout principal con el tablero de juego a la izquierda
        y el panel de controles a la derecha.
        """
        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        layout_principal = QHBoxLayout()
        widget_central.setLayout(layout_principal)

        # Sección de tablero
        grupo_tablero = QGroupBox("Tablero")
        layout_rejilla_tablero = QGridLayout()
        
        # Ajustar espaciado y márgenes
        layout_rejilla_tablero.setSpacing(12)  # Separación entre celdas
        layout_rejilla_tablero.setContentsMargins(28, 28, 28, 28)  # Margen alrededor del grid
        
        grupo_tablero.setLayout(layout_rejilla_tablero)

        self.lista_botones_celda = []
        indice = 0
        while indice < 9:
            boton_celda = QPushButton(" ")
            boton_celda.setFixedSize(115, 115)
            boton_celda.setStyleSheet(self.ESTILO_CELDA_VACIA)
            boton_celda.clicked.connect(self._crear_manejador_click_celda(indice))
            self.lista_botones_celda.append(boton_celda)
            fila = int(indice / 3)
            columna = indice % 3
            layout_rejilla_tablero.addWidget(boton_celda, fila, columna)
            indice += 1

        # Panel lateral derecho
        layout_panel_derecho = QVBoxLayout()

        # Controles básicos
        grupo_controles = QGroupBox("Controles de Juego")
        layout_controles = QVBoxLayout()
        grupo_controles.setLayout(layout_controles)

        self.lista_opciones_quien_inicia = QComboBox()
        self.lista_opciones_quien_inicia.addItems(["Humano (X) primero", "Computadora (O) primero"])
        layout_controles.addWidget(self.lista_opciones_quien_inicia)

        boton_nuevo_juego = QPushButton("Nuevo juego")
        boton_nuevo_juego.clicked.connect(self.on_clic_nuevo_juego)
        layout_controles.addWidget(boton_nuevo_juego)

        self.etiqueta_estado = QLabel("Estado: listo")
        self.etiqueta_estadisticas = QLabel("Estadísticas - Humano: 0 | Computadora: 0 | Empates: 0")
        layout_controles.addWidget(self.etiqueta_estado)
        layout_controles.addWidget(self.etiqueta_estadisticas)

        # Panel de Entrenamiento GA
        grupo_entrenamiento = QGroupBox("Entrenamiento Algoritmo Genético")
        layout_entrenamiento = QVBoxLayout()
        grupo_entrenamiento.setLayout(layout_entrenamiento)

        fila_1 = QHBoxLayout()
        fila_1.addWidget(QLabel("Tamaño de población:"))
        self.campo_poblacion = QSpinBox()
        self.campo_poblacion.setRange(4, 200)
        self.campo_poblacion.setValue(80)  
        fila_1.addWidget(self.campo_poblacion)

        fila_1.addWidget(QLabel("Número de generaciones:"))
        self.campo_generaciones = QSpinBox()
        self.campo_generaciones.setRange(1, 200)
        self.campo_generaciones.setValue(150)  
        fila_1.addWidget(self.campo_generaciones)
        layout_entrenamiento.addLayout(fila_1)

        fila_2 = QHBoxLayout()
        fila_2.addWidget(QLabel("Mutación (%):"))
        self.campo_mutacion = QSpinBox()
        self.campo_mutacion.setRange(0, 100)
        self.campo_mutacion.setValue(10) 
        fila_2.addWidget(self.campo_mutacion)

        fila_2.addWidget(QLabel("Élite:"))
        self.campo_elite = QSpinBox()
        self.campo_elite.setRange(0, 20)
        self.campo_elite.setValue(12)  
        fila_2.addWidget(self.campo_elite)
        layout_entrenamiento.addLayout(fila_2)

        boton_entrenar = QPushButton("Entrenar GA")
        boton_entrenar.clicked.connect(self.on_clic_entrenar_ga)
        layout_entrenamiento.addWidget(boton_entrenar)

        self.barra_progreso_entrenamiento = QProgressBar()
        layout_entrenamiento.addWidget(self.barra_progreso_entrenamiento)

        self.caja_texto_mejor = QTextEdit()
        self.caja_texto_mejor.setReadOnly(True)
        self.caja_texto_mejor.setPlaceholderText("Aquí verás el mejor fitness y los pesos aprendidos...")
        layout_entrenamiento.addWidget(self.caja_texto_mejor)

        layout_panel_derecho.addWidget(grupo_controles)
        layout_panel_derecho.addWidget(grupo_entrenamiento)
        layout_panel_derecho.addStretch()

        layout_principal.addWidget(grupo_tablero, stretch=3)
        layout_principal.addLayout(layout_panel_derecho, stretch=3)

    def _crear_manejador_click_celda(self, indice_posicion):
        """
        Crea un manejador de eventos para el click en una celda específica.
        
        Args:
            indice_posicion (int): Índice de la celda (0-8)
            
        Returns:
            function: Función manejadora del evento click
        """
        def manejador():
            self.on_clic_celda(indice_posicion)
        return manejador

    def _reiniciar_interfaz_tablero(self):
        """
        Reinicia la interfaz del tablero a su estado inicial.
        
        Limpia todas las celdas y restablece los controles
        para comenzar una nueva partida.
        """
        self.tablero_de_juego.reiniciar_tablero()
        indice = 0
        while indice < 9:
            self.lista_botones_celda[indice].setText(" ")
            self.lista_botones_celda[indice].setStyleSheet(self.ESTILO_CELDA_VACIA)
            self.lista_botones_celda[indice].setEnabled(True)
            indice += 1
        self.etiqueta_estado.setText("Estado: turno del jugador humano (X)")
        self.marca_humana = "X"
        self.marca_de_la_computadora = "O"

    # ----------------- Interacción de juego -----------------

    def on_clic_nuevo_juego(self):
        """
        Maneja el evento de iniciar un nuevo juego.
        
        Reinicia el tablero y determina quién debe jugar primero
        según la selección del usuario.
        """
        self._reiniciar_interfaz_tablero()
        opcion = self.lista_opciones_quien_inicia.currentText()
        if "Computadora" in opcion:
            self.etiqueta_estado.setText("Estado: turno de la computadora")
            self._turno_de_la_computadora()
        else:
            self.etiqueta_estado.setText("Estado: turno del jugador humano (X)")

    def on_clic_celda(self, indice_posicion):
        """
        Maneja el click del jugador humano en una celda del tablero.
        
        Args:
            indice_posicion (int): Índice de la celda clickeada (0-8)
        """
        # Verificar que la celda esté vacía
        if self.tablero_de_juego.lista_celdas[indice_posicion] != " ":
            return
            
        # Humano juega "X"
        self.tablero_de_juego.colocar_marca_en_posicion("X", indice_posicion)
        self.lista_botones_celda[indice_posicion].setText("X")
        self.lista_botones_celda[indice_posicion].setStyleSheet(self.ESTILO_CELDA_X)
        self.lista_botones_celda[indice_posicion].setEnabled(False)

        # Verificar si el juego terminó
        resultado = self.tablero_de_juego.obtener_ganador()
        if resultado is not None:
            self._finalizar_partida(resultado)
            return

        # Turno de la computadora
        self.etiqueta_estado.setText("Estado: turno de la computadora")
        self._turno_de_la_computadora()

    def _turno_de_la_computadora(self):
        """
        Ejecuta el turno de la computadora.
        
        La IA elige su movimiento y actualiza el tablero.
        Verifica si el juego termina después del movimiento.
        """
        movimiento = self.ia_con_pesos.elegir_movimiento(self.tablero_de_juego, "O")
        if movimiento == -1:
            self._finalizar_partida("D")
            return

        self.tablero_de_juego.colocar_marca_en_posicion("O", movimiento)
        self.lista_botones_celda[movimiento].setText("O")
        self.lista_botones_celda[movimiento].setStyleSheet(self.ESTILO_CELDA_O)
        self.lista_botones_celda[movimiento].setEnabled(False)

        resultado = self.tablero_de_juego.obtener_ganador()
        if resultado is not None:
            self._finalizar_partida(resultado)
            return

        self.etiqueta_estado.setText("Estado: turno del jugador humano (X)")

    def _finalizar_partida(self, marca_ganadora):
        """
        Finaliza la partida actual y actualiza las estadísticas.
        
        Args:
            marca_ganadora (str): 'X', 'O', o 'D' para empate
        """
        # Deshabilitar todas las celdas
        indice = 0
        while indice < 9:
            self.lista_botones_celda[indice].setEnabled(False)
            indice += 1

        # Actualizar estadísticas y mostrar resultado
        if marca_ganadora == "X":
            self.estadisticas_juego["humano"] += 1
            self.etiqueta_estado.setText("¡Ganaste!")
        elif marca_ganadora == "O":
            self.estadisticas_juego["computadora"] += 1
            self.etiqueta_estado.setText("La computadora ganó.")
        else:
            self.estadisticas_juego["empates"] += 1
            self.etiqueta_estado.setText("Empate.")

        self._actualizar_etiqueta_estadisticas()

    def _actualizar_etiqueta_estadisticas(self):
        """
        Actualiza la etiqueta de estadísticas con los conteos actuales.
        """
        texto = "Estadísticas - Humano: " + str(self.estadisticas_juego["humano"])
        texto += " | Computadora: " + str(self.estadisticas_juego["computadora"])
        texto += " | Empates: " + str(self.estadisticas_juego["empates"])
        self.etiqueta_estadisticas.setText(texto)

    # ----------------- Entrenamiento GA -----------------

    def on_clic_entrenar_ga(self):
        """
        Inicia el proceso de entrenamiento del algoritmo genético.
        
        Configura los parámetros según los valores de la interfaz,
        ejecuta el entrenamiento y actualiza la IA con la mejor estrategia encontrada.
        """
        # Obtener parámetros de la interfaz
        tamano_poblacion = self.campo_poblacion.value()
        numero_generaciones = self.campo_generaciones.value()
        prob_mutacion = self.campo_mutacion.value() / 100.0
        cantidad_elite = self.campo_elite.value()

        # Crear y configurar el algoritmo genético
        ga = AlgoritmoGenetico(
            tamano_poblacion=tamano_poblacion,
            total_generaciones=numero_generaciones,
            probabilidad_mutacion=prob_mutacion,
            cantidad_elite=cantidad_elite
        )

        # Configurar interfaz para mostrar progreso
        self.barra_progreso_entrenamiento.setRange(0, numero_generaciones)
        self.barra_progreso_entrenamiento.setValue(0)
        self.caja_texto_mejor.clear()

        def callback_progreso(generacion, mejor_fit, fit_prom, pesos_mejor):
            """Callback para actualizar la interfaz durante el entrenamiento."""
            self.barra_progreso_entrenamiento.setValue(generacion)
            texto = ""
            texto += "Generación: " + str(generacion) + "\n"
            texto += "Mejor fitness: " + str(mejor_fit) + "\n"
            texto += "Fitness promedio: " + str(round(fit_prom, 2)) + "\n"
            texto += "Pesos del mejor individuo:\n"
            for clave in pesos_mejor:
                texto += "  - " + clave + ": " + str(pesos_mejor[clave]) + "\n"
            self.caja_texto_mejor.setPlainText(texto)

        def callback_permitir_eventos():
            """Callback para mantener la interfaz fluida durante el entrenamiento."""
            QApplication.processEvents()

        # Ejecutar entrenamiento
        inicio = time.time()
        ga.ejecutar_entrenamiento(callback_progreso=callback_progreso,
                                  callback_permitir_eventos=callback_permitir_eventos)
        fin = time.time()

        # Actualizar la IA con la estrategia aprendida
        self.estrategia_actual = ga.mejor_estrategia_encontrada.clonar_estrategia()
        self.ia_con_pesos = IAConPesos(self.estrategia_actual)

        # Mostrar resumen final
        resumen = self.caja_texto_mejor.toPlainText()
        resumen += "\nEntrenamiento terminado en " + str(round(fin - inicio, 2)) + " s.\n"
        resumen += "La estrategia final ha sido aplicada a la computadora.\n"
        self.caja_texto_mejor.setPlainText(resumen)

        QMessageBox.information(
            self, "GA finalizado",
            "Entrenamiento completado.\n"
            "Se actualizaron los pesos de la IA.\n\n"
            "Ahora juega contra la computadora para ver el cambio."
        )


def main():
    """
    Función principal para ejecutar la aplicación.
    
    Crea la aplicación PyQt6, inicializa la ventana principal
    y ejecuta el bucle de eventos.
    """
    app = QApplication(sys.argv)
    ventana = VentanaDeJuego()
    ventana.resize(900, 480)
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()