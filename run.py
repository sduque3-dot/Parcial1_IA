"""
Archivo principal para ejecutar el juego de Triqui con Algoritmo Genético.

Este script lanza la interfaz gráfica completa del juego donde puedes:
- Jugar contra una IA con pesos configurables
- Entrenar la IA usando algoritmos genéticos
- Ver el progreso evolutivo en tiempo real
- Comparar el rendimiento antes y después del entrenamiento

Uso:
    python run.py
"""

if __name__ == "__main__":
    # Importar y ejecutar la interfaz principal
    from ui.interfaz import main
    main()
