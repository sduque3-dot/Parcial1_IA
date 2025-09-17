"""
Módulo que simula partidas completas de triqui entre dos jugadores.

Contiene funciones para ejecutar juegos automáticos entre diferentes
tipos de jugadores (IA, oponentes aleatorios, etc.) y determinar
el resultado final.
"""

def jugar_partida_en_tablero(tablero, jugador_X, jugador_O, marca_que_inicia="X"):
    """
    Simula una partida completa de triqui entre dos jugadores.
    
    Ejecuta el juego turno por turno, permitiendo que cada jugador
    elija su movimiento según su estrategia, hasta que se determine
    un ganador o se produzca un empate.
    
    Args:
        tablero (TableroTriqui): Instancia del tablero donde se jugará la partida
        jugador_X (object): Jugador que usará la marca 'X' (debe tener método elegir_movimiento)
        jugador_O (object): Jugador que usará la marca 'O' (debe tener método elegir_movimiento)
        marca_que_inicia (str, optional): Marca del jugador que inicia ('X' por defecto)
    
    Returns:
        str: Resultado de la partida:
            - 'X' si gana el jugador X
            - 'O' si gana el jugador O
            - 'D' si hay empate
    
    Note:
        Los objetos jugador_X y jugador_O deben implementar el método:
        elegir_movimiento(tablero, mi_marca) -> int
    """
    # Reiniciar el tablero para comenzar una partida limpia
    tablero.reiniciar_tablero()
    marca_del_turno = marca_que_inicia  # Marca del jugador actual
    
    # Bucle principal del juego - continúa hasta que hay un resultado
    while True:
        if marca_del_turno == "X":
            # Turno del jugador X
            movimiento_seleccionado = jugador_X.elegir_movimiento(tablero, "X")
            # Si el jugador no puede mover (error), declarar empate
            if movimiento_seleccionado == -1:
                return "D"
            # Ejecutar el movimiento en el tablero
            tablero.colocar_marca_en_posicion("X", movimiento_seleccionado)
        else:
            # Turno del jugador O
            movimiento_seleccionado = jugador_O.elegir_movimiento(tablero, "O")
            # Si el jugador no puede mover (error), declarar empate
            if movimiento_seleccionado == -1:
                return "D"
            # Ejecutar el movimiento en el tablero
            tablero.colocar_marca_en_posicion("O", movimiento_seleccionado)
            
        # Verificar si el juego ha terminado (ganador o empate)
        resultado_actual = tablero.obtener_ganador()
        if resultado_actual is not None:
            return resultado_actual  # Retornar el resultado final
            
        # Cambiar turno al otro jugador
        marca_del_turno = "O" if marca_del_turno == "X" else "X"
