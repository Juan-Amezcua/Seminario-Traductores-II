# main.py

from analizador_lexico import AnalizadorLexico
from analizador_sintactico import AnalizadorSintactico
from analizador_semantico import AnalizadorSemantico
from generador_ir import GeneradorIR
from generador_codigo import GeneradorCodigo
from categoria_token import CategoriaToken

def main():
    while True:
        # Limpiar la pantalla
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        
        nombre_archivo_c = input("Ingrese el nombre del archivo .c a analizar: ")
        try:
            with open(nombre_archivo_c, 'r') as archivo_c:
                cadena_entrada = archivo_c.read()
        except FileNotFoundError:
            print(f"No se pudo encontrar el archivo '{nombre_archivo_c}'.")
            opcion = input("\n¿Desea intentar con otro archivo? (s/n): ")
            if opcion.lower() != 's':
                break
            else:
                continue
        analizador_lexico = AnalizadorLexico(cadena_entrada)
        
        # Imprimir tabla de lexemas
        print("\nResultado del Análisis Léxico")
        print("╔════════════════════╦════════════════════════════╗")
        print("║      Símbolo       ║            Tipo            ║")
        print("╠════════════════════╬════════════════════════════╣")
    
        while True:
            tipo_token = analizador_lexico.obtener_siguiente_token()
    
            # Preparar el token actual y su tipo con anchuras adecuadas
            simbolo = f"{analizador_lexico.token_actual:^20}"
            tipo = f"{analizador_lexico.obtener_categoria_token(tipo_token):^28}"
            print(f"║{simbolo}║{tipo}║")
    
            # Verificar si se ha llegado al final de la entrada y evitar imprimir una fila extra
            if tipo_token == CategoriaToken.FIN_DE_ENTRADA:
                break
            else:
                print("╠════════════════════╬════════════════════════════╣")
    
        # Borde inferior de la tabla después de imprimir el último token
        print("╚════════════════════╩════════════════════════════╝")
    
        # Reiniciar el analizador léxico para analizar la entrada nuevamente
        analizador_lexico = AnalizadorLexico(cadena_entrada)
        analizador_sintactico = AnalizadorSintactico(analizador_lexico, archivo_lr='compilador.lr')
        analizador_sintactico.analizar()
    
        if analizador_sintactico.aceptado:
            # Realizar análisis semántico
            analizador_semantico = AnalizadorSemantico(analizador_sintactico.raiz_arbol_sintactico)
            analizador_semantico.analizar()
    
            # Generar código intermedio si no hay errores semánticos
            if not analizador_semantico.errores:
                generador_ir = GeneradorIR()
                generador_ir.generar(analizador_sintactico.raiz_arbol_sintactico)
                # El código IR se procesa internamente, no se imprime
                
                # Generar código ensamblador, pasar la tabla de símbolos
                generador_codigo = GeneradorCodigo(generador_ir.codigo, analizador_semantico.tabla_simbolos)
                codigo_asm = generador_codigo.generar()

                # Obtener el nombre base del archivo .c sin la extensión
                nombre_base = os.path.splitext(nombre_archivo_c)[0]
                nombre_archivo_asm = f"{nombre_base}.asm"
                
                # Escribir el código ensamblador en un archivo .asm
                with open(nombre_archivo_asm, 'w') as archivo_asm:
                    for linea in codigo_asm:
                        print(linea)
                        archivo_asm.write(linea + '\n')
                print(f"\nCódigo ensamblador 8086 generado en el archivo '{nombre_archivo_asm}'.")
            else:
                print("Generación de código omitida debido a errores semánticos.")
        else:
            print("Análisis sintáctico fallido. No se puede realizar el análisis semántico.")
        
        # Preguntar al usuario si desea analizar otra cadena
        opcion = input("\n¿Desea analizar otra cadena? (s/n): ")
        if opcion.lower() != 's':
            break

if __name__ == "__main__":
    main()
