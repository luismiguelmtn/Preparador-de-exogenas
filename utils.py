# Documentos tributarios que generan ingreso para el emisor
TIPOS_INGRESO = [
    'Factura electrónica',
    'Documento equivalente POS',
    'Factura electrónica de contingencia',
]

# Documentos tributarios que generan nota crédito para el emisor
TIPOS_NOTA_CREDITO = [
    'Nota de crédito electrónica',
]
# Documentos tributarios que generan devolución para el emisor
TIPOS_DEVOLUCION = [
    'Nota de crédito electrónica',
]

# Documentos tributarios que generan gasto para el emisor
TIPOS_GASTO = [
    'Factura electrónica',
    'Documento equivalente POS',
    'Documento equivalente - Transporte aéreo de pasajeros',
    'Factura electrónica de contingencia',
]

# Documentos tributarios que generan gasto para el emisor (excluidos)
TIPOS_GASTO_EXCLUIDO = [
    'Factura electrónica',
    'Documento equivalente POS',
    'Documento equivalente - Transporte aéreo de pasajeros',
    'Factura electrónica de contingencia',
]
    
# Documentos tributarios que generan nómina para el emisor
TIPOS_NOMINA = [
    'Nomina Individual',
    'Nomima Individual De Ajustes',
    'Nomina Individual De Ajustes',
]

def calcular_digito_verificacion(nit):
    """Calcula el dígito de verificación según algoritmo DIAN."""
    nit = str(nit)
    
    # Pesos ponderados definidos por la DIAN
    pesos = [3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71]

    suma = 0
    for i, digito in enumerate(reversed(nit)):
        suma += int(digito) * pesos[i]

    residuo = suma % 11

    if residuo == 0:
        return 0
    elif residuo == 1:
        return 1
    else:
        return 11 - residuo