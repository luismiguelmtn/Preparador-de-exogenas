import pandas as pd
import io
from utils import  TIPOS_DEVOLUCION, TIPOS_DOC_SOPORTE, TIPOS_GASTO, TIPOS_INGRESO, TIPOS_NOMINA, TIPOS_NOTA_CREDITO, TIPOS_GASTO_EXCLUIDO, COLUMNAS_REQUERIDAS
from utils import validar_nit
from calculo_ingresos import calcular_ingresos
from calculo_notas_credito import calcular_NC
from calculo_devoluciones import calcular_devolucion
from calculo_gastos import calcular_gastos
from calculo_gastos_excluidos import calcular_gastos_excluidos
from calculo_nomina import calcular_nominas


def generar_consolidado(info_exogena, nit_filtro):

    # Validar formato del NIT
    if not validar_nit(nit_filtro):
        raise ValueError(f"NIT inválido: '{nit_filtro}'. Debe ser numérico, 8-10 dígitos, sin dígito de verificación")

    try:
        # Cargar archivo y contenido en memoria (bytes desde la API)
        archivo = pd.ExcelFile(io.BytesIO(info_exogena))
    except Exception as e:
        raise ValueError(f"Archivo no es un Excel válido: {str(e)}")
    
    df = pd.read_excel(archivo, sheet_name=archivo.sheet_names[0])

    # Validar que el DataFrame tenga las columnas requeridas
    columnas_faltantes = [col for col in COLUMNAS_REQUERIDAS if col not in df.columns]
    if columnas_faltantes:
        raise ValueError(f"Columnas faltantes en el archivo: {', '.join(columnas_faltantes)}")

    # Normalizar columnas de NIT a texto para manejo uniforme
    df['NIT Emisor'] = df['NIT Emisor'].astype(str).str.strip()
    df['NIT Receptor'] = df['NIT Receptor'].astype(str).str.strip()

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
        (df['NIT Emisor'] == nit_filtro) &
        (df['Tipo de documento'].isin(TIPOS_NOMINA))
    )]

    # Guardar en memoria en lugar de en disco
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        ingresos.to_excel(writer, sheet_name='Ingresos', index=False)
        notas_credito.to_excel(writer, sheet_name='Notas Crédito', index=False)
        devoluciones.to_excel(writer, sheet_name='Devoluciones', index=False)
        gastos.to_excel(writer, sheet_name='Gastos', index=False)
        gastos_excluidos.to_excel(writer, sheet_name='Gastos Excluidos', index=False)
        nominas.to_excel(writer, sheet_name='Nominas', index=False)

    buffer.seek(0)
    return buffer