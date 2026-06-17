import pandas as pd
from utils import calcular_digito_verificacion, TIPOS_GASTO

def calcular_gastos(df, nit_filtro):
    """Consolida los gastos incurridos por la empresa agrupados por emisor."""

    facturas_emitidas = df[
        (df['NIT Receptor'] == nit_filtro) &
        (df['Tipo de documento'].isin(TIPOS_GASTO)) &
        (df['IVA'] != 0)
    ]

    consolidado = facturas_emitidas.groupby(
        ['NIT Emisor', 'Nombre Emisor']
    ).agg(
        IVA=('IVA', 'sum'),
        Total=('Total', 'sum'),
    ).reset_index()

    # Base gravable: IVA generado / tarifa del 19% (Art. 468 E.T.)
    consolidado['Base'] = consolidado['IVA'] / 0.19

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