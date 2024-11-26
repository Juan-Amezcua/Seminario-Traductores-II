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
                elif self.es_espacio_blanco(self.caracter_actual):
                    # Omite espacios en blanco y continúa con el siguiente carácter
                    pass
                else:
                    if self.caracter_actual == '$':
                        self.token_actual += self.caracter_actual
                        self.aceptar_token(CategoriaToken.FIN_DE_ENTRADA)
                    else:
                        if self.caracter_actual != '':
                            self.token_actual += self.caracter_actual
                        self.aceptar_token(CategoriaToken.TIPO_ERROR)

            elif self.estado_actual == 1:
                if self.es_letra(self.caracter_actual) or self.es_digito(self.caracter_actual):
                    self.token_actual += self.caracter_actual
                else:
                    # Verificar palabras clave y asignar tipos de token apropiados
                    if self.token_actual in ["int", "float", "void", "char"]:
                        self.aceptar_token(CategoriaToken.TIPO_DATO)
                    elif self.token_actual == "if":
                        self.aceptar_token(CategoriaToken.PALABRA_CLAVE_IF)
                    elif self.token_actual == "while":
                        self.aceptar_token(CategoriaToken.PALABRA_CLAVE_WHILE)
                    elif self.token_actual == "return":
                        self.aceptar_token(CategoriaToken.PALABRA_CLAVE_RETURN)
                    elif self.token_actual == "else":
                        self.aceptar_token(CategoriaToken.PALABRA_CLAVE_ELSE)
                    elif self.token_actual == "programa":
                        self.aceptar_token(24)  # Suponiendo que 'programa' tiene asignado el ID 24
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
                    self.retroceder()

            elif self.estado_actual == 4:
                if self.es_digito(self.caracter_actual):
                    self.token_actual += self.caracter_actual
                else:
                    self.aceptar_token(CategoriaToken.PUNTO_FLOTANTE)
                    self.retroceder()

            elif self.estado_actual == 5:
                if self.caracter_actual == '=':
                    self.token_actual += self.caracter_actual
                    self.aceptar_token(CategoriaToken.OPERADOR_RELACIONAL)
                else:
                    self.aceptar_token(CategoriaToken.OPERADOR_RELACIONAL)
                    self.retroceder()

            elif self.estado_actual == 6:
                if self.caracter_actual == '|':
                    self.token_actual += self.caracter_actual
                    self.aceptar_token(CategoriaToken.OPERADOR_LOGICO_O)
                else:
                    self.aceptar_token(CategoriaToken.TIPO_ERROR)
                    self.retroceder()

            elif self.estado_actual == 7:
                if self.caracter_actual == '&':
                    self.token_actual += self.caracter_actual
                    self.aceptar_token(CategoriaToken.OPERADOR_LOGICO_Y)
                else:
                    self.aceptar_token(CategoriaToken.TIPO_ERROR)
                    self.retroceder()

            elif self.estado_actual == 8:
                if self.caracter_actual == '=':
                    self.token_actual += self.caracter_actual
                    self.aceptar_token(CategoriaToken.OPERADOR_IGUALDAD)
                else:
                    self.aceptar_token(CategoriaToken.OPERADOR_LOGICO_NO)
                    self.retroceder()

            elif self.estado_actual == 9:
                if self.caracter_actual == '=':
                    self.token_actual += self.caracter_actual
                    self.aceptar_token(CategoriaToken.OPERADOR_IGUALDAD)
                else:
                    self.aceptar_token(CategoriaToken.OPERADOR_ASIGNACION)
                    self.retroceder()

            else:
                # Estado desconocido, tratar como error
                self.aceptar_token(CategoriaToken.TIPO_ERROR)

        return self.tipo_actual

    def obtener_siguiente_caracter(self):
        if not self.entrada_consumida():
            ch = self.fuente_entrada[self.posicion]
            self.posicion += 1
            return ch
        else:
            return '$'

    def establecer_estado(self, nuevo_estado):
        self.estado_actual = nuevo_estado

    def aceptar_token(self, estado_final):
        self.tipo_actual = estado_final
        self.continuar_escaneo = False

    def entrada_consumida(self):
        return self.posicion >= len(self.fuente_entrada)

    def es_letra(self, ch):
        return ch.isalpha() or ch == '_'

    def es_digito(self, ch):
        return ch.isdigit()

    def es_espacio_blanco(self, ch):
        return ch in [' ', '\t', '\n', '\r']

    def retroceder(self):
        if self.caracter_actual != '$' and self.caracter_actual != '':
            self.posicion -= 1
