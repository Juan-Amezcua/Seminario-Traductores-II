# main.py

from analizador_lexico import AnalizadorLexico
from analizador_sintactico import AnalizadorSintactico
from analizador_semantico import AnalizadorSemantico 

def main():
    cadena_entrada = input("Ingrese la cadena de entrada para el análisis: ")
    analizador_lexico = AnalizadorLexico(cadena_entrada)
    analizador_sintactico = AnalizadorSintactico(analizador_lexico, archivo_lr='compilador.lr')
    analizador_sintactico.analizar()
    if analizador_sintactico.aceptado:
        # El análisis sintáctico tuvo éxito, procede al análisis semántico
        analizador_semantico = AnalizadorSemantico(analizador_sintactico.raiz_arbol_sintactico)
        analizador_semantico.analizar()
    else:
        print("El análisis sintáctico falló. No se puede realizar el análisis semántico.")

if __name__ == "__main__":
    main()
