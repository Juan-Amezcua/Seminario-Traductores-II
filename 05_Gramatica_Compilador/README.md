# Analizador Léxico y Sintáctico en Python

Este proyecto implementa un **analizador léxico y sintáctico** para un lenguaje de programación simplificado, escrito en Python. El analizador léxico tokeniza una cadena de entrada, mientras que el analizador sintáctico verifica la estructura gramatical utilizando una tabla LR.

## Características

- **Analizador Léxico:**
  - Identifica correctamente todos los tokens definidos en la especificación del lenguaje, incluyendo identificadores, números, operadores y palabras reservadas.
  - Maneja errores léxicos proporcionando mensajes claros y precisos para entradas inválidas.

- **Analizador Sintáctico:**
  - Verifica si la secuencia de tokens cumple con la gramática del lenguaje.
  - Utiliza una tabla LR (`compilador.lr`) para el análisis sintáctico.
  - Proporciona mensajes de error útiles en caso de encontrar inconsistencias sintácticas.
