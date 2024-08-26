# Analizador Sintáctico en Python

Este proyecto implementa un analizador sintáctico simple en Python, utilizando un analizador léxico como componente. El analizador es capaz de procesar expresiones simples y realizar análisis sintáctico utilizando tablas de transición.

## Características

- Analizador léxico integrado que reconoce varios tipos de tokens.
- Analizador sintáctico basado en tablas de transición.
- Implementación de una pila para el análisis sintáctico.
- Capacidad de analizar expresiones simples.
- Dos modos de análisis con diferentes tablas de transición.

## Estructura del Proyecto

El proyecto consta de tres archivos principales:

1. `main.py`: Contiene la implementación del analizador sintáctico y la lógica principal.
2. `lexico.py`: Implementa el analizador léxico utilizado por el analizador sintáctico.
3. `pila.py`: Proporciona una implementación de pila utilizada en el análisis sintáctico.

## Uso

Para usar el analizador sintáctico, ejecute el script `main.py`

## Componentes Principales

### Analizador Léxico

- Reconoce varios tipos de tokens como identificadores, números, operadores, y palabras clave.
- Implementado en la clase `AnalizadorLexico` en `lexico.py`.

### Analizador Sintáctico

- Utiliza tablas de transición para el análisis.
- Implementa acciones de desplazamiento y reducción.
- Definido en la clase `Parser` en `main.py`.

### Pila

- Estructura de datos auxiliar para el análisis sintáctico.
- Implementada en la clase `Pila` en `pila.py`.
