from analizador_lexico import AnalizadorLexico
from categoria_token import CategoriaToken

def main():
    cadena_entrada = input("Ingrese la cadena de entrada para el análisis léxico: ")

    analizador_lexico = AnalizadorLexico(cadena_entrada)

    # Ajustar el ancho de la columna 'Tipo'
    print("\nResultado del Análisis Léxico")
    print("╔════════════════════╦════════════════════════════╗")
    print("║      Símbolo       ║            Tipo            ║")
    print("╠════════════════════╬════════════════════════════╣")

    while True:
        tipo_token = analizador_lexico.obtener_siguiente_token()

        # Preparar el token actual y su tipo con los anchos apropiados
        simbolo = f"{analizador_lexico.token_actual:^20}"
        tipo_token_str = f"{analizador_lexico.obtener_categoria_token(tipo_token):^28}"
        print(f"║{simbolo}║{tipo_token_str}║")

        # Verificar si se ha alcanzado el final de la entrada y evitar imprimir una fila extra
        if tipo_token == CategoriaToken.FIN_DE_ENTRADA:
            break
        else:
            print("╠════════════════════╬════════════════════════════╣")

    # Borde inferior de la tabla después de imprimir el último token
    print("╚════════════════════╩════════════════════════════╝")

if __name__ == "__main__":
    main()





