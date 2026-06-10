import pandas as pd
from utils import calcular_digito_verificacion

# Documentos tributarios que generan ingreso para el emisor
TIPOS_INGRESO = [
    'Factura electrónica',
    'Documento soporte con no obligados'
]

def calcular_ingresos(df, nit_filtro):
    """Consolida los ingresos emitidos por la empresa agrupados por receptor."""

    facturas_emitidas = df[
        (df['NIT Emisor'] == nit_filtro) &
        (df['Tipo de documento'].isin(TIPOS_INGRESO))
    ]

    consolidado = facturas_emitidas.groupby(
        ['NIT Receptor', 'Nombre Receptor']
    ).agg(
        IVA=('IVA', 'sum'),
        Total=('Total', 'sum'),
    ).reset_index()

    # Base gravable: IVA generado / tarifa del 19% (Art. 468 E.T.)
    consolidado['Base'] = consolidado['IVA'] / 0.19

    # Dígito de verificación calculado según algoritmo DIAN
    consolidado['DV'] = consolidado['NIT Receptor'].apply(calcular_digito_verificacion)

    return consolidado[[
        'NIT Receptor',
        'DV',
        'Nombre Receptor',
        'Base',
        'IVA',
        'Total'
    ]]