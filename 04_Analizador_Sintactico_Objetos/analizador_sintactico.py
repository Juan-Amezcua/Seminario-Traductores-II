# analizador_sintactico.py

from categoria_token import CategoriaToken
from analizador_lexico import AnalizadorLexico

class ElementoPila:
    def mostrar(self):
        pass

class Terminal(ElementoPila):
    def __init__(self, simbolo):
        self.simbolo = simbolo  # El símbolo en sí, por ejemplo, 'id', '+', etc.

    def mostrar(self):
        return self.simbolo

class NoTerminal(ElementoPila):
    def __init__(self, simbolo):
        self.simbolo = simbolo  # El símbolo en sí, por ejemplo, 'E', 'T', etc.

    def mostrar(self):
        return self.simbolo

class Estado(ElementoPila):
    def __init__(self, numero_estado):
        self.numero_estado = numero_estado  # El número de estado, por ejemplo, 0, 1, 2, etc.

    def mostrar(self):
        return str(self.numero_estado)

class AnalizadorSintactico:
    def __init__(self, analizador_lexico, gramatica='gramatica1'):
        self.analizador_lexico = analizador_lexico
        self.pila = []
        self.aceptado = False

        # Mapa de símbolos a sus índices en la tabla de análisis
        self.simbolo_a_columna = {
            'id': 0,
            '+': 1,
            '$': 2,
            'E': 3,
        }

        if gramatica == 'gramatica1':
            # Tabla de análisis para Gramática 1: E → id + id
            # Estados: 0-4
            # Tokens: id(0), +(1), $(2), E(3)
            self.tabla = [
                [2, 0, 0, 1],   # Estado 0
                [0, 0, -1, 0],  # Estado 1
                [0, 3, 0, 0],   # Estado 2
                [4, 0, 0, 0],   # Estado 3
                [0, 0, -2, 0],  # Estado 4
            ]
            # Producciones
            # Acción -1: aceptar
            # Acción -2: reducir por producción 1: E → id + id
            self.producciones = {
                -2: ('E', 3),  # Producción: E → id + id
            }
        elif gramatica == 'gramatica2':
            # Tabla de análisis para Gramática 2: E → id + E | id
            self.tabla = [
                [2, 0, 0, 1],   # Estado 0
                [0, 0, -1, 0],  # Estado 1
                [0, 3, -3, 0],  # Estado 2
                [2, 0, 0, 4],   # Estado 3
                [0, 0, -2, 0],  # Estado 4
            ]
            # Producciones
            # Acción -1: aceptar
            # Acción -2: reducir por producción 1: E → id + E
            # Acción -3: reducir por producción 0: E → id
            self.producciones = {
                -2: ('E', 3),  # Producción: E → id + E
                -3: ('E', 1),  # Producción: E → id
            }
        else:
            raise ValueError("Gramática desconocida especificada.")

    def analizar(self):
        self.pila = [Terminal('$'), Estado(0)]  # Pila inicializada con [$, 0]
        self.siguiente_token()

        while not self.aceptado:
            elemento_estado = self.pila[-1]
            if isinstance(elemento_estado, Estado):
                estado = elemento_estado.numero_estado
            else:
                print("Error: Se esperaba un Estado en la cima de la pila")
                return

            simbolo_str = self.obtener_simbolo_desde_tipo_token(self.tipo_token_actual)
            if simbolo_str is None:
                print(f"Error: Token desconocido {self.token_actual}")
                return

            token = Terminal(simbolo_str)
            indice_token = self.simbolo_a_columna.get(simbolo_str)
            if indice_token is None:
                print(f"Error: Símbolo desconocido {simbolo_str}")
                return

            accion = self.obtener_accion(estado, indice_token)

            self.mostrar_pila()
            print(f"Entrada: {self.token_actual}")
            print(f"Acción: {accion}")

            if accion is None:
                print("Error: Acción inválida (celda vacía)")
                return

            if accion > 0:
                # Desplazar
                self.pila.append(token)    # Apilar token
                self.pila.append(Estado(accion))   # Apilar estado
                self.siguiente_token()
            elif accion < 0:
                if accion == -1:
                    print("Aceptar")
                    self.aceptado = True
                    return
                else:
                    # Realizar reducción
                    produccion = self.producciones.get(accion)
                    if produccion is None:
                        print("Error: Producción desconocida")
                        return
                    simbolo_lhs, longitud_rhs = produccion
                    # Desapilar 2 * longitud_rhs elementos de la pila (estado y símbolo por cada uno)
                    for _ in range(longitud_rhs * 2):
                        self.pila.pop()
                    # Obtener el siguiente estado de la cima de la pila
                    elemento_estado = self.pila[-1]
                    if isinstance(elemento_estado, Estado):
                        estado = elemento_estado.numero_estado
                    else:
                        print("Error: Se esperaba un Estado en la cima de la pila después de la reducción")
                        return
                    lhs = NoTerminal(simbolo_lhs)
                    indice_lhs = self.simbolo_a_columna.get(simbolo_lhs)
                    if indice_lhs is None:
                        print(f"Error: Símbolo desconocido {simbolo_lhs}")
                        return
                    estado_ir_a = self.obtener_accion(estado, indice_lhs)
                    if estado_ir_a is None or estado_ir_a == 0:
                        print("Error: 'ir_a' inválido")
                        return
                    self.pila.append(lhs)
                    self.pila.append(Estado(estado_ir_a))
            else:
                print("Error: Acción inválida")
                return

    def obtener_accion(self, estado, token):
        if estado < len(self.tabla) and token < len(self.tabla[estado]):
            accion = self.tabla[estado][token]
            return accion
        else:
            return None

    def siguiente_token(self):
        tipo_token = self.analizador_lexico.obtener_siguiente_token()
        self.token_actual = self.analizador_lexico.token_actual
        self.tipo_token_actual = tipo_token
        # Omitir tokens de espacio en blanco si es necesario
        while self.token_actual.strip() == '':
            tipo_token = self.analizador_lexico.obtener_siguiente_token()
            self.token_actual = self.analizador_lexico.token_actual
            self.tipo_token_actual = tipo_token

    def obtener_simbolo_desde_tipo_token(self, tipo_token):
        if tipo_token == CategoriaToken.IDENTIFICADOR:
            return 'id'
        elif tipo_token == CategoriaToken.OPERADOR_ADITIVO:
            return '+'
        elif tipo_token == CategoriaToken.FIN_DE_ENTRADA:
            return '$'
        else:
            return None

    def mostrar_pila(self):
        pila_str = ''
        for elem in self.pila:
            pila_str += elem.mostrar()
        print(pila_str)
        print("------------------------")
