from enum import Enum

class TipoSimbolo(Enum):
    ERROR = -1
    IDENTIFICADOR = 0
    ENTERO = 1
    FLOTANTE = 2
    CADENA = 3
    TIPO = 4
    OPERADOR_SUMA = 5
    OPERADOR_MULTIPLICACION = 6
    OPERADOR_RELACIONAL = 7
    OPERADOR_O = 8
    OPERADOR_Y = 9
    OPERADOR_NEGACION = 10
    OPERADOR_IGUALDAD = 11
    PUNTO_Y_COMA = 12
    COMA = 13
    PARENTESIS_ABIERTO = 14
    PARENTESIS_CERRADO = 15
    LLAVE_ABIERTA = 16
    LLAVE_CERRADA = 17
    OPERADOR_ASIGNACION = 18
    PALABRA_IF = 19
    PALABRA_WHILE = 20
    PALABRA_RETURN = 21
    PALABRA_ELSE = 22
    FIN_ENTRADA = 23

class AnalizadorLexico:
    def __init__(self, fuente_entrada=""):
        self.simbolo_actual = ""
        self.tipo_simbolo = TipoSimbolo.ERROR
        self.fuente_entrada = fuente_entrada
        self.indice_actual = 0
        self.en_ejecucion = True
        self.caracter_actual = ''
        self.estado = 0

    def establecer_entrada(self, fuente_entrada):
        self.indice_actual = 0
        self.fuente_entrada = fuente_entrada

    def obtener_siguiente_simbolo(self):
        self.estado = 0
        self.en_ejecucion = True
        self.simbolo_actual = ""
        while self.en_ejecucion:
            self.caracter_actual = self.obtener_siguiente_caracter()
            if self.caracter_actual == '$':
                break
            self.procesar_caracter_actual()
        self.determinar_tipo_simbolo()

    def obtener_siguiente_caracter(self):
        if self.entrada_terminada():
            return '$'
        caracter = self.fuente_entrada[self.indice_actual]
        self.indice_actual += 1
        return caracter

    def procesar_caracter_actual(self):
        if self.estado == 0:
            if self.caracter_actual.isalpha() or self.caracter_actual == '_':
                self.estado = 1
                self.simbolo_actual += self.caracter_actual
            elif self.caracter_actual.isdigit():
                self.estado = 2
                self.simbolo_actual += self.caracter_actual
            elif self.caracter_actual in '+-':
                self.aceptar(TipoSimbolo.OPERADOR_SUMA)
            elif self.caracter_actual in '*/':
                self.aceptar(TipoSimbolo.OPERADOR_MULTIPLICACION)
            elif self.caracter_actual in '<>':
                self.estado = 5
                self.simbolo_actual += self.caracter_actual
            elif self.caracter_actual == '|':
                self.estado = 6
                self.simbolo_actual += self.caracter_actual
            elif self.caracter_actual == '&':
                self.estado = 7
                self.simbolo_actual += self.caracter_actual
            elif self.caracter_actual == '!':
                self.estado = 8
                self.simbolo_actual += self.caracter_actual
            elif self.caracter_actual == ';':
                self.aceptar(TipoSimbolo.PUNTO_Y_COMA)
            elif self.caracter_actual == ',':
                self.aceptar(TipoSimbolo.COMA)
            elif self.caracter_actual == '(':
                self.aceptar(TipoSimbolo.PARENTESIS_ABIERTO)
            elif self.caracter_actual == ')':
                self.aceptar(TipoSimbolo.PARENTESIS_CERRADO)
            elif self.caracter_actual == '{':
                self.aceptar(TipoSimbolo.LLAVE_ABIERTA)
            elif self.caracter_actual == '}':
                self.aceptar(TipoSimbolo.LLAVE_CERRADA)
            elif self.caracter_actual == '=':
                self.estado = 9
                self.simbolo_actual += self.caracter_actual
            elif self.caracter_actual == '$':
                self.aceptar(TipoSimbolo.FIN_ENTRADA)
        elif self.estado == 1:
            if self.caracter_actual.isalpha() or self.caracter_actual.isdigit():
                self.estado = 1
                self.simbolo_actual += self.caracter_actual
            else:
                if self.simbolo_actual in ["int", "float", "void"]:
                    self.aceptar(TipoSimbolo.TIPO)
                else:
                    self.aceptar(TipoSimbolo.IDENTIFICADOR)
                if self.simbolo_actual == "if":
                    self.aceptar(TipoSimbolo.PALABRA_IF)
                elif self.simbolo_actual == "while":
                    self.aceptar(TipoSimbolo.PALABRA_WHILE)
                elif self.simbolo_actual == "return":
                    self.aceptar(TipoSimbolo.PALABRA_RETURN)
                elif self.simbolo_actual == "else":
                    self.aceptar(TipoSimbolo.PALABRA_ELSE)
        elif self.estado == 2:
            if self.caracter_actual.isdigit():
                self.estado = 2
                self.simbolo_actual += self.caracter_actual
            elif self.caracter_actual == '.':
                self.estado = 3
                self.simbolo_actual += self.caracter_actual
            else:
                self.aceptar(TipoSimbolo.ENTERO)
        elif self.estado == 3:
            if self.caracter_actual.isdigit():
                self.estado = 4
                self.simbolo_actual += self.caracter_actual
        elif self.estado == 4:
            if self.caracter_actual.isdigit():
                self.estado = 4
                self.simbolo_actual += self.caracter_actual
            else:
                self.aceptar(TipoSimbolo.FLOTANTE)
        elif self.estado == 5:
            if self.caracter_actual != '=':
                self.aceptar(TipoSimbolo.OPERADOR_RELACIONAL)
            else:
                self.aceptar(TipoSimbolo.OPERADOR_RELACIONAL)
        elif self.estado == 6:
            if self.caracter_actual != '|':
                self.aceptar(TipoSimbolo.ERROR)
            else:
                self.aceptar(TipoSimbolo.OPERADOR_O)
        elif self.estado == 7:
            if self.caracter_actual != '&':
                self.aceptar(TipoSimbolo.ERROR)
            else:
                self.aceptar(TipoSimbolo.OPERADOR_Y)
        elif self.estado == 8:
            if self.caracter_actual != '=':
                self.aceptar(TipoSimbolo.OPERADOR_NEGACION)
            else:
                self.aceptar(TipoSimbolo.OPERADOR_IGUALDAD)
        elif self.estado == 9:
            if self.caracter_actual != '=':
                self.aceptar(TipoSimbolo.OPERADOR_ASIGNACION)
            else:
                self.aceptar(TipoSimbolo.OPERADOR_IGUALDAD)

    def determinar_tipo_simbolo(self):
        pass

    def aceptar(self, tipo_simbolo):
        self.tipo_simbolo = tipo_simbolo
        self.en_ejecucion = False

    def entrada_terminada(self):
        return self.indice_actual >= len(self.fuente_entrada)
