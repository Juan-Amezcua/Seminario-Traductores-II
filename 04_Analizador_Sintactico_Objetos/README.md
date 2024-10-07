# Analizador Léxico y Sintáctico en Python

Este proyecto implementa un **analizador léxico y sintáctico** para un lenguaje de programación simplificado, escrito en Python. El programa es una versión anterior al analizador completo, centrado en demostrar las fases iniciales del análisis léxico y sintáctico.

## Características

- **Analizador Léxico:**
  - Convierte una cadena de entrada en una secuencia de tokens.
  - Reconoce identificadores, números enteros y reales, operadores y símbolos especiales.
  - Maneja palabras clave como `int`, `float`, `void`, `if`, `while`, `return`, `else`.
  - Proporciona mensajes de error para tokens no reconocidos.

- **Analizador Sintáctico:**
  - Verifica si la secuencia de tokens cumple con una gramática simple.
  - Utiliza dos gramáticas distintas (`gramatica1` y `gramatica2`) basadas en la entrada.
    - **Gramática 1:** `E → id + id`
    - **Gramática 2:** `E → id + E | id`
  - Selecciona automáticamente la gramática adecuada según el número de operadores `+` en la entrada.

## Archivos del Proyecto

- `main.py`: Punto de entrada del programa. Solicita la cadena de entrada y ejecuta el análisis.
- `analizador_lexico.py`: Implementa el analizador léxico.
- `analizador_sintactico.py`: Implementa el analizador sintáctico.
- `categoria_token.py`: Define las categorías de tokens utilizadas durante el análisis.

## Cadena "a+b"

<img width="369" alt="image" src="https://github.com/user-attachments/assets/876686fa-bb4d-4b70-8bf7-837565ddd0fc">
