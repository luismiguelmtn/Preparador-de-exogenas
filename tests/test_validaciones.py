from io import BytesIO

import pandas as pd
import pytest

from main import generar_consolidado
from utils import validar_nit


def crear_excel_en_memoria(df):
    """Convierte un DataFrame en bytes de Excel, simulando un archivo subido por el usuario."""
    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Datos")

    buffer.seek(0)
    return buffer.getvalue()


# --- Validación de formato de NIT ---

def test_validar_nit_correcto():
    assert validar_nit("900984614") is True


def test_validar_nit_con_letras():
    assert validar_nit("abc") is False


def test_validar_nit_muy_corto():
    assert validar_nit("123") is False


# --- Validaciones del archivo Excel recibido ---

def test_generar_consolidado_rechaza_archivo_no_excel():
    # Simula que alguien sube un archivo corrupto o de otro formato
    with pytest.raises(ValueError, match="Archivo no es un Excel válido"):
        generar_consolidado(b"esto no es un excel", "901521156")


def test_generar_consolidado_rechaza_columnas_faltantes():
    # Excel real pero sin las columnas que la exógena DIAN requiere
    df = pd.DataFrame({
        "Tipo de documento": ["Factura electrónica"],
        "NIT Emisor": ["901521156"],
        "Nombre Emisor": ["EMPRESA PRUEBA SAS"],
    })

    contenido_excel = crear_excel_en_memoria(df)

    with pytest.raises(ValueError, match="Columnas faltantes"):
        generar_consolidado(contenido_excel, "901521156")


def test_generar_consolidado_rechaza_iva_no_numerico():
    # El IVA debe ser un número para poder sumarlo en el consolidado
    df = pd.DataFrame({
        "Tipo de documento": ["Factura electrónica"],
        "NIT Emisor": ["901521156"],
        "Nombre Emisor": ["EMPRESA PRUEBA SAS"],
        "NIT Receptor": ["900111222"],
        "Nombre Receptor": ["CLIENTE PRUEBA SAS"],
        "IVA": ["texto"],
        "Total": [119000],
    })

    contenido_excel = crear_excel_en_memoria(df)

    with pytest.raises(ValueError, match="IVA"):
        generar_consolidado(contenido_excel, "901521156")


def test_generar_consolidado_rechaza_total_vacio():
    # Un Total vacío rompería las sumas del consolidado si no se valida antes
    df = pd.DataFrame({
        "Tipo de documento": ["Factura electrónica"],
        "NIT Emisor": ["901521156"],
        "Nombre Emisor": ["EMPRESA PRUEBA SAS"],
        "NIT Receptor": ["900111222"],
        "Nombre Receptor": ["CLIENTE PRUEBA SAS"],
        "IVA": [19000],
        "Total": [None],
    })

    contenido_excel = crear_excel_en_memoria(df)

    with pytest.raises(ValueError, match="Total"):
        generar_consolidado(contenido_excel, "901521156")