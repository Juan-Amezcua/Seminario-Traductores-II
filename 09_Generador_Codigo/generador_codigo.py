# generador_codigo.py

from analizador_semantico import TablaSimbolos

class GeneradorCodigo:
    def __init__(self, codigo_ir, tabla_simbolos):
        self.codigo_ir = codigo_ir
        self.codigo_asm = []
        self.tabla_simbolos = tabla_simbolos  # Tabla de símbolos del analizador semántico
        self.contador_temporales = 0
        self.contador_etiquetas = 0
        self.segmento_datos = []
        self.variables = set()
        self.temp_vars = set()
        self.literal_cadenas = {}
        self.desplazamientos = {}  # Desplazamientos de variables desde BP
        self.funcion_actual = None
        self.desplazamiento_actual = 0  # Desplazamiento para variables locales (negativo desde BP)

    def generar(self):
        self.recolectar_variables()
        self.generar_segmento_datos()
        self.generar_segmento_codigo()
        return self.codigo_asm

    def recolectar_variables(self):
        # Recolectar variables y temporales del código IR
        for instruccion in self.codigo_ir:
            tokens = instruccion.replace(',', '').split()
            if '=' in tokens:
                idx = tokens.index('=')
                destino = tokens[0]
                src1 = tokens[idx + 1]
                if destino.startswith('t'):
                    self.temp_vars.add(destino)
                else:
                    self.variables.add(destino)
                if src1.startswith('t'):
                    self.temp_vars.add(src1)
                elif src1.isidentifier():
                    self.variables.add(src1)
                if len(tokens) > idx + 2:
                    src2 = tokens[idx + 2]
                    if src2.startswith('t'):
                        self.temp_vars.add(src2)
                    elif src2.isidentifier():
                        self.variables.add(src2)
            elif tokens[0] == 'param':
                parametro = tokens[1]
                if parametro.startswith('t'):
                    self.temp_vars.add(parametro)
                elif parametro.isidentifier():
                    self.variables.add(parametro)
            elif tokens[0] == 'call':
                pass  # Los nombres de funciones no necesitan ser recolectados
            elif tokens[0] == 'return':
                if len(tokens) > 1:
                    valor_retorno = tokens[1]
                    if valor_retorno.startswith('t'):
                        self.temp_vars.add(valor_retorno)
                    elif valor_retorno.isidentifier():
                        self.variables.add(valor_retorno)
            elif tokens[0] == 'label':
                pass
            elif tokens[0] == 'goto':
                pass
            elif tokens[0] == 'if':
                var_condicion = tokens[1]
                if var_condicion.startswith('t'):
                    self.temp_vars.add(var_condicion)
                elif var_condicion.isidentifier():
                    self.variables.add(var_condicion)
            # Agregar más casos según sea necesario

    def generar_segmento_datos(self):
        self.segmento_datos.append('.data')
        # Declarar variables globales
        for var in self.variables:
            # Verificar si la variable es global (no está en el ámbito de ninguna función)
            if self.es_global(var):
                self.segmento_datos.append(f'{var} DW 0')
        # Declarar digit_buffer
        self.segmento_datos.append('digit_buffer db 6 dup(0)')
        self.segmento_datos.append('')

    def es_global(self, nombre_var):
        try:
            info_simbolo = self.tabla_simbolos.buscar(nombre_var)
            return info_simbolo.get('nivel_ambito', 0) == 0
        except Exception:
            return False  # Si no se encuentra, asumir que no es global

    def generar_segmento_codigo(self):
        self.codigo_asm.append('.model small')
        self.codigo_asm.append('.stack 100h')
        self.codigo_asm.extend(self.segmento_datos)
        self.codigo_asm.append('.code')
        self.codigo_asm.append('start:')
        self.codigo_asm.append('call main')
        self.codigo_asm.append('mov ah, 4Ch')  # Salir del programa
        self.codigo_asm.append('int 21h')
        self.codigo_asm.append('')

        for instruccion in self.codigo_ir:
            instrucciones_asm = self.traducir_instruccion(instruccion)
            self.codigo_asm.extend(instrucciones_asm)

        # Agregar la subrutina de impresión al final
        self.codigo_asm.extend(self.generar_subrutina_print())
        self.codigo_asm.append('')
        self.codigo_asm.append('end start')

    def traducir_instruccion(self, instruccion):
        tokens = instruccion.replace(',', '').split()
        instrucciones_asm = []
        if '=' in tokens:
            destino = tokens[0]
            idx = tokens.index('=')
            src1 = tokens[idx + 1]
            if len(tokens) > idx + 2:
                op = tokens[idx + 2]
                src2 = tokens[idx + 3]
                # Operación binaria
                instrucciones_asm.extend(self.traducir_operacion_binaria(destino, src1, op, src2))
            else:
                # Asignación o resultado de llamada a función
                if 'call' in tokens:
                    nombre_funcion = tokens[idx + 1]
                    instrucciones_asm.extend(self.traducir_llamada(nombre_funcion, 0))
                    instrucciones_asm.append(f'mov {self.obtener_operando(destino)}, ax')  # El resultado de la función está en AX
                else:
                    # Asignación simple
                    instrucciones_asm.extend(self.traducir_asignacion(destino, src1))
        elif tokens[0] == 'param':
            parametro = tokens[1]
            instrucciones_asm.extend(self.traducir_param(parametro))
        elif tokens[0] == 'call':
            nombre_funcion = tokens[1]
            num_args = int(tokens[2])
            instrucciones_asm.extend(self.traducir_llamada(nombre_funcion, num_args))
        elif tokens[0] == 'return':
            if len(tokens) > 1:
                valor_retorno = tokens[1]
                instrucciones_asm.extend(self.traducir_return(valor_retorno))
            else:
                instrucciones_asm.append('ret')
        elif tokens[0] == 'func':
            nombre_funcion = tokens[1][:-1]  # Eliminar los dos puntos
            instrucciones_asm.append(f'{nombre_funcion} proc')
            instrucciones_asm.append('push bp')
            instrucciones_asm.append('mov bp, sp')
            self.funcion_actual = nombre_funcion
            self.desplazamiento_actual = 0  # Restablecer desplazamiento para variables locales
            self.asignar_variables_locales(nombre_funcion)
        elif tokens[0] == 'endfunc':
            nombre_funcion = tokens[1]
            instrucciones_asm.append('mov sp, bp')
            instrucciones_asm.append('pop bp')
            instrucciones_asm.append('ret')
            instrucciones_asm.append(f'{nombre_funcion} endp')
            self.funcion_actual = None
        elif tokens[0] == 'label':
            etiqueta = tokens[1]
            instrucciones_asm.append(f'{etiqueta}:')
        elif tokens[0] == 'goto':
            etiqueta = tokens[1]
            instrucciones_asm.append(f'jmp {etiqueta}')
        elif tokens[0] == 'if':
            var_condicion = tokens[1]
            etiqueta = tokens[3]
            instrucciones_asm.extend(self.traducir_if(var_condicion, etiqueta))
        # Agregar más casos según sea necesario
        return instrucciones_asm

    def asignar_variables_locales(self, nombre_funcion):
        # Asignar espacio para variables locales y temporales
        simbolos_funcion = self.obtener_simbolos_en_funcion(nombre_funcion)
        for var, info in simbolos_funcion.items():
            if info['clase'] == 'variable' and info['funcion'] == nombre_funcion:
                self.desplazamiento_actual -= 2  # Asumiendo tamaño de palabra de 2 bytes
                self.desplazamientos[var] = self.desplazamiento_actual
        # Asignar temporales
        for temp in self.temp_vars:
            # Asumiendo que los temporales son por función
            self.desplazamiento_actual -= 2
            self.desplazamientos[temp] = self.desplazamiento_actual

    def obtener_simbolos_en_funcion(self, nombre_funcion):
        simbolos = {}
        for ambito in self.tabla_simbolos.ambitos:
            for nombre, info in ambito.items():
                if info.get('funcion') == nombre_funcion:
                    simbolos[nombre] = info
        return simbolos

    def obtener_operando(self, operando):
        if operando.isdigit():
            return operando
        elif operando.startswith('['):
            return operando
        elif operando in self.desplazamientos:
            desplazamiento = self.desplazamientos[operando]
            direccion = f'[bp{desplazamiento}]' if desplazamiento < 0 else f'[bp+{desplazamiento}]'
            # Determinar si es byte o palabra basado en el operando
            return f'word ptr {direccion}'
        elif self.es_global(operando):
            return f'word ptr {operando}'
        else:
            # Parámetro o variable accedida vía BP
            info_simbolo = self.tabla_simbolos.buscar(operando)
            if info_simbolo['clase'] == 'parametro':
                indice_parametro = info_simbolo.get('indice_parametro', 0)
                desplazamiento = 4 + indice_parametro * 2
                self.desplazamientos[operando] = desplazamiento
                return f'word ptr [bp+{desplazamiento}]'
            else:
                return operando

    def traducir_asignacion(self, destino, src):
        instrucciones_asm = []
        instrucciones_asm.append(f'mov ax, {self.obtener_operando(src)}')
        instrucciones_asm.append(f'mov {self.obtener_operando(destino)}, ax')
        return instrucciones_asm

    def traducir_operacion_binaria(self, destino, src1, op, src2):
        instrucciones_asm = []
        instrucciones_asm.append(f'mov ax, {self.obtener_operando(src1)}')
        if op == '+':
            instrucciones_asm.append(f'add ax, {self.obtener_operando(src2)}')
        elif op == '-':
            instrucciones_asm.append(f'sub ax, {self.obtener_operando(src2)}')
        elif op == '*':
            instrucciones_asm.append(f'mov dx, 0')
            instrucciones_asm.append(f'mov bx, {self.obtener_operando(src2)}')
            instrucciones_asm.append(f'mul bx')  # DX:AX = AX * BX
            # El resultado está en AX
        elif op == '/':
            instrucciones_asm.append(f'mov dx, 0')
            instrucciones_asm.append(f'mov bx, {self.obtener_operando(src2)}')
            instrucciones_asm.append(f'div bx')  # AX = DX:AX / BX
            # Cociente en AX
        instrucciones_asm.append(f'mov {self.obtener_operando(destino)}, ax')
        return instrucciones_asm

    def traducir_param(self, parametro):
        instrucciones_asm = []
        instrucciones_asm.append(f'push {self.obtener_operando(parametro)}')
        return instrucciones_asm

    def traducir_llamada(self, nombre_funcion, num_args):
        instrucciones_asm = []
        if nombre_funcion == 'print':
            # Para print, el valor a imprimir está en la cima de la pila
            instrucciones_asm.append('pop ax')  # Obtener el valor a imprimir
            instrucciones_asm.append('call print')
        else:
            instrucciones_asm.append(f'call {nombre_funcion}')
            instrucciones_asm.append(f'add sp, {num_args * 2}')  # Limpiar la pila
        return instrucciones_asm

    def traducir_return(self, valor_retorno):
        instrucciones_asm = []
        instrucciones_asm.append(f'mov ax, {self.obtener_operando(valor_retorno)}')
        instrucciones_asm.append('mov sp, bp')
        instrucciones_asm.append('pop bp')
        instrucciones_asm.append('ret')
        return instrucciones_asm

    def traducir_if(self, var_condicion, etiqueta):
        instrucciones_asm = []
        instrucciones_asm.append(f'mov ax, {self.obtener_operando(var_condicion)}')
        instrucciones_asm.append('cmp ax, 0')
        instrucciones_asm.append(f'je {etiqueta}')
        return instrucciones_asm

    # Incluir la subrutina print
    def generar_subrutina_print(self):
        instrucciones_asm = []
        instrucciones_asm.append('print proc')
        instrucciones_asm.append('push ax')
        instrucciones_asm.append('push bx')
        instrucciones_asm.append('push cx')
        instrucciones_asm.append('push dx')
        instrucciones_asm.append('push si')

        # Inicializar variables
        instrucciones_asm.append('mov cx, 0')
        instrucciones_asm.append('mov bx, 10')
        instrucciones_asm.append('mov si, offset digit_buffer')
        instrucciones_asm.append('add si, 6            ; Apuntar SI al final del buffer')

        # Verificar si AX es cero
        instrucciones_asm.append('cmp ax, 0')
        instrucciones_asm.append('jne convertir_loop')
        # Manejar caso cero
        instrucciones_asm.append('dec si')
        instrucciones_asm.append('mov byte ptr [si], \'0\'')
        instrucciones_asm.append('inc cx')
        instrucciones_asm.append('jmp imprimir_digitos')

        instrucciones_asm.append('convertir_loop:')
        instrucciones_asm.append('inicio_convertir_loop:')
        instrucciones_asm.append('xor dx, dx')
        instrucciones_asm.append('div bx')
        instrucciones_asm.append('dec si')
        instrucciones_asm.append('add dl, \'0\'')
        instrucciones_asm.append('mov [si], dl')
        instrucciones_asm.append('inc cx')
        instrucciones_asm.append('cmp ax, 0')
        instrucciones_asm.append('jne inicio_convertir_loop')

        instrucciones_asm.append('imprimir_digitos:')
        instrucciones_asm.append('loop_imprimir_digito:')
        instrucciones_asm.append('mov dl, [si]')
        instrucciones_asm.append('mov ah, 02h')
        instrucciones_asm.append('int 21h')
        instrucciones_asm.append('inc si')
        instrucciones_asm.append('loop loop_imprimir_digito')

        # Nueva línea
        instrucciones_asm.append('mov dl, 0Ah')
        instrucciones_asm.append('mov ah, 02h')
        instrucciones_asm.append('int 21h')
        instrucciones_asm.append('mov dl, 0Dh')
        instrucciones_asm.append('mov ah, 02h')
        instrucciones_asm.append('int 21h')

        instrucciones_asm.append('pop si')
        instrucciones_asm.append('pop dx')
        instrucciones_asm.append('pop cx')
        instrucciones_asm.append('pop bx')
        instrucciones_asm.append('pop ax')
        instrucciones_asm.append('ret')
        instrucciones_asm.append('print endp')
        return instrucciones_asm

    # Métodos auxiliares adicionales según sea necesario
