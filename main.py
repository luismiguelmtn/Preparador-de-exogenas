import pandas as pd
from utils import  TIPOS_INGRESO
from calculo_ingresos import calcular_ingresos

# Cargar archivo
archivo = pd.ExcelFile("ejemplo.xlsx")
df = pd.read_excel(archivo, sheet_name=archivo.sheet_names[0])

# NIT de la empresa que reporta
nit_filtro = int(input("Ingresa tu NIT (sin dígito de verificación): "))

# Calcular consolidados de ingresos
ingresos = calcular_ingresos(df, nit_filtro)

# Reducir df901391837 eliminando filas ya procesadas en ingresos
df = df[~(
    (df['NIT Emisor'] == nit_filtro) &
    (df['Tipo de documento'].isin(TIPOS_INGRESO))
)]

# Guardar resultados
with pd.ExcelWriter('consolidado_exogena.xlsx', engine='openpyxl') as writer:
    ingresos.to_excel(writer, sheet_name='Ingresos', index=False)

print("Archivo consolidado_exogena.xlsx generado exitosamente.")