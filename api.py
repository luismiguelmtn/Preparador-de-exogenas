from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from main import generar_consolidado

# Crear la aplicación FastAPI
app = FastAPI(title="Preparador de Exógenas DIAN.")

@app.post("/consolidar")
async def consolidar(
    archivo: UploadFile = File(...),
    nit: str = Form(...)
):
    """Recibe un archivo Excel y un NIT, retorna el consolidado."""

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