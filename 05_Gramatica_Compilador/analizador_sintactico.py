# analizador_sintactico.py

from categoria_token import CategoriaToken
from analizador_lexico import AnalizadorLexico

class ElementoPila:
    def mostrar(self):
        pass

class Terminal(ElementoPila):
    def __init__(self, id_token, simbolo):
        self.id_token = id_token
        self.simbolo = simbolo  # El lexema real

    def mostrar(self):
        return f"{self.simbolo}{self.id_token}"

class NoTerminal(ElementoPila):
    def __init__(self, id_simbolo, simbolo):
        self.id_simbolo = id_simbolo
        self.simbolo = simbolo

    def mostrar(self):
        return f"{self.simbolo}{self.id_simbolo}"

class Estado(ElementoPila):
    def __init__(self, numero_estado):
        self.numero_estado = numero_estado

    def mostrar(self):
        return f"Estado{self.numero_estado}"

class AnalizadorSintactico:
    def __init__(self, analizador_lexico, archivo_lr='compilador.lr'):
        self.analizador_lexico = analizador_lexico
        self.pila = []
        self.aceptado = False
        self.producciones = {}
        self.tabla = []
        self.cargar_tabla_lr(archivo_lr)
    
    def cargar_tabla_lr(self, nombre_archivo):
        with open(nombre_archivo, 'r') as f:
            lineas = f.readlines()
        lineas = [linea.rstrip() for linea in lineas if linea.strip()]
        
        # Leer las reglas
        num_reglas = 53
        self.producciones = {}  # Reiniciar producciones
        for i in range(num_reglas):
            linea_regla = lineas[i]
            # Almacenar la línea de regla completa, se analizará durante la reducción
            numero_accion = - (i + 1)
            self.producciones[numero_accion] = linea_regla  # Usar índices negativos para números de acción
        
        # Leer la tabla de análisis sintáctico a partir de la línea 54 en adelante (índice 53)
        self.tabla = []
        for linea in lineas[num_reglas + 1:]:
            if linea:
                fila = list(map(int, linea.strip().split()))
                self.tabla.append(fila)
    
    def analizar(self):
        # Incluir el símbolo FIN_DE_ENTRADA en el fondo de la pila
        self.pila = [Terminal(CategoriaToken.FIN_DE_ENTRADA, '$'), Estado(0)]
        self.siguiente_token()
        while not self.aceptado:
            # Obtener el estado actual de la cima de la pila
            elemento_estado = self.pila[-1]
            if isinstance(elemento_estado, Estado):
                estado = elemento_estado.numero_estado
            else:
                print("Error: Se esperaba un Estado en la cima de la pila")
                return
            id_token = self.tipo_token_actual
            if id_token == CategoriaToken.TIPO_ERROR:
                print(f"Error Léxico: Token desconocido {self.token_actual}")
                return
            # Obtener acción de la tabla de análisis
            if estado < len(self.tabla) and id_token < len(self.tabla[estado]):
                accion = self.tabla[estado][id_token]
            else:
                print("Error: Acción inválida (celda vacía)")
                return
            self.mostrar_pila()
            print(f"Entrada: {self.token_actual}")
            print(f"Acción: {accion}")
            if accion == 0:
                print("Error: Acción inválida")
                return
            elif accion > 0:
                # Desplazar
                self.pila.append(Terminal(id_token, self.token_actual))
                self.pila.append(Estado(accion))
                self.siguiente_token()
            elif accion < 0:
                if accion == -1:
                    print("Aceptar")
                    self.aceptado = True
                    return
                else:
                    # Inicia el proceso de reducción según la acción obtenida
                    linea_regla = self.producciones.get(accion)
                    if linea_regla is None:
                        print(f"Error: Producción desconocida para la acción {accion}")
                        return
                    # Analizar la línea de regla
                    # Suponiendo que el formato de la regla es: 'LHS num RHS', ej., '27 3 DefVar'
                    # O 'DefVar -> TIPO ListaVar ;'
                    # Por simplicidad, analicemos como 'LHS -> RHS'
                    if '->' in linea_regla:
                        simbolo_lhs, _, simbolos_rhs = linea_regla.partition('->')
                        simbolo_lhs = simbolo_lhs.strip()
                        simbolos_rhs = simbolos_rhs.strip().split()
                        if simbolos_rhs == ['ε']:
                            longitud_rhs = 0
                        else:
                            longitud_rhs = len(simbolos_rhs)
                    else:
                        # Analiza la regla para determinar el número de símbolos a desapilar
                        partes = linea_regla.split()
                        if len(partes) >= 3:
                            simbolo_lhs = partes[2]
                            longitud_rhs = int(partes[1])
                        else:
                            print(f"Error: Formato de regla inválido: {linea_regla}")
                            return
                    # Obtener ID del símbolo LHS
                    id_lhs = self.obtener_id_simbolo(simbolo_lhs)
                    if id_lhs is None:
                        print(f"Error: Símbolo LHS desconocido: {simbolo_lhs}")
                        return
                    # Eliminar 2 * longitud_rhs elementos de la pila
                    elementos_a_eliminar = longitud_rhs * 2
                    if elementos_a_eliminar > len(self.pila) - 1:  # Ajustar por $ al fondo
                        print("Error: No hay suficientes elementos en la pila para reducir")
                        return
                    for _ in range(elementos_a_eliminar):
                        self.pila.pop()
                    # Obtener estado de la cima de la pila
                    elemento_estado = self.pila[-1]
                    if isinstance(elemento_estado, Estado):
                        estado = elemento_estado.numero_estado
                    else:
                        print("Error: Se esperaba un Estado en la cima de la pila después de la reducción")
                        return
                    # Obtener estado de transición
                    if estado < len(self.tabla) and id_lhs < len(self.tabla[estado]):
                        estado_ir_a = self.tabla[estado][id_lhs]
                    else:
                        print("Error: Acción 'ir_a' inválida")
                        return
                    if estado_ir_a == 0:
                        print("Error: Estado 'ir_a' inválido")
                        return
                    self.pila.append(NoTerminal(id_lhs, simbolo_lhs))
                    self.pila.append(Estado(estado_ir_a))
            else:
                print("Error: Acción inválida")
                return

    def obtener_id_simbolo(self, simbolo):
        mapa_id_simbolo = {
            # Mapear símbolos no terminales a sus IDs
            'programa': 24,
            'Definiciones': 25,
            'Definicion': 26,
            'DefVar': 27,
            'ListaVar': 28,
            'DefFunc': 29,
            'Parametros': 30,
            'ListaParam': 31,
            'BloqFunc': 32,
            'DefLocales': 33,
            'DefLocal': 34,
            'Sentencias': 35,
            'Sentencia': 36,
            'Otro': 37,
            'Bloque': 38,
            'ValorRegresa': 39,
            'Argumentos': 40,
            'ListaArgumentos': 41,
            'Termino': 42,
            'LlamadaFunc': 43,
            'SentenciaBloque': 44,
            'Expresion': 45,
            # Añadir otros símbolos no terminales según sea necesario
        }
        # Para terminales, podemos usar la CategoriaToken
        mapa_id_terminal = {k: v for k, v in CategoriaToken.__dict__.items() if not k.startswith('__') and not callable(getattr(CategoriaToken, k))}
        if simbolo in mapa_id_simbolo:
            return mapa_id_simbolo[simbolo]
        elif simbolo in mapa_id_terminal:
            return mapa_id_terminal[simbolo]
        else:
            return None

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

    def mostrar_pila(self):
        pila_str = ''
        for elem in self.pila:
            pila_str += elem.mostrar()
        print(pila_str)
        print("------------------------")
