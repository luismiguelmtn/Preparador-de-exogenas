import pandas as pd

# 1. Abrir el archivo y ver qué hojas tiene
archivo = pd.ExcelFile("ejemplo.xlsx")
# print(archivo.sheet_names)  # Te muestra: ['Hoja1', 'F_2276', etc.]

# 2. Leer la primera hoja (sin importar su nombre)
nombre_hoja = archivo.sheet_names[0]
df = pd.read_excel(archivo, sheet_name=nombre_hoja)

# 3. Ver qué tiene el DataFrame
# print(df.columns.tolist())  # Nombres de columnas
# print(df.shape)        # Cuántas filas y columnas

# Pedir el NIT al usuario
nit_filtro = int(input("Ingresa tu NIT (sin dígito de verificación): "))

# Tipos de documento que representan ingresos emitidos
tipos_ingreso = [
    'Factura electrónica',
    'Documento soporte con no obligados'
]

# Filtrar facturas emitidas por el NIT del emisor y por los tipos de documento
facturas_emitidas = df[
    (df['NIT Emisor'] == nit_filtro) &
    (df['Tipo de documento'].isin(tipos_ingreso))
]

# Agrupar por NIT Receptor y Nombre Receptor, sumar columnas de valor
consolidado_facturas = facturas_emitidas.groupby(
    ['NIT Receptor', 'Nombre Receptor']
).agg(
    IVA=('IVA', 'sum'),
    Total=('Total', 'sum'),
).reset_index()

print(consolidado_facturas)