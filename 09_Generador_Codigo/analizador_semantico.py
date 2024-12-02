# analizador_semantico.py

from tabla_simbolos import TablaSimbolos
from analizador_sintactico import NodoArbolSintactico

class AnalizadorSemantico:
    def __init__(self, raiz):
        self.raiz = raiz
        self.tabla_simbolos = TablaSimbolos()
        self.errores = []
        self.funcion_actual = None  # Mantener seguimiento de la función actual para verificar el tipo de retorno

    def analizar(self):
        self.visitar(self.raiz)
        self.reportar_errores()

    def visitar(self, nodo):
        nombre_metodo = f'visitar_{nodo.simbolo}'
        visitador = getattr(self, nombre_metodo, self.visita_generica)
        return visitador(nodo)

    def visita_generica(self, nodo):
        for hijo in nodo.hijos:
            self.visitar(hijo)

    # Implementación de las primeras 10 reglas

    # Regla 1: programa -> Definiciones
    def visitar_programa(self, nodo):
        self.visitar(nodo.hijos[0])  # Definiciones

    # Reglas 2 y 3: Definiciones -> Definicion Definiciones | ε
    def visitar_Defs(self, nodo):
        if len(nodo.hijos) == 0:
            # Producción vacía (épsilon), no hacer nada
            pass
        else:
            # Definicion Definiciones
            self.visitar(nodo.hijos[0])  # Definicion
            self.visitar(nodo.hijos[1])  # Definiciones

    visitar_Defs.__name__ = 'visitar_Defs'  # Manejar posibles problemas de nombres

    def visitar_Definiciones(self, nodo):
        return self.visitar_Defs(nodo)

    # Reglas 4 y 5: Definicion -> DefVar | DefFunc
    def visitar_Definicion(self, nodo):
        self.visitar(nodo.hijos[0])  # Puede ser DefVar o DefFunc

    # Regla 6: DefVar -> TIPO ListaVar ;
    def visitar_DefVar(self, nodo):
        nodo_tipo = nodo.hijos[0]
        tipo = nodo_tipo.simbolo  # Por ejemplo, 'int', 'float'

        nodo_ident = nodo.hijos[1]
        nombre_var = nodo_ident.simbolo  # Nombre de la variable
        nombres_vars = [nombre_var]

        nodo_lista_var = nodo.hijos[2]
        nombres_vars.extend(self.recolectar_vars_de_ListaVar(nodo_lista_var))

        for nombre_var in nombres_vars:
            self.declarar_variable(nombre_var, tipo)

    # Función auxiliar para recolectar nombres de variables desde ListaVar
    def recolectar_vars_de_ListaVar(self, nodo):
        nombres_vars = []
        if len(nodo.hijos) == 0:
            return nombres_vars
        else:
            if nodo.hijos[0].simbolo == ',':
                nodo_ident = nodo.hijos[1]
                nombre_var = nodo_ident.simbolo
                nombres_vars.append(nombre_var)
                if len(nodo.hijos) > 2:
                    nombres_vars.extend(self.recolectar_vars_de_ListaVar(nodo.hijos[2]))
        return nombres_vars

    # Regla 9: DefFunc -> TIPO ident ( Parametros ) BloqFunc
    def visitar_DefFunc(self, nodo):
        nodo_tipo = nodo.hijos[0]
        tipo = nodo_tipo.simbolo  # Tipo de retorno de la función

        nodo_ident = nodo.hijos[1]
        nombre_funcion = nodo_ident.simbolo  # Nombre de la función

        nodo_parametros = nodo.hijos[3]  # Los parámetros están en el índice 3

        # Recolectar información de parámetros (sin declarar aún los parámetros)
        info_parametros = self.recolectar_parametros(nodo_parametros)

        # Declarar la función en la tabla de símbolos con parámetros
        info_simbolo_funcion = {
            'tipo': tipo,
            'clase': 'funcion',
            'parametros': info_parametros,
            'nombre': nombre_funcion,
            'nivel_ambito': self.tabla_simbolos.nivel_ambito
        }
        try:
            self.tabla_simbolos.declarar(nombre_funcion, info_simbolo_funcion)
        except Exception as e:
            self.errores.append(str(e))

        # Establecer la función actual para verificar el tipo de retorno e incluir parámetros
        self.funcion_actual = {'tipo': tipo, 'nombre': nombre_funcion, 'parametros': info_parametros}

        # Entrar a un nuevo ámbito para la función
        self.tabla_simbolos.entrar_ambito()

        # Declarar parámetros en el ámbito de la función
        for indice, parametro in enumerate(self.funcion_actual['parametros']):
            info_parametro = {
                'tipo': parametro['tipo'],
                'clase': 'parametro',
                'funcion': nombre_funcion,
                'indice_parametro': indice,
                'nivel_ambito': self.tabla_simbolos.nivel_ambito
            }
            try:
                self.tabla_simbolos.declarar(parametro['nombre'], info_parametro)
            except Exception as e:
                self.errores.append(str(e))

        # Procesar el bloque de la función
        nodo_bloq_func = nodo.hijos[5]  # El bloque de la función está en el índice 5
        self.visitar(nodo_bloq_func)

        # Salir del ámbito de la función
        self.tabla_simbolos.salir_ambito()

        # Limpiar la función actual
        self.funcion_actual = None

    # Regla 10: Parametros -> ListaParam | ε
    def visitar_Parametros(self, nodo):
        if len(nodo.hijos) == 0:
            # Producción vacía (épsilon)
            return []
        else:
            return self.recolectar_parametros(nodo.hijos[0])  # ListaParam

    def recolectar_parametros(self, nodo):
        parametros = []
        if len(nodo.hijos) == 2:
            # ListaParam -> TIPO ident
            nodo_tipo = nodo.hijos[0]
            tipo = nodo_tipo.simbolo
            nodo_ident = nodo.hijos[1]
            nombre_parametro = nodo_ident.simbolo
            parametros.append({'tipo': tipo, 'nombre': nombre_parametro})
        elif len(nodo.hijos) == 4:
            # ListaParam -> TIPO ident , ListaParam
            nodo_tipo = nodo.hijos[0]
            tipo = nodo_tipo.simbolo
            nodo_ident = nodo.hijos[1]
            nombre_parametro = nodo_ident.simbolo
            parametros.append({'tipo': tipo, 'nombre': nombre_parametro})
            parametros.extend(self.recolectar_parametros(nodo.hijos[3]))  # Saltar ',' en el índice 2
        return parametros

    # Regla 14: BloqFunc -> { DefLocales }
    def visitar_BloqFunc(self, nodo):
        # No entrar ni salir de un ámbito aquí, ya que ya estamos en el ámbito de la función
        nodo_def_locales = nodo.hijos[1]  # Asumiendo que hijos[0] es '{', hijos[1] es DefLocales
        self.visitar(nodo_def_locales)

    # Reglas 15 y 16: DefLocales -> ε | DefLocal DefLocales
    def visitar_DefLocales(self, nodo):
        if len(nodo.hijos) == 0:
            # Producción vacía
            pass
        else:
            # DefLocales -> DefLocal DefLocales
            nodo_def_local = nodo.hijos[0]
            self.visitar(nodo_def_local)
            nodo_def_locales = nodo.hijos[1]
            self.visitar(nodo_def_locales)

    # Reglas 17 y 18: DefLocal -> DefVar | Sentencia
    def visitar_DefLocal(self, nodo):
        # DefLocal -> DefVar | Sentencia
        self.visitar(nodo.hijos[0])

    # Reglas 19 y 20: Sentencias -> ε | Sentencia Sentencias
    def visitar_Sentencias(self, nodo):
        if len(nodo.hijos) == 0:
            # Producción vacía
            pass
        else:
            # Sentencias -> Sentencia Sentencias
            nodo_sentencia = nodo.hijos[0]
            self.visitar(nodo_sentencia)
            nodo_sentencias = nodo.hijos[1]
            self.visitar(nodo_sentencias)

    # Regla 26: Otro -> else SentenciaBloque | ε
    def visitar_Otro(self, nodo):
        if len(nodo.hijos) == 0:
            # Producción vacía
            pass
        else:
            # else SentenciaBloque
            nodo_sentencia_bloque = nodo.hijos[1]
            self.visitar(nodo_sentencia_bloque)

    # Regla 27: SentenciaBloque -> Bloque | Sentencia
    def visitar_SentenciaBloque(self, nodo):
        self.visitar(nodo.hijos[0])  # Puede ser Bloque o Sentencia

    # Regla 28: Bloque -> { Sentencias }
    def visitar_Bloque(self, nodo):
        # Entrar a un nuevo ámbito para bloques anidados (por ejemplo, dentro de if o while)
        self.tabla_simbolos.entrar_ambito()
        nodo_sentencias = nodo.hijos[1]
        self.visitar(nodo_sentencias)
        self.tabla_simbolos.salir_ambito()

    # Regla 29: ValorRegresa -> Expresion | ε
    def visitar_ValorRegresa(self, nodo):
        if len(nodo.hijos) == 0:
            # Producción vacía
            return 'void'
        else:
            nodo_expresion = nodo.hijos[0]
            return self.visitar_Expresion(nodo_expresion)

    # Regla 30: Argumentos -> ListaArgumentos | ε
    def visitar_Argumentos(self, nodo):
        if len(nodo.hijos) == 0:
            # Producción vacía
            return []
        else:
            return self.visitar_ListaArgumentos(nodo.hijos[0])

    def visitar_Expresion(self, nodo):
        if len(nodo.hijos) == 1:
            # Regla: Expresion -> Termino
            return self.visitar_Termino(nodo.hijos[0])
        elif len(nodo.hijos) == 2:
            # Regla: Expresion -> opNot Expresion
            nodo_operador = nodo.hijos[0]
            nodo_operando = nodo.hijos[1]
            operador = nodo_operador.simbolo

            tipo_operando = self.visitar_Expresion(nodo_operando)
            if operador == '!':
                if tipo_operando == 'int':
                    return 'int'
                else:
                    self.errores.append("Error Semántico: El operador '!' requiere un operando de tipo 'int'.")
                    return None
            else:
                self.errores.append(f"Error Semántico: Operador unario desconocido '{operador}'.")
                return None
        elif len(nodo.hijos) == 3:
            # Operaciones binarias
            nodo_izquierdo = nodo.hijos[0]
            nodo_operador = nodo.hijos[1]
            nodo_derecho = nodo.hijos[2]

            tipo_izquierdo = self.visitar_Expresion(nodo_izquierdo)
            tipo_derecho = self.visitar_Expresion(nodo_derecho)
            operador = nodo_operador.simbolo

            tipo_resultado = self.verificar_operacion_binaria(tipo_izquierdo, tipo_derecho, operador)
            if tipo_resultado is None:
                self.errores.append(f"Error Semántico: Incompatibilidad de tipos en la operación '{operador}'.")
                return None
            else:
                return tipo_resultado
        else:
            self.errores.append("Error Semántico: Estructura de expresión inválida.")
            return None

    def verificar_operacion_binaria(self, tipo_izquierdo, tipo_derecho, operador):
        operadores_aritmeticos = ['+', '-', '*', '/']
        operadores_relacionales = ['<', '>', '<=', '>=']
        operadores_igualdad = ['==', '!=']
        operadores_logicos = ['&&', '||']

        if operador in operadores_aritmeticos:
            if tipo_izquierdo in ['int', 'float'] and tipo_derecho in ['int', 'float']:
                # Promover a float si algún operando es float
                if tipo_izquierdo == 'float' or tipo_derecho == 'float':
                    return 'float'
                else:
                    return 'int'
            else:
                return None  # Error de tipo
        elif operador in operadores_relacionales:
            if tipo_izquierdo in ['int', 'float', 'char'] and tipo_derecho in ['int', 'float', 'char']:
                return 'int'  # Asumiendo que 'int' representa booleano
            else:
                return None
        elif operador in operadores_igualdad:
            if tipo_izquierdo == tipo_derecho:
                return 'int'  # Resultado es booleano
            else:
                return None
        elif operador in operadores_logicos:
            if tipo_izquierdo == 'int' and tipo_derecho == 'int':
                return 'int'
            else:
                return None
        else:
            return None  # Operador desconocido

    # ===================================
    # Otros Métodos de Análisis Semántico
    # ===================================

    def declarar_variable(self, nombre_var, tipo):
        info = {
            'tipo': tipo,
            'clase': 'variable',
            'funcion': self.funcion_actual['nombre'] if self.funcion_actual else None,
            'nivel_ambito': self.tabla_simbolos.nivel_ambito
        }
        try:
            self.tabla_simbolos.declarar(nombre_var, info)
        except Exception as e:
            self.errores.append(str(e))

    # Sentencias de Asignación (Regla 21)
    def visitar_Sentencia(self, nodo):
        primer_hijo = nodo.hijos[0]
        if len(nodo.hijos) == 4 and nodo.hijos[1].simbolo == '=':
            # Regla 21: Sentencia -> ident = Expresion ;
            nodo_ident = nodo.hijos[0]
            nombre_ident = nodo_ident.simbolo

            try:
                info_ident = self.tabla_simbolos.buscar(nombre_ident)
            except Exception as e:
                self.errores.append(str(e))
                info_ident = None  # Continuar verificando la expresión

            nodo_expresion = nodo.hijos[2]
            tipo_expresion = self.visitar_Expresion(nodo_expresion)

            if info_ident:
                # Verificación de tipos
                if info_ident['tipo'] != tipo_expresion:
                    self.errores.append(
                        f"Error Semántico: Incompatibilidad de tipos en la asignación a '{nombre_ident}'. Se esperaba '{info_ident['tipo']}', se obtuvo '{tipo_expresion}'."
                    )
        elif primer_hijo.simbolo == 'if':
            # Regla: Sentencia -> if ( Expresion ) SentenciaBloque Otro
            nodo_expresion = nodo.hijos[2]
            tipo_expresion = self.visitar_Expresion(nodo_expresion)

            if tipo_expresion != 'int':
                self.errores.append("Error Semántico: La condición en la sentencia 'if' debe ser de tipo 'int'.")

            nodo_sentencia_bloque = nodo.hijos[4]
            self.visitar_SentenciaBloque(nodo_sentencia_bloque)

            nodo_otro = nodo.hijos[5]
            self.visitar_Otro(nodo_otro)
        elif primer_hijo.simbolo == 'while':
            # Regla: Sentencia -> while ( Expresion ) SentenciaBloque
            nodo_expresion = nodo.hijos[2]
            tipo_expresion = self.visitar_Expresion(nodo_expresion)

            if tipo_expresion != 'int':
                self.errores.append("Error Semántico: La condición en la sentencia 'while' debe ser de tipo 'int'.")

            nodo_sentencia_bloque = nodo.hijos[4]
            self.visitar_SentenciaBloque(nodo_sentencia_bloque)
        elif primer_hijo.simbolo == 'return':
            # Regla: Sentencia -> return ValorRegresa ;
            nodo_valor_regresa = nodo.hijos[1]
            tipo_retorno = self.visitar_ValorRegresa(nodo_valor_regresa)

            if self.funcion_actual:
                tipo_retorno_esperado = self.funcion_actual['tipo']
                if tipo_retorno != tipo_retorno_esperado:
                    self.errores.append(
                        f"Error Semántico: El tipo de retorno '{tipo_retorno}' no coincide con el tipo de retorno de la función '{self.funcion_actual['nombre']}' que es '{tipo_retorno_esperado}'."
                    )
            else:
                self.errores.append("Error Semántico: La sentencia 'return' no está dentro de una función.")
        elif primer_hijo.simbolo == 'LlamadaFunc':
            # Regla: Sentencia -> LlamadaFunc ;
            nodo_llamada_func = nodo.hijos[0]
            self.visitar_LlamadaFunc(nodo_llamada_func)
        else:
            # Manejar otros tipos de Sentencia
            self.visita_generica(nodo)

    def visitar_Termino(self, nodo):
        if len(nodo.hijos) == 1:
            hijo = nodo.hijos[0]
            if hijo.simbolo == 'LlamadaFunc':
                return self.visitar_LlamadaFunc(hijo)
            elif len(hijo.hijos) == 0:
                # Nodo hoja
                valor_token = hijo.simbolo  # Usar hijo.simbolo
                if valor_token.isdigit():
                    return 'int'
                elif self.es_literal_flotante(valor_token):
                    return 'float'
                elif valor_token.startswith('"') and valor_token.endswith('"'):
                    return 'string'
                else:
                    nombre_ident = valor_token
                    try:
                        info_ident = self.tabla_simbolos.buscar(nombre_ident)
                        return info_ident['tipo']
                    except Exception as e:
                        self.errores.append(str(e))
                        return None
            else:
                self.errores.append(f"Error Semántico: Término inválido '{hijo.simbolo}'.")
                return None
        elif len(nodo.hijos) == 3 and nodo.hijos[0].simbolo == '(':
            # Manejar ( Expresion )
            return self.visitar_Expresion(nodo.hijos[1])
        else:
            self.errores.append("Error Semántico: Término inválido.")
            return None

    # Regla 30: Argumentos -> ListaArgumentos | ε
    def visitar_Argumentos(self, nodo):
        if len(nodo.hijos) == 0:
            # Producción vacía
            return []
        else:
            return self.visitar_ListaArgumentos(nodo.hijos[0])

    def visitar_ListaArgumentos(self, nodo):
        tipos_argumentos = []
        if len(nodo.hijos) == 1:
            # ListaArgumentos -> Expresion
            nodo_expresion = nodo.hijos[0]
            tipo_argumento = self.visitar_Expresion(nodo_expresion)
            tipos_argumentos.append(tipo_argumento)
        elif len(nodo.hijos) == 3:
            # ListaArgumentos -> Expresion , ListaArgumentos
            nodo_expresion = nodo.hijos[0]
            tipo_argumento = self.visitar_Expresion(nodo_expresion)
            tipos_argumentos.append(tipo_argumento)
            nodo_siguiente_lista_argumentos = nodo.hijos[2]  # Saltar ',' en el índice 1
            tipos_argumentos.extend(self.visitar_ListaArgumentos(nodo_siguiente_lista_argumentos))
        return tipos_argumentos

    # Manejo de Llamadas a Funciones (Regla 52)
    def visitar_LlamadaFunc(self, nodo):
        nodo_ident = nodo.hijos[0]
        nombre_funcion = nodo_ident.simbolo

        if nombre_funcion == 'print':
            # Manejar 'print' como una función incorporada
            nodo_argumentos = nodo.hijos[2]  # Saltar '(' en el índice 1
            tipos_argumentos = self.visitar_Argumentos(nodo_argumentos)
            if len(tipos_argumentos) != 1:
                self.errores.append(f"Error Semántico: 'print' espera 1 argumento, se recibieron {len(tipos_argumentos)}.")
            else:
                # Opcionalmente, se puede verificar si el tipo de argumento es aceptable
                pass  # Para simplicidad, aceptar cualquier tipo
            return 'void'  # 'print' retorna void
        else:
            # Código existente para manejar funciones definidas por el usuario
            try:
                info_funcion = self.tabla_simbolos.buscar(nombre_funcion)
                if info_funcion['clase'] != 'funcion':
                    self.errores.append(f"Error Semántico: '{nombre_funcion}' no es una función.")
                    return None
            except Exception as e:
                self.errores.append(str(e))
                return None

            nodo_argumentos = nodo.hijos[2]  # Saltar '(' en el índice 1
            tipos_argumentos = self.visitar_Argumentos(nodo_argumentos)

            # Verificar si los tipos de argumentos coinciden con los tipos de parámetros de la función
            tipos_parametros_esperados = [param['tipo'] for param in info_funcion.get('parametros', [])]
            if len(tipos_argumentos) != len(tipos_parametros_esperados):
                self.errores.append(
                    f"Error Semántico: Número incorrecto de argumentos en la llamada a '{nombre_funcion}'. Se esperaban {len(tipos_parametros_esperados)}, se recibieron {len(tipos_argumentos)}."
                )
                return info_funcion['tipo']

            for i, (tipo_arg, tipo_param) in enumerate(zip(tipos_argumentos, tipos_parametros_esperados), start=1):
                if tipo_arg != tipo_param:
                    self.errores.append(
                        f"Error Semántico: El argumento {i} en la llamada a '{nombre_funcion}' tiene tipo '{tipo_arg}', se esperaba '{tipo_param}'."
                    )
            return info_funcion['tipo']

    # Método para verificar si una cadena es un literal flotante
    def es_literal_flotante(self, s):
        try:
            float(s)
            return '.' in s
        except ValueError:
            return False

    def reportar_errores(self):
        if self.errores:
            print("Errores Semánticos:")
            for error in self.errores:
                print(error)
        else:
            print("Análisis Semántico completado exitosamente.")
