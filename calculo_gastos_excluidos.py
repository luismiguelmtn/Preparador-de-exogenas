import pandas as pd
from utils import calcular_digito_verificacion, TIPOS_GASTO_EXCLUIDO

def calcular_gastos_excluidos(df, nit_filtro):
    """Consolida los gastos incurridos por la empresa agrupados por emisor."""

    facturas_emitidas = df[
        (df['NIT Emisor'] != nit_filtro) &
        (df['Tipo de documento'].isin(TIPOS_GASTO_EXCLUIDO)) &
        (df['IVA'] == 0)
    ]

    consolidado = facturas_emitidas.groupby(
        ['NIT Emisor', 'Nombre Emisor']
    ).agg(
        IVA=('IVA', 'sum'),
        Total=('Total', 'sum'),
    ).reset_index()

    # Base gravable: Para gastos excluidos se asigna 0
    consolidado['Base'] = 0

    # Dígito de verificación calculado según algoritmo DIAN
    consolidado['DV'] = consolidado['NIT Emisor'].apply(calcular_digito_verificacion)

    return consolidado[[
        'NIT Emisor',
        'DV',
        'Nombre Emisor',
        'Base',
        'IVA',
        'Total'
    ]]