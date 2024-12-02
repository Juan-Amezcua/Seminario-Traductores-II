# generador_ir.py

class GeneradorIR:
    def __init__(self):
        self.contador_temporales = 0
        self.contador_etiquetas = 0
        self.codigo = []

    def nuevo_temporal(self):
        self.contador_temporales += 1
        return f"t{self.contador_temporales}"

    def nueva_etiqueta(self):
        self.contador_etiquetas += 1
        return f"L{self.contador_etiquetas}"

    def generar(self, raiz):
        self.generar_programa(raiz)

    def generar_programa(self, nodo):
        if nodo.simbolo == 'programa':
            self.generar_definiciones(nodo.hijos[0])  # Definiciones

    def generar_definiciones(self, nodo):
        if len(nodo.hijos) == 0:
            return
        else:
            self.generar_definicion(nodo.hijos[0])    # Definicion
            self.generar_definiciones(nodo.hijos[1])  # Definiciones

    def generar_definicion(self, nodo):
        nodo_def = nodo.hijos[0]
        if nodo_def.simbolo == 'DefFunc':
            self.generar_definicion_funcion(nodo_def)
        elif nodo_def.simbolo == 'DefVar':
            # Manejar definiciones de variables si es necesario
            pass

    def generar_definicion_funcion(self, nodo):
        nombre_funcion = nodo.hijos[1].simbolo
        self.codigo.append(f"func {nombre_funcion}:")
        # Los parámetros no se manejan en este ejemplo por simplicidad
        nodo_bloq_func = nodo.hijos[5]
        self.generar_bloque(nodo_bloq_func)
        self.codigo.append(f"endfunc {nombre_funcion}")

    def generar_bloque(self, nodo):
        # BloqFunc -> { DefLocales }
        nodo_def_locales = nodo.hijos[1]
        self.generar_def_locales(nodo_def_locales)

    def generar_def_locales(self, nodo):
        if len(nodo.hijos) == 0:
            return
        else:
            self.generar_def_local(nodo.hijos[0])    # DefLocal
            self.generar_def_locales(nodo.hijos[1])  # DefLocales

    def generar_def_local(self, nodo):
        nodo_local = nodo.hijos[0]
        if nodo_local.simbolo == 'DefVar':
            # Manejar declaraciones de variables
            self.generar_def_var(nodo_local)
        elif nodo_local.simbolo == 'Sentencia':
            self.generar_sentencia(nodo_local)

    def generar_def_var(self, nodo):
        # DefVar -> TIPO ListaVar ;
        tipo = nodo.hijos[0].simbolo
        nombre_var = nodo.hijos[1].simbolo
        self.codigo.append(f"{nombre_var} = 0")
        # Manejar ListaVar si es necesario

    def generar_sentencia(self, nodo):
        primer_hijo = nodo.hijos[0]
        if primer_hijo.simbolo == 'IDENTIFIER' and nodo.hijos[1].simbolo == '=':
            ident = primer_hijo.simbolo
            nodo_expr = nodo.hijos[2]
            lugar_expr = self.generar_expresion(nodo_expr)
            self.codigo.append(f"{ident} = {lugar_expr}")
        elif primer_hijo.simbolo == 'return':
            nodo_expr = nodo.hijos[1]
            lugar_expr = self.generar_expresion(nodo_expr)
            self.codigo.append(f"return {lugar_expr}")
        elif primer_hijo.simbolo == 'LlamadaFunc':
            self.generar_llamada_funcion(primer_hijo)
        else:
            # Manejar otras sentencias
            pass

    def generar_expresion(self, nodo):
        if len(nodo.hijos) == 3:
            nodo_izquierdo = nodo.hijos[0]
            nodo_op = nodo.hijos[1]
            nodo_derecho = nodo.hijos[2]

            lugar_izquierdo = self.generar_expresion(nodo_izquierdo)
            lugar_derecho = self.generar_expresion(nodo_derecho)
            temp = self.nuevo_temporal()
            op = nodo_op.simbolo  # Por ejemplo, '+', '-', '*', '/'

            self.codigo.append(f"{temp} = {lugar_izquierdo} {op} {lugar_derecho}")
            return temp
        elif len(nodo.hijos) == 1:
            # Es un Termino
            return self.generar_termino(nodo.hijos[0])
        else:
            # Manejar otros casos
            pass

    def generar_termino(self, nodo):
        hijo = nodo.hijos[0]
        if hijo.simbolo == 'IDENTIFIER' or hijo.simbolo.isdigit():
            return hijo.simbolo
        elif hijo.simbolo == 'LlamadaFunc':
            return self.generar_llamada_funcion(hijo)
        else:
            # Manejar otros casos
            pass

    def generar_llamada_funcion(self, nodo):
        nombre_funcion = nodo.hijos[0].simbolo
        nodo_argumentos = nodo.hijos[2]  # Los argumentos están en el índice 2
        lugares_argumentos = self.generar_argumentos(nodo_argumentos)
        for arg in lugares_argumentos:
            self.codigo.append(f"param {arg}")
        self.codigo.append(f"call {nombre_funcion}, {len(lugares_argumentos)}")
        if nombre_funcion != 'print':
            temp = self.nuevo_temporal()
            self.codigo.append(f"{temp} = call {nombre_funcion}")
            return temp
        else:
            return None

    def generar_argumentos(self, nodo):
        lugares_argumentos = []
        if len(nodo.hijos) == 1:
            nodo_expr = nodo.hijos[0]
            lugar_arg = self.generar_expresion(nodo_expr)
            lugares_argumentos.append(lugar_arg)
        elif len(nodo.hijos) == 3:
            nodo_expr = nodo.hijos[0]
            lugar_arg = self.generar_expresion(nodo_expr)
            lugares_argumentos.append(lugar_arg)
            lugares_argumentos.extend(self.generar_argumentos(nodo.hijos[2]))
        return lugares_argumentos
