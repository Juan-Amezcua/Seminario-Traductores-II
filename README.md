# Proyecto Compilador

## Mini Analizador Léxico

<a href="https://github.com/Juan-Amezcua/Seminario-Traductores-II/tree/main/01_Mini-Analizador_Lexico">Archivos de esta sección - Mini Analizador Léxico</a><br>

Este proyecto implementa una versión simplificada de un analizador léxico en Python. El analizador es capaz de tokenizar una cadena de entrada y clasificar los tokens en categorías básicas.

### Características

- Reconoce identificadores y números reales.
- Proporciona una interfaz de línea de comandos para el análisis léxico interactivo.
- Muestra los resultados en una tabla formateada.

### Ejemplo

![Captura de pantalla 2024-09-09 122937](https://github.com/user-attachments/assets/6471823a-932e-4d6e-8617-14a661660c23)

## Analizador Léxico Completo

<a href="https://github.com/Juan-Amezcua/Seminario-Traductores-II/tree/main/02_Analizador_Lexico_Completo">Archivos de esta sección - Analizador Léxico Completo</a><br>

Este proyecto implementa un analizador léxico simple en Python. El analizador es capaz de tokenizar una cadena de entrada y clasificar los tokens en diferentes categorías.

### Características

- Reconoce identificadores, números (enteros y de punto flotante), operadores, palabras clave y símbolos especiales.
- Proporciona una interfaz de línea de comandos para el análisis léxico interactivo.
- Muestra los resultados en una tabla formateada.

### Ejemplo

![Captura de pantalla 2024-09-09 122723](https://github.com/user-attachments/assets/c8290065-813f-465c-a9c1-71858c246aaf)

## Analizador Léxico y Sintáctico en Python

<a href="https://github.com/Juan-Amezcua/Seminario-Traductores-II/tree/main/04_Analizador_Sintactico_Objetos">Archivos de esta sección - Analizador Léxico y Sintáctico</a><br>

Este proyecto implementa un **analizador léxico y sintáctico** para un lenguaje de programación simplificado, escrito en Python. El programa es una versión anterior al analizador completo, centrado en demostrar las fases iniciales del análisis léxico y sintáctico.

### Características

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
 
### Ejemplo

- **Cadena "a+b"**

<img width="369" alt="image" src="https://github.com/user-attachments/assets/876686fa-bb4d-4b70-8bf7-837565ddd0fc">

- **Cadena "a+b+c+d+e+f"**

![imagen](https://github.com/user-attachments/assets/ce9e573e-3125-4b1f-b78c-fe32db40265b)

## Analizador Léxico y Sintáctico en Python (Gramática del Compilador)

<a href="https://github.com/Juan-Amezcua/Seminario-Traductores-II/tree/main/05_Gramatica_Compilador">Archivos de esta sección - Analizador Sintáctico con Gramática del Compilador</a><br>

Este proyecto implementa un **analizador léxico y sintáctico** para un lenguaje de programación simplificado, escrito en Python. El analizador léxico tokeniza una cadena de entrada, mientras que el analizador sintáctico verifica la estructura gramatical utilizando una tabla LR.

### Características

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
 
### Ejemplos input

**Cadenas correctas**

![Input 1](https://github.com/user-attachments/assets/12da8d73-81cc-41b4-8d1a-381ff1ce2cb0)

![Captura de pantalla 2024-09-30 123125](https://github.com/user-attachments/assets/94d34088-9fa9-4d96-ba2e-3e13bfb254b4)

**Cadenas incorrectas**

![Captura de pantalla 2024-09-30 123436](https://github.com/user-attachments/assets/06b8614d-2ee7-4da6-bb17-ec2190d9da84)

![Captura de pantalla 2024-09-30 123519](https://github.com/user-attachments/assets/65dd8c12-c4ce-471d-8f72-d5941db40fa7)

## Analizador Léxico y Sintáctico en Python (Árbol Sintáctico)

<a href="https://github.com/Juan-Amezcua/Seminario-Traductores-II/tree/main/06_Arbol_Sintactico">Archivos de esta sección - Árbol Sintáctico </a><br>

Analizador sintáctico completo adaptado para mostrar el árbol sintáctico

### Ejemplos input

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

## Analizador Semántico

<a href="https://github.com/Juan-Amezcua/Seminario-Traductores-II/tree/main/08_Analizador_Semantico">Archivos de esta sección - Analizador Semántico </a><br>

Este proyecto implementa un compilador funcional que procesa código fuente hasta la fase de análisis semántico. El objetivo principal es garantizar que el código no solo sea válido en términos gramaticales, sino también lógico y coherente, validando aspectos como tipos de datos, declaraciones de variables, funciones y estructuras de control.

### Características Principales

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

### Ejemplos input

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

## Compilador con Generación de Código Ensamblador 8086

<a href="https://github.com/Juan-Amezcua/Seminario-Traductores-II/tree/main/09_Generador_Codigo">Archivos de esta sección - Compilador con Generación de Código Ensamblador 8086 </a><br>

Este proyecto implementa un compilador que procesa un archivo fuente en C, realizando todas las fases principales de la compilación hasta generar código ensamblador compatible con el procesador 8086.

### Descripción General

**Analizador Léxico:** Divide el código fuente en tokens (identificadores, palabras clave, operadores, etc.) y detecta errores léxicos.

**Analizador Sintáctico:** Construye un árbol sintáctico basado en la gramática definida, validando la estructura del programa.

**Analizador Semántico:** Asegura la validez lógica del programa verificando tipos de datos, uso de variables, funciones y otras reglas semánticas. Incluye una tabla de símbolos que organiza y rastrea identificadores por ámbito.

**Generación de Representación Intermedia (IR):** Convierte el árbol sintáctico en una representación intermedia que facilita la traducción a ensamblador.

**Generación de Código Ensamblador:** Produce código ensamblador 8086 a partir del IR, utilizando instrucciones adecuadas para inicialización de datos, control de flujo, operaciones aritméticas, etc.

### Características Principales

**Compatibilidad con C básico:** Admite funciones, variables, expresiones aritméticas, control de flujo (if, while), entre otros.

**Generación Automática de Código Ensamblador:** Convierte el código fuente en un archivo .asm que puede ensamblarse y ejecutarse.

**Gestión de Ámbitos:** Soporte para anidamiento de funciones y bloques con alcance léxico bien definido.

**Subrutinas Incorporadas:** Incluye soporte para impresión básica en consola (print).

**Manejo de Errores:** Detecta y reporta errores léxicos, sintácticos y semánticos de manera detallada.

## Estructura de Archivos

  - main.py: Punto de entrada que coordina todas las fases de compilación.
  - categoria_token.py: Enumera las categorías de tokens léxicos.
  - analizador_lexico.py: Realiza el análisis léxico.
  - analizador_sintactico.py: Implementa el análisis sintáctico y la construcción del árbol sintáctico.
  - analizador_semantico.py: Verifica reglas semánticas usando la tabla de símbolos.
  - tabla_simbolos.py: Maneja la tabla de símbolos.
  - generador_ir.py: Genera la representación intermedia (IR).
  - generador_codigo.py: Traduce el IR a código ensamblador 8086.
  - compilador.lr: Archivo que contiene la tabla LR utilizada por el analizador sintáctico.
