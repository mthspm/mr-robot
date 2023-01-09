from measure_time import measure_time

@measure_time
def funcaogrande():

    for n in range (0,9999):
        print(n)

funcaogrande()