# main.py

from analizador_lexico import AnalizadorLexico
from analizador_sintactico import AnalizadorSintactico

def main():
    cadena_entrada = input("Ingrese la cadena de entrada para el análisis sintáctico: ")
    analizador_lexico = AnalizadorLexico(cadena_entrada)
    analizador_sintactico = AnalizadorSintactico(analizador_lexico, archivo_lr='compilador.lr')
    analizador_sintactico.analizar()

if __name__ == "__main__":
    main()
