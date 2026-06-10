import pandas as pd
from utils import  TIPOS_INGRESO, TIPOS_NOTA_CREDITO
from calculo_ingresos import calcular_ingresos
from calculo_notas_credito import calcular_NC

# Cargar archivo
archivo = pd.ExcelFile("ejemplo.xlsx")
df = pd.read_excel(archivo, sheet_name=archivo.sheet_names[0])

# NIT de la empresa que reporta
nit_filtro = int(input("Ingresa tu NIT (sin dígito de verificación): "))

# Calcular consolidados de ingresos
ingresos = calcular_ingresos(df, nit_filtro)

# Reducir df eliminando filas ya procesadas en ingresos
df = df[~(
    (df['NIT Emisor'] == nit_filtro) &
    (df['Tipo de documento'].isin(TIPOS_INGRESO))
)]

# Calcular consolidados de notas crédito
notas_credito = calcular_NC(df, nit_filtro)

# Reducir df eliminando filas ya procesadas en notas crédito
df = df[~(
    (df['NIT Emisor'] == nit_filtro) &
    (df['Tipo de documento'].isin(TIPOS_NOTA_CREDITO))
)]

# Guardar resultados
with pd.ExcelWriter('consolidado_exogena.xlsx', engine='openpyxl') as writer:
    ingresos.to_excel(writer, sheet_name='Ingresos', index=False)
    notas_credito.to_excel(writer, sheet_name='Notas Crédito', index=False)

print("Archivo consolidado_exogena.xlsx generado exitosamente.")