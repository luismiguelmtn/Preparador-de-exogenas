import pandas as pd
from calculo_ingresos import calcular_ingresos

# Cargar archivo
archivo = pd.ExcelFile("ejemplo.xlsx")
df = pd.read_excel(archivo, sheet_name=archivo.sheet_names[0])

# NIT de la empresa que reporta
nit_filtro = int(input("Ingresa tu NIT (sin dígito de verificación): "))

# Calcular consolidados
ingresos = calcular_ingresos(df, nit_filtro)

# Guardar resultados
with pd.ExcelWriter('consolidado_exogena.xlsx', engine='openpyxl') as writer:
    ingresos.to_excel(writer, sheet_name='Ingresos', index=False)

print("Archivo consolidado_exogena.xlsx generado exitosamente.")