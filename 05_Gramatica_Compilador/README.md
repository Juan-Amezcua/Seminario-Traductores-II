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

- **Estructura de Archivos**
  - main.py: Punto de entrada del programa. Inicia el análisis léxico y sintáctico.
  - analizador_lexico.py: Contiene la implementación del analizador léxico.
  - analizador_sintactico.py: Contiene la implementación del analizador sintáctico.
  - categoria_token.py: Define las categorías de tokens utilizadas en el análisis.
  - compilador.lr: Archivo que contiene la tabla LR utilizada por el analizador sintáctico.
  - Documentacion: Documento que explica el diseño, las decisiones de implementación y el manejo de errores.
 
## Ejemplos input

**Cadenas correctas**

![Input 1](https://github.com/user-attachments/assets/12da8d73-81cc-41b4-8d1a-381ff1ce2cb0)

![Captura de pantalla 2024-09-30 123125](https://github.com/user-attachments/assets/94d34088-9fa9-4d96-ba2e-3e13bfb254b4)

**Cadenas incorrectas**

![Captura de pantalla 2024-09-30 123436](https://github.com/user-attachments/assets/06b8614d-2ee7-4da6-bb17-ec2190d9da84)

![Captura de pantalla 2024-09-30 123519](https://github.com/user-attachments/assets/65dd8c12-c4ce-471d-8f72-d5941db40fa7)

