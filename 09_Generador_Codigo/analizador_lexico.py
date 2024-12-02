# analizador_lexico.py

from categoria_token import CategoriaToken

class AnalizadorLexico:
    def __init__(self, fuente_entrada=""):
        self.posicion = 0
        self.fuente_entrada = fuente_entrada
        self.token_actual = ""
        self.tipo_actual = None
        self.continuar_escaneo = True
        self.caracter_actual = ""
        self.estado_actual = 0

    def establecer_entrada(self, fuente_entrada):
        self.posicion = 0
        self.fuente_entrada = fuente_entrada

    def obtener_siguiente_token(self):
        self.estado_actual = 0
        self.continuar_escaneo = True
        self.token_actual = ""

        while self.continuar_escaneo:
            self.caracter_actual = self.obtener_siguiente_caracter()

            if self.estado_actual == 0:
                if self.es_letra(self.caracter_actual):
                    self.estado_actual = 1
                    self.token_actual += self.caracter_actual
                elif self.es_digito(self.caracter_actual):
                    self.estado_actual = 2
                    self.token_actual += self.caracter_actual
                elif self.caracter_actual in ['+', '-']:
                    self.token_actual += self.caracter_actual
                    self.aceptar_token(CategoriaToken.OPERADOR_ADITIVO)
                elif self.caracter_actual in ['*', '/']:
                    self.token_actual += self.caracter_actual
                    self.aceptar_token(CategoriaToken.OPERADOR_MULTIPLICATIVO)
                elif self.caracter_actual in ['<', '>']:
                    self.estado_actual = 5
                    self.token_actual += self.caracter_actual
                elif self.caracter_actual == '|':
                    self.estado_actual = 6
                    self.token_actual += self.caracter_actual
                elif self.caracter_actual == '&':
                    self.estado_actual = 7
                    self.token_actual += self.caracter_actual
                elif self.caracter_actual == '!':
                    self.estado_actual = 8
                    self.token_actual += self.caracter_actual
                elif self.caracter_actual == ';':
                    self.token_actual += self.caracter_actual
                    self.aceptar_token(CategoriaToken.PUNTO_Y_COMA)
                elif self.caracter_actual == ',':
                    self.token_actual += self.caracter_actual
                    self.aceptar_token(CategoriaToken.COMA)
                elif self.caracter_actual == '(':
                    self.token_actual += self.caracter_actual
                    self.aceptar_token(CategoriaToken.PARENTESIS_ABIERTO)
                elif self.caracter_actual == ')':
                    self.token_actual += self.caracter_actual
                    self.aceptar_token(CategoriaToken.PARENTESIS_CERRADO)
                elif self.caracter_actual == '{':
                    self.token_actual += self.caracter_actual
                    self.aceptar_token(CategoriaToken.LLAVE_ABIERTA)
                elif self.caracter_actual == '}':
                    self.token_actual += self.caracter_actual
                    self.aceptar_token(CategoriaToken.LLAVE_CERRADA)
                elif self.caracter_actual == '=':
                    self.estado_actual = 9
                    self.token_actual += self.caracter_actual
                elif self.caracter_actual == '$':
                    self.token_actual += self.caracter_actual
                    self.aceptar_token(CategoriaToken.FIN_DE_ENTRADA)
                elif self.es_espacio_blanco(self.caracter_actual):
                    # Ignorar espacios en blanco
                    continue
                else:
                    if self.caracter_actual == '$':
                        self.token_actual += self.caracter_actual
                        self.aceptar_token(CategoriaToken.FIN_DE_ENTRADA)
                    else:
                        # Caracter desconocido
                        self.token_actual += self.caracter_actual
                        self.aceptar_token(CategoriaToken.TIPO_ERROR)

            elif self.estado_actual == 1:
                if self.es_letra(self.caracter_actual) or self.es_digito(self.caracter_actual):
                    self.token_actual += self.caracter_actual
                else:
                    self.token_respaldo = self.token_actual
                    if self.token_respaldo in ["int", "float", "void"]:
                        self.aceptar_token(CategoriaToken.TIPO_DATO)
                    elif self.token_respaldo == "if":
                        self.aceptar_token(CategoriaToken.PALABRA_CLAVE_IF)
                    elif self.token_respaldo == "while":
                        self.aceptar_token(CategoriaToken.PALABRA_CLAVE_WHILE)
                    elif self.token_respaldo == "return":
                        self.aceptar_token(CategoriaToken.PALABRA_CLAVE_RETURN)
                    elif self.token_respaldo == "else":
                        self.aceptar_token(CategoriaToken.PALABRA_CLAVE_ELSE)
                    else:
                        self.aceptar_token(CategoriaToken.IDENTIFICADOR)
                    self.retroceder()

            elif self.estado_actual == 2:
                if self.es_digito(self.caracter_actual):
                    self.token_actual += self.caracter_actual
                elif self.caracter_actual == '.':
                    self.estado_actual = 3
                    self.token_actual += self.caracter_actual
                else:
                    self.aceptar_token(CategoriaToken.ENTERO)
                    self.retroceder()

            elif self.estado_actual == 3:
                if self.es_digito(self.caracter_actual):
                    self.token_actual += self.caracter_actual
                    self.estado_actual = 4
                else:
                    self.aceptar_token(CategoriaToken.TIPO_ERROR)

            elif self.estado_actual == 4:
                if self.es_digito(self.caracter_actual):
                    self.token_actual += self.caracter_actual
                else:
                    self.aceptar_token(CategoriaToken.PUNTO_FLOTANTE)
                    self.retroceder()

            elif self.estado_actual == 5:
                if self.caracter_actual != '=':
                    self.aceptar_token(CategoriaToken.OPERADOR_RELACIONAL)
                    self.retroceder()
                else:
                    self.token_actual += self.caracter_actual
                    self.aceptar_token(CategoriaToken.OPERADOR_RELACIONAL)

            elif self.estado_actual == 6:
                if self.caracter_actual != '|':
                    self.aceptar_token(CategoriaToken.TIPO_ERROR)
                    self.retroceder()
                else:
                    self.token_actual += self.caracter_actual
                    self.aceptar_token(CategoriaToken.OPERADOR_LOGICO_O)

            elif self.estado_actual == 7:
                if self.caracter_actual != '&':
                    self.aceptar_token(CategoriaToken.TIPO_ERROR)
                    self.retroceder()
                else:
                    self.token_actual += self.caracter_actual
                    self.aceptar_token(CategoriaToken.OPERADOR_LOGICO_Y)

            elif self.estado_actual == 8:
                if self.caracter_actual != '=':
                    self.aceptar_token(CategoriaToken.OPERADOR_LOGICO_NO)
                    self.retroceder()
                else:
                    self.token_actual += self.caracter_actual
                    self.aceptar_token(CategoriaToken.OPERADOR_IGUALDAD)

            elif self.estado_actual == 9:
                if self.caracter_actual != '=':
                    self.aceptar_token(CategoriaToken.OPERADOR_ASIGNACION)
                    self.retroceder()
                else:
                    self.token_actual += self.caracter_actual
                    self.aceptar_token(CategoriaToken.OPERADOR_IGUALDAD)

        return self.tipo_actual

    def obtener_siguiente_caracter(self):
        if self.entrada_consumida():
            return '$'
        caracter = self.fuente_entrada[self.posicion]
        self.posicion += 1
        return caracter

    def establecer_estado(self, nuevo_estado):
        self.estado_actual = nuevo_estado

    def aceptar_token(self, estado_final):
        self.tipo_actual = estado_final
        self.continuar_escaneo = False

    def entrada_consumida(self):
        return self.posicion >= len(self.fuente_entrada)

    def es_letra(self, caracter):
        return caracter.isalpha() or caracter == '_'

    def es_digito(self, caracter):
        return caracter.isdigit()

    def es_espacio_blanco(self, caracter):
        return caracter in [' ', '\t', '\n', '\r']

    def retroceder(self):
        if self.caracter_actual != '$':
            self.posicion -= 1

    def obtener_categoria_token(self, tipo_token):
        descripciones = {
            CategoriaToken.IDENTIFICADOR: "Identificador",
            CategoriaToken.ENTERO: "Número Entero",
            CategoriaToken.PUNTO_FLOTANTE: "Número Real",
            CategoriaToken.LITERAL_CADENA: "Cadena",
            CategoriaToken.TIPO_DATO: "Tipo de dato",
            CategoriaToken.OPERADOR_ADITIVO: "Operador Suma/Resta",
            CategoriaToken.OPERADOR_MULTIPLICATIVO: "Operador Mult/Div",
            CategoriaToken.OPERADOR_RELACIONAL: "Operador Relacional",
            CategoriaToken.OPERADOR_LOGICO_O: "Operador OR",
            CategoriaToken.OPERADOR_LOGICO_Y: "Operador AND",
            CategoriaToken.OPERADOR_LOGICO_NO: "Operador NOT",
            CategoriaToken.OPERADOR_IGUALDAD: "Operador Igualdad",
            CategoriaToken.PUNTO_Y_COMA: "Punto y Coma",
            CategoriaToken.COMA: "Coma",
            CategoriaToken.PARENTESIS_ABIERTO: "Paréntesis Abierto",
            CategoriaToken.PARENTESIS_CERRADO: "Paréntesis Cerrado",
            CategoriaToken.LLAVE_ABIERTA: "Llave Abierta",
            CategoriaToken.LLAVE_CERRADA: "Llave Cerrada",
            CategoriaToken.OPERADOR_ASIGNACION: "Operador Asignación",
            CategoriaToken.PALABRA_CLAVE_IF: "Palabra Reservada 'if'",
            CategoriaToken.PALABRA_CLAVE_WHILE: "Palabra Reservada 'while'",
            CategoriaToken.PALABRA_CLAVE_RETURN: "Palabra Reservada 'return'",
            CategoriaToken.PALABRA_CLAVE_ELSE: "Palabra Reservada 'else'",
            CategoriaToken.FIN_DE_ENTRADA: "Fin de Entrada",
            CategoriaToken.TIPO_ERROR: "Error Léxico",
        }
        return descripciones.get(tipo_token, "Desconocido")
