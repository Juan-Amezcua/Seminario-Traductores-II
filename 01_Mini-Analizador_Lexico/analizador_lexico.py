from categoria_token import CategoriaToken

class AnalizadorLexico:
    def __init__(self, fuente_entrada=""):
        self.posicion = 0
        self.fuente_entrada = fuente_entrada
        self.token_actual = ""
        self.tipo_actual = None
        self.continuar_escaner = True
        self.caracter_actual = ""
        self.estado_actual = 0

    def establecer_entrada(self, fuente_entrada):
        self.posicion = 0
        self.fuente_entrada = fuente_entrada

    def obtener_categoria_token(self, tipo_token):
        descripciones = {
            CategoriaToken.IDENTIFICADOR: "Identificador",
            CategoriaToken.NUMERO_REAL: "Número Real",
            CategoriaToken.FIN_DE_ENTRADA: "Fin de la Entrada",
        }
        return descripciones.get(tipo_token, "Desconocido")

    def obtener_siguiente_token(self):
        self.estado_actual = 0
        self.continuar_escaner = True
        self.token_actual = ""

        while self.continuar_escaner:
            self.caracter_actual = self.obtener_siguiente_caracter()

            if self.estado_actual == 0:
                if self.es_letra(self.caracter_actual):
                    self.estado_actual = 1
                    self.token_actual += self.caracter_actual
                elif self.es_digito(self.caracter_actual):
                    self.estado_actual = 2
                    self.token_actual += self.caracter_actual
                else:
                    if self.caracter_actual == '$':
                        self.token_actual += self.caracter_actual
                        self.aceptar_token(CategoriaToken.FIN_DE_ENTRADA)

            elif self.estado_actual == 1:  # Identificadores
                if self.es_letra(self.caracter_actual) or self.es_digito(self.caracter_actual):
                    self.token_actual += self.caracter_actual
                else:
                    self.aceptar_token(CategoriaToken.IDENTIFICADOR)
                    self.retroceder()

            elif self.estado_actual == 2:  # Números reales
                if self.es_digito(self.caracter_actual):
                    self.token_actual += self.caracter_actual
                elif self.caracter_actual == '.':
                    self.estado_actual = 3
                    self.token_actual += self.caracter_actual
                else:
                    self.aceptar_token(CategoriaToken.NUMERO_REAL)
                    self.retroceder()

            elif self.estado_actual == 3:  # Flotantes
                if self.es_digito(self.caracter_actual):
                    self.token_actual += self.caracter_actual
                    self.estado_actual = 4
                else:
                    self.aceptar_token(CategoriaToken.NUMERO_REAL)
                    self.retroceder()

            elif self.estado_actual == 4:  # Resto de números
                if self.es_digito(self.caracter_actual):
                    self.token_actual += self.caracter_actual
                else:
                    self.aceptar_token(CategoriaToken.NUMERO_REAL)
                    self.retroceder()

        return self.tipo_actual

    def obtener_siguiente_caracter(self):
        if self.entrada_consumida():
            return '$'
        caracter = self.fuente_entrada[self.posicion]
        self.posicion += 1
        return caracter

    def aceptar_token(self, estado_final):
        self.tipo_actual = estado_final
        self.continuar_escaner = False

    def entrada_consumida(self):
        return self.posicion >= len(self.fuente_entrada)

    def es_letra(self, caracter):
        return caracter.isalpha() or caracter == '_'

    def es_digito(self, caracter):
        return caracter.isdigit()

    def retroceder(self):
        if self.caracter_actual != '$':
            self.posicion -= 1
