from lexico import AnalizadorLexico, TipoSimbolo
from pila import Pila

tabla_transicion_r1 = [
    [2, 0, 0, 1],
    [0, 0, -1, 0],
    [0, 3, 0, 0],
    [4, 0, 0, 0],
    [0, 0, -2, 0]
]

tabla_transicion_r2 = [
    [2, 0, 0, 1],
    [0, 0, -1, 0],
    [0, 3, -3, 0],
    [2, 0, 0, 4],
    [0, 0, -2, 0]
]

class EstadoParser:
    def __init__(self):
        self.fila = 0
        self.columna = 0
        self.accion = 0
        self.aceptado = False

class Parser:
    def __init__(self, analizador_lexico, pila, tabla_transicion):
        self.analizador_lexico = analizador_lexico
        self.pila = pila
        self.tabla_transicion = tabla_transicion
        self.estado = EstadoParser()

    def analizar(self, cadena_entrada):
        self.analizador_lexico.establecer_entrada(cadena_entrada)
        self.pila.apilar(TipoSimbolo.FIN_ENTRADA)
        self.pila.apilar(0)
        self.analizador_lexico.obtener_siguiente_simbolo()

        while not self.estado.aceptado:
            self.ejecutar_paso()

        if self.estado.aceptado:
            print("Análisis Aceptado")

    def ejecutar_paso(self):
        self.estado.fila = self.pila.tope()
        self.estado.columna = self.analizador_lexico.tipo_simbolo
        self.estado.accion = self.tabla_transicion[self.estado.fila][self.estado.columna]

        self.pila.mostrar()
        print(f"Símbolo Actual de Entrada: {self.analizador_lexico.simbolo_actual}")
        print(f"Acción: {self.estado.accion}")

        if self.estado.accion == -1:
            self.estado.aceptado = True
        elif self.estado.accion > 0:
            self.ejecutar_accion_desplazar()
        else:
            self.ejecutar_accion_reducir(-self.estado.accion)

    def ejecutar_accion_desplazar(self):
        self.pila.apilar(self.analizador_lexico.tipo_simbolo)
        self.pila.apilar(self.estado.accion)
        self.analizador_lexico.obtener_siguiente_simbolo()

    def ejecutar_accion_reducir(self, cuenta_reduccion):
        for _ in range(cuenta_reduccion):
            self.pila.desapilar()

if __name__ == "__main__":
    pila = Pila()
    analizador_lexico = AnalizadorLexico()

    parser1 = Parser(analizador_lexico, pila, tabla_transicion_r1)
    parser1.analizar("hola + mundo")

    parser2 = Parser(analizador_lexico, pila, tabla_transicion_r2)
    parser2.analizar("a + b + c + d + e + f")

