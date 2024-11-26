# Analizador Sintáctico Completo

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

**Cadena: int x ;**

![Captura de pantalla 2024-11-26 023553](https://github.com/user-attachments/assets/360ff8d5-7a9a-4fab-93f1-34b7c6aed5f2)

**Cadena: 
int x ;
float y;**

![Captura de pantalla 2024-11-26 023712](https://github.com/user-attachments/assets/953a4942-0bed-495e-ae7e-1bdcd251ccd0)

**Cadena: int x, y, z ;**

![Captura de pantalla 2024-11-26 023747](https://github.com/user-attachments/assets/12b029f1-7eb2-4aea-8927-b47a8b190830)

**Cadena: 
int a;
int suma(int a, int b){
return a+b;
}
int main(){
float a;
int b;
int c;
c = a+b;
c = suma(8,9);
}**

![Captura de pantalla 2024-11-26 023946](https://github.com/user-attachments/assets/06bb455d-4c6f-46e8-aa30-10991763e1dd)
