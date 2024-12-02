# tabla_simbolos.py

class TablaSimbolos:
    def __init__(self):
        self.ambitos = [{}]  # Pila de ámbitos (lista de diccionarios)
        self.nivel_ambito = 0  # Para rastrear el nivel de ámbito actual

    def entrar_ambito(self):
        self.ambitos.append({})
        self.nivel_ambito += 1

    def salir_ambito(self):
        if len(self.ambitos) > 1:
            self.ambitos.pop()
            self.nivel_ambito -= 1
        else:
            raise Exception("Error Semántico: No se puede salir del ámbito global.")

    def declarar(self, nombre, info):
        ambito_actual = self.ambitos[-1]
        if nombre in ambito_actual:
            raise Exception(f"Error Semántico: '{nombre}' ya está declarado en el ámbito actual.")
        # Agregar nivel de ámbito a la información
        info['nivel_ambito'] = self.nivel_ambito
        ambito_actual[nombre] = info

    def buscar(self, nombre):
        for ambito in reversed(self.ambitos):
            if nombre in ambito:
                return ambito[nombre]
        raise Exception(f"Error Semántico: '{nombre}' no está declarado.")

    def actualizar(self, nombre, info):
        for ambito in reversed(self.ambitos):
            if nombre in ambito:
                ambito[nombre].update(info)
                return
        raise Exception(f"Error Semántico: '{nombre}' no está declarado.")

    def obtener_todos_los_simbolos(self):
        simbolos = {}
        for ambito in self.ambitos:
            simbolos.update(ambito)
        return simbolos
