### Proyecto Compilador

## Mini Analizador Lexico

Este proyecto implementa una versión simplificada de un analizador léxico en Python. El analizador es capaz de tokenizar una cadena de entrada y clasificar los tokens en categorías básicas.

# Características

- Reconoce identificadores y números reales.
- Proporciona una interfaz de línea de comandos para el análisis léxico interactivo.
- Muestra los resultados en una tabla formateada.

# Ejemplo

![Captura de pantalla 2024-09-09 122937](https://github.com/user-attachments/assets/6471823a-932e-4d6e-8617-14a661660c23)

## Analizador Léxico Completo

Este proyecto implementa un analizador léxico simple en Python. El analizador es capaz de tokenizar una cadena de entrada y clasificar los tokens en diferentes categorías.

# Características

- Reconoce identificadores, números (enteros y de punto flotante), operadores, palabras clave y símbolos especiales.
- Proporciona una interfaz de línea de comandos para el análisis léxico interactivo.
- Muestra los resultados en una tabla formateada.

# Ejemplo

![Captura de pantalla 2024-09-09 122723](https://github.com/user-attachments/assets/c8290065-813f-465c-a9c1-71858c246aaf)

## Analizador Léxico y Sintáctico en Python

Este proyecto implementa un **analizador léxico y sintáctico** para un lenguaje de programación simplificado, escrito en Python. El programa es una versión anterior al analizador completo, centrado en demostrar las fases iniciales del análisis léxico y sintáctico.

# Características

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
 
# Ejemplo

- **Cadena "a+b"**

<img width="369" alt="image" src="https://github.com/user-attachments/assets/876686fa-bb4d-4b70-8bf7-837565ddd0fc">

- **Cadena "a+b+c+d+e+f"**

![imagen](https://github.com/user-attachments/assets/ce9e573e-3125-4b1f-b78c-fe32db40265b)
