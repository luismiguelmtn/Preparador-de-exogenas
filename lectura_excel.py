import pandas as pd

# 1. Abrir el archivo y ver qué hojas tiene
archivo = pd.ExcelFile("ejemplo.xlsx")
print(archivo.sheet_names)  # Te muestra: ['Hoja1', 'F_2276', etc.]

# 2. Leer la primera hoja (sin importar su nombre)
nombre_hoja = archivo.sheet_names[0]
df = pd.read_excel(archivo, sheet_name=nombre_hoja)

# 3. Ver qué tiene
print(df.head())       # Primeras 5 filas
print(df.columns.tolist())  # Nombres de columnas
print(df.shape)        # Cuántas filas y columnas