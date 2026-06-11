import pandas as pd
from utils import TIPOS_NOMINA

def calcular_nominas(df, nit_filtro):
    """Consolida las nominas generadas por la empresa agrupadas por emisor."""

    facturas_emitidas = df[
        (df['NIT Emisor'] == nit_filtro) &
        (df['Tipo de documento'].isin(TIPOS_NOMINA))
    ]

    consolidado = facturas_emitidas.groupby(
        ['NIT Receptor', 'Nombre Receptor']
    ).agg(
        Total=('Total', 'sum'),
    ).reset_index()

    # Para nominas el IVA es 0
    consolidado['IVA'] = 0

    # Base gravable: Para nominas se asigna 0
    consolidado['Base'] = 0

    # Dígito de verificación no aplica para nominas, se deja vacío
    consolidado['DV'] = ''

    return consolidado[[
        'NIT Receptor',
        'DV',
        'Nombre Receptor',
        'Base',
        'IVA',
        'Total'
    ]]