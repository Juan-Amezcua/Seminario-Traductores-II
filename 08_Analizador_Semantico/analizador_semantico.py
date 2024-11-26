
# analizador_semantico.py

from categoria_token import CategoriaToken
from analizador_sintactico import NodoArbolSintactico

class TablaSimbolos:
    def __init__(self):
        self.ambitos = [{}]  # Pila de ámbitos (lista de diccionarios)

    def entrar_ambito(self):
        self.ambitos.append({})

    def salir_ambito(self):
        if len(self.ambitos) > 1:
            self.ambitos.pop()
        else:
            raise Exception("Error semántico: No se puede salir del ámbito global.")

    def declarar(self, nombre, informacion):
        ambito_actual = self.ambitos[-1]
        if nombre in ambito_actual:
            raise Exception(f"Error semántico: '{nombre}' ya está declarado en el ámbito actual.")
        ambito_actual[nombre] = informacion

    def buscar(self, nombre):
        for ambito in reversed(self.ambitos):
            if nombre in ambito:
                return ambito[nombre]
        raise Exception(f"Error semántico: '{nombre}' no está declarado.")


class AnalizadorSemantico:
    def __init__(self, raiz):
        self.raiz = raiz
        self.tabla_simbolos = TablaSimbolos()
        self.errores = []
        self.funcion_actual = None  # Lleva el seguimiento de la función actual para verificar el tipo de retorno

    def analizar(self):
        self.visitar(self.raiz)
        self.reportar_errores()

    def visitar(self, nodo):
        nombre_metodo = f'visitar_{nodo.simbolo}'
        visitante = getattr(self, nombre_metodo, self.visita_generica)
        return visitante(nodo)

    def visita_generica(self, nodo):
        for hijo in nodo.hijos:
            self.visitar(hijo)

    # Regla 1: programa -> Definiciones
    def visitar_programa(self, nodo):
        self.visitar(nodo.hijos[0])  # Definiciones

    # Reglas 2 y 3: Definiciones -> Definicion Definiciones | ε
    def visitar_Definiciones(self, nodo):
        if len(nodo.hijos) == 0:
            pass
        else:
            self.visitar(nodo.hijos[0])  # Definicion
            self.visitar(nodo.hijos[1])  # Definiciones

    # Reglas 4 y 5: Definicion -> DefVar | DefFunc
    def visitar_Definicion(self, nodo):
        self.visitar(nodo.hijos[0])  # DefVar o DefFunc

    # Regla 6: DefVar -> TIPO ListaVar ;
    def visitar_DefVar(self, nodo):
        tipo_nodo = nodo.hijos[0]
        tipo = tipo_nodo.simbolo # TIPO (por ejemplo, 'int', 'float')

        lista_var_nodo = nodo.hijos[1]
        nombres_variables = self.recolectar_vars_de_ListaVar(lista_var_nodo)

        for nombre_variable in nombres_variables:
            try:
                self.tabla_simbolos.declarar(nombre_variable, {'tipo': tipo, 'clase': 'variable'})
            except Exception as e:
                self.errores.append(str(e))

    # Función auxiliar para recolectar nombres de variables de ListaVar
    def recolectar_vars_de_ListaVar(self, nodo):
        nombres_variables = []
        if nodo.simbolo == 'ListaVar':
            # ListaVar -> ident | ident , ListaVar
            ident_nodo = nodo.hijos[0]
            nombre_variable = ident_nodo.simbolo
            nombres_variables.append(nombre_variable)
            if len(nodo.hijos) > 1:
                # Hay una coma y otra ListaVar
                siguiente_lista_var_nodo = nodo.hijos[2] # Saltar la coma
                nombres_variables.extend(self.recolectar_vars_de_ListaVar(siguiente_lista_var_nodo))
        return nombres_variables

    # Regla 9: DefFunc -> TIPO ident ( Parametros ) BloqFunc
    def visitar_DefFunc(self, nodo):
        tipo_nodo = nodo.hijos[0]
        tipo = tipo_nodo.simbolo

        ident_nodo = nodo.hijos[1]
        nombre_funcion = ident_nodo.simbolo

        try:
            self.tabla_simbolos.declarar(nombre_funcion, {'tipo': tipo, 'clase': 'funcion', 'parametros': []})
        except Exception as e:
            self.errores.append(str(e))

        self.tabla_simbolos.entrar_ambito()  # Entrar al ámbito de la función

        parametros_nodo = nodo.hijos[3]  # Saltar '(' en el índice 2
        self.visitar(parametros_nodo)  # Procesar los parámetros

        bloq_func_nodo = nodo.hijos[5]  # Saltar ')' en el índice 4
        self.visitar(bloq_func_nodo)  # Procesar el bloque de la función

        self.tabla_simbolos.salir_ambito()  # Salir del ámbito de la función

    # Regla 10: Parametros -> ListaParam | ε
    def visitar_Parametros(self, nodo):
        if len(nodo.hijos) == 0:
            # Producción vacía (epsilon), no hace nada
            pass
        else:
            self.visitar(nodo.hijos[0])  # ListaParam

    # Regla 11: Parametros -> ListaParam
    # Ya manejada en visitar_Parametros

    # Reglas 12 y 13: ListaParam -> TIPO ident | TIPO ident , ListaParam
    def visitar_ListaParam(self, nodo):
        if len(nodo.hijos) == 0:
            # Producción vacía (epsilon)
            pass
        else:
            # ListaParam -> TIPO ident
            tipo_nodo = nodo.hijos[0]
            tipo = tipo_nodo.simbolo  # TIPO (por ejemplo, 'int', 'float')
            ident_nodo = nodo.hijos[1]
            nombre_parametro = ident_nodo.simbolo

            try:
                self.tabla_simbolos.declarar(nombre_parametro, {'tipo': tipo, 'clase': 'parametro'})
            except Exception as e:
                self.errores.append(str(e))

            if len(nodo.hijos) > 2:
                # Hay una coma y otro ListaParam
                siguiente_lista_param_nodo = nodo.hijos[3]  # Saltar la coma en el índice 2
                self.visitar(siguiente_lista_param_nodo)

    # Regla 14: BloqFunc -> { DefLocales }
    def visitar_BloqFunc(self, nodo):
        # Entrar en un nuevo ámbito para el bloque de la función
        self.tabla_simbolos.entrar_ambito()
        def_locales_nodo = nodo.hijos[1]  # Asumiendo que hijos[0] es '{', hijos[1] es DefLocales
        self.visitar(def_locales_nodo)
        self.tabla_simbolos.salir_ambito()

    # Reglas 15 y 16: DefLocales -> ε | DefLocal DefLocales
    def visitar_DefLocales(self, nodo):
        if len(nodo.hijos) == 0:
            # Producción vacía
            pass
        else:
            # DefLocales -> DefLocal DefLocales
            def_local_nodo = nodo.hijos[0]
            self.visitar(def_local_nodo)
            def_locales_nodo = nodo.hijos[1]
            self.visitar(def_locales_nodo)

    # Reglas 17 y 18: DefLocal -> DefVar | Sentencia
    def visitar_DefLocal(self, nodo):
        # DefLocal -> DefVar o Sentencia
        self.visitar(nodo.hijos[0])

    # Reglas 19 y 20: Sentencias -> ε | Sentencia Sentencias
    def visitar_Sentencias(self, nodo):
        if len(nodo.hijos) == 0:
            # Producción vacía
            pass
        else:
            # Sentencias -> Sentencia Sentencias
            sentencia_nodo = nodo.hijos[0]
            self.visitar(sentencia_nodo)
            sentencias_nodo = nodo.hijos[1]
            self.visitar(sentencias_nodo)

    # Regla 21: Sentencia -> ident = Expresion ;
    def visitar_Sentencia(self, nodo):
        if len(nodo.hijos) == 4 and nodo.hijos[1].simbolo == '=':
            # Asignación
            ident_nodo = nodo.hijos[0]
            nombre_identificador = ident_nodo.simbolo

            try:
                informacion_identificador = self.tabla_simbolos.buscar(nombre_identificador)
            except Exception as e:
                self.errores.append(str(e))
                informacion_identificador = None  # Continuar para verificar la expresión

            expresion_nodo = nodo.hijos[2]
            tipo_expresion = self.visitar_Expresion(expresion_nodo)

            if informacion_identificador:
                # Comprobación de tipos
                if informacion_identificador['tipo'] != tipo_expresion:
                    self.errores.append(
                        f"Error semántico: Incompatibilidad de tipos en la asignación a '{nombre_identificador}'. "
                        f"Se esperaba '{informacion_identificador['tipo']}', pero se obtuvo '{tipo_expresion}'."
                    )
        else:
            # Otras Sentencias
            self.visita_generica(nodo)

    # Regla 22: Sentencia -> if ( Expresion ) SentenciaBloque Otro
    def visitar_Sentencia(self, nodo):
        if nodo.hijos[0].simbolo == 'if':
            expresion_nodo = nodo.hijos[2]
            tipo_expresion = self.visitar_Expresion(expresion_nodo)

            if tipo_expresion != 'int':
                self.errores.append(
                    "Error semántico: La condición en la sentencia 'if' debe ser de tipo 'int'."
                )

            sentencia_bloque_nodo = nodo.hijos[4]
            self.visitar(sentencia_bloque_nodo)

            otro_nodo = nodo.hijos[5]
            self.visitar(otro_nodo)
        else:
            self.visita_generica(nodo)

    # Regla 23: Sentencia -> while ( Expresion ) SentenciaBloque
    def visitar_Sentencia(self, nodo):
        if nodo.hijos[0].simbolo == 'while':
            expresion_nodo = nodo.hijos[2]
            tipo_expresion = self.visitar_Expresion(expresion_nodo)

            if tipo_expresion != 'int':
                self.errores.append(
                    "Error semántico: La condición en la sentencia 'while' debe ser de tipo 'int'."
                )

            sentencia_bloque_nodo = nodo.hijos[4]
            self.visitar(sentencia_bloque_nodo)
        else:
            self.visita_generica(nodo)

    # Regla 24: Sentencia -> return ValorRegresa ;
    def visitar_Sentencia(self, nodo):
        if nodo.hijos[0].simbolo == 'return':
            valor_regresa_nodo = nodo.hijos[1]
            tipo_retorno = self.visitar_ValorRegresa(valor_regresa_nodo)

            if self.funcion_actual:
                tipo_esperado = self.funcion_actual['tipo']
                if tipo_retorno != tipo_esperado:
                    self.errores.append(
                        f"Error semántico: El tipo de retorno '{tipo_retorno}' no coincide con el tipo "
                        f"esperado '{tipo_esperado}' en la función '{self.funcion_actual['nombre']}'."
                    )
            else:
                self.errores.append("Error semántico: La sentencia 'return' no está dentro de una función.")
        else:
            self.visita_generica(nodo)

    # Regla 25: Sentencia -> LlamadaFunc ;
    def visitar_Sentencia(self, nodo):
        if nodo.hijos[0].simbolo == 'LlamadaFunc':
            llamada_func_nodo = nodo.hijos[0]
            self.visitar_LlamadaFunc(llamada_func_nodo)
        else:
            self.visita_generica(nodo)

    # Regla 26: Otro -> else SentenciaBloque | ε
    def visitar_Otro(self, nodo):
        if len(nodo.hijos) == 0:
            # Producción vacía
            pass
        else:
            # else SentenciaBloque
            sentencia_bloque_nodo = nodo.hijos[1]
            self.visitar(sentencia_bloque_nodo)

    # Regla 27: SentenciaBloque -> Bloque | Sentencia
    def visitar_SentenciaBloque(self, nodo):
        self.visitar(nodo.hijos[0])  # Puede ser Bloque o Sentencia

    # Regla 28: Bloque -> { Sentencias }
    def visitar_Bloque(self, nodo):
        self.tabla_simbolos.entrar_ambito()
        sentencias_nodo = nodo.hijos[1]
        self.visitar(sentencias_nodo)
        self.tabla_simbolos.salir_ambito()

    # Regla 29: ValorRegresa -> Expresion | ε
    def visitar_ValorRegresa(self, nodo):
        if len(nodo.hijos) == 0:
            # Producción vacía
            return 'void'
        else:
            expresion_nodo = nodo.hijos[0]
            return self.visitar_Expresion(expresion_nodo)

    # Regla 30: Argumentos -> ListaArgumentos | ε
    def visitar_Argumentos(self, nodo):
        if len(nodo.hijos) == 0:
            # Producción vacía
            return []
        else:
            return self.visitar_ListaArgumentos(nodo.hijos[0])

    def visitar_Expresion(self, nodo):
        if len(nodo.hijos) == 1:
            # Regla 36, 37, 38: Expresion -> ident | number | LlamadaFunc
            return self.visitar_Termino(nodo.hijos[0])
        elif len(nodo.hijos) == 2:
            # Regla 43: Expresion -> opNot Expresion
            operador_nodo = nodo.hijos[0]
            operando_nodo = nodo.hijos[1]
            operador = operador_nodo.simbolo

            tipo_operando = self.visitar_Expresion(operando_nodo)
            if operador == '!':
                if tipo_operando == 'int':
                    return 'int'
                else:
                    self.errores.append("Error semántico: El operador '!' requiere un operando de tipo 'int'.")
                    return None
            else:
                self.errores.append(f"Error semántico: Operador unario desconocido '{operador}'.")
                return None
        elif len(nodo.hijos) == 3:
            # Reglas 31-34, 35, 39-40: Operaciones binarias y relacionales
            izquierda_nodo = nodo.hijos[0]
            operador_nodo = nodo.hijos[1]
            derecha_nodo = nodo.hijos[2]

            tipo_izquierda = self.visitar_Expresion(izquierda_nodo)
            tipo_derecha = self.visitar_Expresion(derecha_nodo)
            operador = operador_nodo.simbolo

            tipo_resultado = self.verificar_operacion_binaria(tipo_izquierda, tipo_derecha, operador)
            if tipo_resultado is None:
                self.errores.append(f"Error semántico: Incompatibilidad de tipos en la operación '{operador}'.")
                return None
            else:
                return tipo_resultado
        else:
            self.errores.append("Error semántico: Estructura de expresión inválida.")
            return None

    def visitar_Termino(self, nodo):
        # Termino puede ser ident, número, cadena, carácter o LlamadaFunc
        hijo = nodo.hijos[0]
        if hijo.simbolo == 'ident':
            nombre_identificador = hijo.hijos[0].simbolo  # Se asume que el hijo tiene el identificador como símbolo
            try:
                informacion_identificador = self.tabla_simbolos.buscar(nombre_identificador)
                return informacion_identificador['tipo']
            except Exception as e:
                self.errores.append(str(e))
                return None
        elif hijo.simbolo == 'number':
            valor_numero = hijo.hijos[0].simbolo
            if self.es_literal_flotante(valor_numero):
                return 'float'
            else:
                return 'int'
        elif hijo.simbolo == 'LlamadaFunc':
            return self.visitar_LlamadaFunc(hijo)
        elif hijo.simbolo == '(':
            # Regla 35: Expresion -> ( Expresion )
            expresion_nodo = nodo.hijos[1]
            return self.visitar_Expresion(expresion_nodo)
        else:
            self.errores.append(f"Error semántico: Término desconocido '{hijo.simbolo}'.")
            return None

    # Método auxiliar para verificar operaciones binarias
    def verificar_operacion_binaria(self, tipo_izquierda, tipo_derecha, operador):
        operadores_aritmeticos = ['+', '-', '*', '/']
        operadores_relacionales = ['<', '>', '<=', '>=']
        operadores_igualdad = ['==', '!=']

        if operador in operadores_aritmeticos:
            if tipo_izquierda in ['int', 'float'] and tipo_derecha in ['int', 'float']:
                # Promoción a float si alguno de los operandos es float
                return 'float' if 'float' in [tipo_izquierda, tipo_derecha] else 'int'
            return None  # Error de tipo
        elif operador in operadores_relacionales:
            if tipo_izquierda in ['int', 'float'] and tipo_derecha in ['int', 'float']:
                return 'int'  # Se asume que 'int' representa un booleano
            return None
        elif operador in operadores_igualdad:
            if tipo_izquierda == tipo_derecha:
                return 'int'  # Resultado booleano
            return None
        else:
            self.errores.append(f"Error semántico: Operador desconocido '{operador}'.")
            return None

    def visitar_DefFunc(self, nodo):
        tipo_nodo = nodo.hijos[0]
        tipo = tipo_nodo.simbolo

        ident_nodo = nodo.hijos[1]
        nombre_funcion = ident_nodo.simbolo

        parametros_nodo = nodo.hijos[3]  # Los parámetros están en el índice 3

        # Recolectar información de los parámetros
        informacion_parametros = self.recolectar_parametros(parametros_nodo)

        try:
            self.tabla_simbolos.declarar(nombre_funcion, {
                'tipo': tipo,
                'clase': 'funcion',
                'parametros': informacion_parametros,
                'nombre': nombre_funcion
            })
        except Exception as e:
            self.errores.append(str(e))

        # Establecer la función actual para verificar el tipo de retorno
        self.funcion_actual = {'tipo': tipo, 'nombre': nombre_funcion}

        self.tabla_simbolos.entrar_ambito()  # Entrar al ámbito de la función

        # Declarar parámetros en el ámbito de la función
        for parametro in informacion_parametros:
            try:
                self.tabla_simbolos.declarar(parametro['nombre'], {
                    'tipo': parametro['tipo'],
                    'clase': 'parametro'
                })
            except Exception as e:
                self.errores.append(str(e))

        bloque_funcion_nodo = nodo.hijos[5]  # El bloque de la función está en el índice 5
        self.visitar(bloque_funcion_nodo)  # Procesar el bloque de la función

        self.tabla_simbolos.salir_ambito()  # Salir del ámbito de la función

        # Limpiar la función actual
        self.funcion_actual = None

    # Recolectar parámetros (Reglas 10 y 11)
    def recolectar_parametros(self, nodo):
        # Recolectar tipos y nombres de parámetros
        parametros = []
        if nodo.simbolo == 'Parametros' and len(nodo.hijos) > 0:
            lista_param_nodo = nodo.hijos[0]
            parametros = self.visitar_ListaParam(lista_param_nodo)
        return parametros

    def visitar_ListaParam(self, nodo):
        # Regla 11: ListaParam -> TIPO ident | TIPO ident , ListaParam
        parametros = []
        if len(nodo.hijos) == 2:
            # ListaParam -> TIPO ident
            tipo_nodo = nodo.hijos[0]
            tipo = tipo_nodo.simbolo
            ident_nodo = nodo.hijos[1]
            nombre_parametro = ident_nodo.simbolo
            parametros.append({'tipo': tipo, 'nombre': nombre_parametro})
        elif len(nodo.hijos) == 4:
            # ListaParam -> TIPO ident , ListaParam
            tipo_nodo = nodo.hijos[0]
            tipo = tipo_nodo.simbolo
            ident_nodo = nodo.hijos[1]
            nombre_parametro = ident_nodo.simbolo
            parametros.append({'tipo': tipo, 'nombre': nombre_parametro})
            parametros.extend(self.visitar_ListaParam(nodo.hijos[3]))  # Saltar ',' en el índice 2
        return parametros

    # Sentencias de asignación, control y retorno
    def visitar_Sentencia(self, nodo):
        if len(nodo.hijos) == 4 and nodo.hijos[1].simbolo == '=':
            # Regla 21: Sentencia -> ident = Expresion ;
            ident_nodo = nodo.hijos[0]
            nombre_identificador = ident_nodo.simbolo

            try:
                informacion_identificador = self.tabla_simbolos.buscar(nombre_identificador)
            except Exception as e:
                self.errores.append(str(e))
                informacion_identificador = None  # Continuar verificando la expresión

            expresion_nodo = nodo.hijos[2]
            tipo_expresion = self.visitar_Expresion(expresion_nodo)

            if informacion_identificador:
                # Verificación de tipos
                if informacion_identificador['tipo'] != tipo_expresion:
                    self.errores.append(
                        f"Error semántico: Incompatibilidad de tipos en la asignación a '{nombre_identificador}'. "
                        f"Se esperaba '{informacion_identificador['tipo']}', pero se obtuvo '{tipo_expresion}'."
                    )
        elif nodo.hijos[0].simbolo == 'if':
            # Regla 22: Sentencia -> if ( Expresion ) SentenciaBloque Otro
            expresion_nodo = nodo.hijos[2]
            tipo_expresion = self.visitar_Expresion(expresion_nodo)

            if tipo_expresion != 'int':
                self.errores.append("Error semántico: La condición en la sentencia 'if' debe ser de tipo 'int'.")

            sentencia_bloque_nodo = nodo.hijos[4]
            self.visitar(sentencia_bloque_nodo)

            otro_nodo = nodo.hijos[5]
            self.visitar(otro_nodo)
        elif nodo.hijos[0].simbolo == 'while':
            # Regla 23: Sentencia -> while ( Expresion ) SentenciaBloque
            expresion_nodo = nodo.hijos[2]
            tipo_expresion = self.visitar_Expresion(expresion_nodo)

            if tipo_expresion != 'int':
                self.errores.append("Error semántico: La condición en la sentencia 'while' debe ser de tipo 'int'.")

            sentencia_bloque_nodo = nodo.hijos[4]
            self.visitar(sentencia_bloque_nodo)
        elif nodo.hijos[0].simbolo == 'return':
            # Regla 24: Sentencia -> return ValorRegresa ;
            valor_regresa_nodo = nodo.hijos[1]
            tipo_retorno = self.visitar_ValorRegresa(valor_regresa_nodo)

            if self.funcion_actual:
                tipo_esperado = self.funcion_actual['tipo']
                if tipo_retorno != tipo_esperado:
                    self.errores.append(
                        f"Error semántico: El tipo de retorno '{tipo_retorno}' no coincide con el tipo "
                        f"esperado '{tipo_esperado}' en la función '{self.funcion_actual['nombre']}'."
                    )
            else:
                self.errores.append("Error semántico: La sentencia 'return' no está dentro de una función.")
        elif nodo.hijos[0].simbolo == 'LlamadaFunc':
            # Regla 25: Sentencia -> LlamadaFunc ;
            llamada_func_nodo = nodo.hijos[0]
            self.visitar_LlamadaFunc(llamada_func_nodo)
        else:
            # Manejar otros tipos de Sentencia
            self.visita_generica(nodo)

    # Otro -> else SentenciaBloque | ε
    def visitar_Otro(self, nodo):
        if len(nodo.hijos) == 0:
            # Producción vacía
            pass
        else:
            # else SentenciaBloque
            sentencia_bloque_nodo = nodo.hijos[1]
            self.visitar(sentencia_bloque_nodo)

    # SentenciaBloque -> Bloque | Sentencia
    def visitar_SentenciaBloque(self, nodo):
        self.visitar(nodo.hijos[0])  # Puede ser Bloque o Sentencia

    # Regla 28: Bloque -> { Sentencias }
    def visitar_Bloque(self, nodo):
        self.tabla_simbolos.entrar_ambito()
        sentencias_nodo = nodo.hijos[1]
        self.visitar(sentencias_nodo)
        self.tabla_simbolos.salir_ambito()

    # ValorRegresa -> Expresion | ε
    def visitar_ValorRegresa(self, nodo):
        if len(nodo.hijos) == 0:
            # Producción vacía
            return 'void'
        else:
            # ValorRegresa -> Expresion
            expresion_nodo = nodo.hijos[0]
            return self.visitar_Expresion(expresion_nodo)

    # Regla 30: Argumentos -> ListaArgumentos | ε
    def visitar_Argumentos(self, nodo):
        if len(nodo.hijos) == 0:
            # Producción vacía
            return []
        else:
            return self.visitar_ListaArgumentos(nodo.hijos[0])

    # Manejo de llamadas a funciones (Regla 52)
    def visitar_LlamadaFunc(self, nodo):
        ident_nodo = nodo.hijos[0]
        nombre_funcion = ident_nodo.simbolo

        try:
            informacion_funcion = self.tabla_simbolos.buscar(nombre_funcion)
            if informacion_funcion['clase'] != 'funcion':
                self.errores.append(f"Error semántico: '{nombre_funcion}' no es una función.")
                return None
        except Exception as e:
            self.errores.append(str(e))
            return None

        argumentos_nodo = nodo.hijos[2]  # Saltar '(' en el índice 1
        tipos_argumentos = self.visitar_Argumentos(argumentos_nodo)

        # Verificar si los tipos de argumentos coinciden con los parámetros de la función
        tipos_parametros_esperados = [param['tipo'] for param in informacion_funcion.get('parametros', [])]
        if len(tipos_argumentos) != len(tipos_parametros_esperados):
            self.errores.append(
                f"Error semántico: Número incorrecto de argumentos en la llamada a '{nombre_funcion}'. "
                f"Se esperaban {len(tipos_parametros_esperados)}, pero se obtuvieron {len(tipos_argumentos)}."
            )
            return informacion_funcion['tipo']

        for i, (tipo_arg, tipo_param) in enumerate(zip(tipos_argumentos, tipos_parametros_esperados)):
            if tipo_arg != tipo_param:
                self.errores.append(
                    f"Error semántico: El argumento {i+1} en la llamada a '{nombre_funcion}' tiene tipo "
                    f"'{tipo_arg}', pero se esperaba '{tipo_param}'."
                )
        return informacion_funcion['tipo']

    # Método para verificar si una cadena es un literal flotante
    def es_literal_flotante(self, s):
        try:
            float(s)
            return '.' in s
        except ValueError:
            return False

    # Método para reportar errores
    def reportar_errores(self):
        if self.errores:
            print("Errores semánticos:")
            for error in self.errores:
                print(error)
        else:
            print("El análisis semántico se completó exitosamente.")