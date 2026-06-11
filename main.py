import pandas as pd
from utils import  TIPOS_DEVOLUCION, TIPOS_DOC_SOPORTE, TIPOS_GASTO, TIPOS_INGRESO, TIPOS_NOMINA, TIPOS_NOTA_CREDITO, TIPOS_GASTO_EXCLUIDO
from calculo_ingresos import calcular_ingresos
from calculo_notas_credito import calcular_NC
from calculo_devoluciones import calcular_devolucion
from calculo_gastos import calcular_gastos
from calculo_gastos_excluidos import calcular_gastos_excluidos
from calculo_nomina import calcular_nominas

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

# Calcular consolidados de devoluciones
devoluciones = calcular_devolucion(df, nit_filtro)

# Reducir df eliminando filas ya procesadas en devoluciones
df = df[~(
    (df['NIT Emisor'] != nit_filtro) &
    (df['Tipo de documento'].isin(TIPOS_DEVOLUCION))
)]

# Calcular consolidados de gastos
gastos = calcular_gastos(df, nit_filtro)

# Reducir df eliminando filas ya procesadas en gastos
df = df[~(
    (df['NIT Emisor'] != nit_filtro) &
    (df['Tipo de documento'].isin(TIPOS_GASTO)) &
    (df['IVA'] != 0)
)]

# Calcular consolidados de gastos excluidos
gastos_excluidos = calcular_gastos_excluidos(df, nit_filtro)

# Reducir df eliminando filas ya procesadas en gastos excluidos
df = df[~(
    (
        (df['NIT Emisor'] != nit_filtro) &
        (df['Tipo de documento'].isin(TIPOS_GASTO_EXCLUIDO)) &
        (df['IVA'] == 0)
    ) | (
        (df['NIT Emisor'] == nit_filtro) &
        (df['Tipo de documento'].isin(TIPOS_DOC_SOPORTE))
    )
)]

# Calcular consolidados de nomina
nominas = calcular_nominas(df, nit_filtro)

# Reducir df eliminando filas ya procesadas en nominas
df = df[~(
    (df['NIT Emisor'] != nit_filtro) &
    (df['Tipo de documento'].isin(TIPOS_NOMINA))
)]

# Guardar resultados
with pd.ExcelWriter('consolidado_exogena.xlsx', engine='openpyxl') as writer:
    ingresos.to_excel(writer, sheet_name='Ingresos', index=False)
    notas_credito.to_excel(writer, sheet_name='Notas Crédito', index=False)
    devoluciones.to_excel(writer, sheet_name='Devoluciones', index=False)
    gastos.to_excel(writer, sheet_name='Gastos', index=False)
    gastos_excluidos.to_excel(writer, sheet_name='Gastos Excluidos', index=False)
    nominas.to_excel(writer, sheet_name='Nominas', index=False)

print("Archivo consolidado_exogena.xlsx generado exitosamente.")