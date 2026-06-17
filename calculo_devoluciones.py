import pandas as pd
from utils import calcular_digito_verificacion, TIPOS_DEVOLUCION

def calcular_devolucion(df, nit_filtro):
    """Consolida las devoluciones emitidas a la empresa agrupados por emisor."""

    devoluciones = df[
        (df['NIT Receptor'] == nit_filtro) &
        (df['Tipo de documento'].isin(TIPOS_DEVOLUCION))
    ]

    consolidado = devoluciones.groupby(
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