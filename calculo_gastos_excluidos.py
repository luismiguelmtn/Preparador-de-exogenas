import pandas as pd
from utils import calcular_digito_verificacion, TIPOS_GASTO_EXCLUIDO,TIPOS_DOC_SOPORTE

def calcular_gastos_excluidos(df, nit_filtro):
    """Consolida los gastos excluidos por la empresa agrupados por emisor."""

    # Caso 1: facturas de terceros sin IVA (tú eres receptor)
    caso1 = (
        (df['NIT Receptor'] == nit_filtro) &
        (df['Tipo de documento'].isin(TIPOS_GASTO_EXCLUIDO)) &
        (df['IVA'] == 0)
    )

    # Caso 2: Documento soporte emitido por la empresa (gasto propio)
    caso2 = (
        (df['NIT Emisor'] == nit_filtro) &
        (df['Tipo de documento'].isin(TIPOS_DOC_SOPORTE))
    )

    facturas_emitidas = df[caso1 | caso2]

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