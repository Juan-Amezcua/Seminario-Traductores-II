# Analizador Semántico

Este proyecto implementa un compilador funcional que procesa código fuente hasta la fase de análisis semántico. El objetivo principal es garantizar que el código no solo sea válido en términos gramaticales, sino también lógico y coherente, validando aspectos como tipos de datos, declaraciones de variables, funciones y estructuras de control.

## Características Principales

- **Analizador Léxico:**
  - Divide el código en tokens como identificadores, palabras clave y operadores.
  - Detecta y reporta errores léxicos.

- **Analizador Sintáctico:**
  - Construye un árbol sintáctico validando la estructura del programa según su gramática.
  - Reporta errores de estructura gramatical.

- **Analizador Semántico:**
  - Maneja una tabla de símbolos para controlar declaraciones y ámbitos.
  - Verifica reglas semánticas como asignaciones válidas, coherencia de tipos y parámetros de funciones.
  - Genera mensajes detallados sobre errores semánticos encontrados.

- **Estructura de Archivos**
  - main.py: Punto de entrada que conecta todas las fases y ejecuta el análisis completo.
  - analizador_lexico.py: Contiene la implementación del analizador léxico.
  - analizador_sintactico.py: Contiene la implementación del analizador sintáctico.
  - categoria_token.py: Define las categorías de tokens utilizadas en el análisis.
  - analizador_semantico.py: Verifica la coherencia semántica del programa.
  - compilador.lr: Archivo que contiene la tabla LR utilizada por el analizador sintáctico.
  - Documentacion: Documento que explica el diseño y las decisiones de implementación.

## Ejemplos input

**Cadena (semánticamente incorrecta): 
int main(){
float a;
int b;
int c;
c = a+b;
c = suma(8,9);
}**

![Captura de pantalla 2024-11-26 054222](https://github.com/user-attachments/assets/40ba1c22-9e8b-44b6-b0f0-56b02512f52c)

**Cadena (semánticamente incorrecta): 
int a;
int suma(int a, int b){
return a+b;
}
int main(){
float a;
int b;
int c;
c = a+b;
c = suma(8.5,9.9);
}**

![Captura de pantalla 2024-11-26 054639](https://github.com/user-attachments/assets/e3594825-288c-43bc-bb7e-004f07616685)

**Cadena (semánticamente correcta): 
int suma(int a, int b) {
    return a + b;
}
int main() {
    int a;
    int b;
    int c;
    a = 5;
    b = 10;
    c = suma(a, b);
}**

![Captura de pantalla 2024-11-26 055445](https://github.com/user-attachments/assets/03040d6d-ffcf-4db2-ae9e-24f72650d963)

![Captura de pantalla 2024-11-26 055512](https://github.com/user-attachments/assets/f7cdf34c-6f5e-4838-a19e-1e8e477ad8dc)

