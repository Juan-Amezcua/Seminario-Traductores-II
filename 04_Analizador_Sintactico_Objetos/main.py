# main.py

from analizador_lexico import AnalizadorLexico
from analizador_sintactico import AnalizadorSintactico

def main():
    cadena_entrada = input("Ingrese la cadena de entrada para el análisis sintáctico: ")

    analizador_lexico = AnalizadorLexico(cadena_entrada)

    # Los dos tipos de gramáticas
    if cadena_entrada.count('+') > 1:
        gramatica = 'gramatica2'
    else:
        gramatica = 'gramatica1'

    analizador_sintactico = AnalizadorSintactico(analizador_lexico, gramatica=gramatica)
    analizador_sintactico.analizar()

if __name__ == "__main__":
    main()
