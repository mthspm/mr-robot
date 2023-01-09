import time

# Calcula o tempo de execucao de uma funcao e imprime o tempo no log de registro... retorna : func(*args, **kwargs)
def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'Execution time: {end-start} seconds for {func}')
        return result

    return wrapper