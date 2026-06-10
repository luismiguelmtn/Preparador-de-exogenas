def calcular_digito_verificacion(nit):
    nit = str(nit)  # asegurarse que sea texto
    primos = [3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71]
    
    # Multiplicar cada dígito por su primo correspondiente de derecha a izquierda
    suma = 0
    for i, digito in enumerate(reversed(nit)):
        suma += int(digito) * primos[i]
    
    residuo = suma % 11
    
    if residuo == 0:
        return 0
    elif residuo == 1:
        return 1
    else:
        return 11 - residuo