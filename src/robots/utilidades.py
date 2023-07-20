import time

def tiempoejecucion(funcion):
    def funcionmedida(*args, **kwargs):
        inicio = time.time()
        c = funcion(*args, **kwargs)
        print(time.time() - inicio)
        return c
    return funcionmedida