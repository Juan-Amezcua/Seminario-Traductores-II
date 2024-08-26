from collections import deque

class Pila:
    def __init__(self):
        self.pila = deque()

    def apilar(self, elemento):
        self.pila.appendleft(elemento)

    def desapilar(self):
        return self.pila.popleft()

    def tope(self):
        return self.pila[0]

    def mostrar(self):
        print("Pila:", ' '.join(map(str, reversed(self.pila))))


