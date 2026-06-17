from fastapi import FastAPI, File, HTTPException, UploadFile, Form
from fastapi.responses import StreamingResponse
from main import generar_consolidado

# Crear la aplicación FastAPI
app = FastAPI(title="Preparador de Exógenas DIAN")

@app.post("/consolidar")
async def consolidar(
    archivo: UploadFile = File(...),
    nit: str = Form(...)
):
    """Recibe un archivo Excel y un NIT, retorna el consolidado."""

    try:
        # Leer el contenido del archivo en memoria
        contenido = await archivo.read()

        # Generar el consolidado
        buffer = generar_consolidado(contenido, nit)

        # Enviar el Excel como descarga al navegador
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=consolidado_exogena.xlsx"}
        )
    except ValueError as e:
        # Errores de validación (NIT, formato de archivo, columnas faltantes)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Errores inesperados durante el procesamiento del archivo
        raise HTTPException(
            status_code=500,
            detail=f"Ocurrió un error inesperado al procesar el archivo"
        )