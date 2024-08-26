from analizador_lexico import AnalizadorLexico
from categoria_token import CategoriaToken

def main():
    cadena_entrada = input("Ingrese la cadena de entrada para el análisis léxico: ")

    analizador_lexico = AnalizadorLexico(cadena_entrada)

    # Adjusted column width for 'Tipo'
    print("\nResultado del Análisis Léxico")
    print("╔════════════════════╦════════════════════════════╗")
    print("║      Símbolo       ║            Tipo            ║")
    print("╠════════════════════╬════════════════════════════╣")

    while True:
        tipo_token = analizador_lexico.obtener_siguiente_token()

        # Prepare the current token and its type with appropriate widths
        simbolo = f"{analizador_lexico.token_actual:^20}"
        tipo = f"{analizador_lexico.obtener_categoria_token(tipo_token):^28}"
        print(f"║{simbolo}║{tipo}║")

        # Check if the end of input is reached and avoid printing an extra row
        if tipo_token == CategoriaToken.FIN_DE_ENTRADA:
            break
        else:
            print("╠════════════════════╬════════════════════════════╣")

    # Bottom border of the table after the last token is printed
    print("╚════════════════════╩════════════════════════════╝")

if __name__ == "__main__":
    main()



