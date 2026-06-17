# Preparador de Exogenas DIAN

Aplicacion en Python y FastAPI para consolidar informacion exogena de la DIAN a partir de un archivo Excel exportado desde una plataforma de facturacion electronica.

La app recibe un archivo Excel y el NIT de la empresa reportante por medio de un endpoint web. Luego genera un archivo `consolidado_exogena.xlsx` en memoria y lo devuelve como descarga.

---

## Estado Actual

El proyecto esta orientado a uso web mediante FastAPI. Ya no depende de ejecutar `main.py` por consola ni de leer archivos desde una ruta fija del disco.

Flujo actual:

1. El usuario envia un archivo Excel y el NIT de la empresa.
2. `api.py` recibe el archivo por el endpoint `/consolidar`.
3. El archivo se lee en memoria como bytes.
4. `main.py` valida y procesa la informacion.
5. Se genera un Excel consolidado en memoria.
6. La API devuelve el archivo como descarga.

---

## Requisitos

- Python 3.10 o superior
- Dependencias listadas en `requirements.txt`

Instalacion:

```bash
pip install -r requirements.txt
```

Dependencias principales:

- `fastapi`
- `uvicorn`
- `python-multipart`
- `pandas`
- `openpyxl`

---

## Como Ejecutar La API

Iniciar el servidor de desarrollo:

```bash
uvicorn api:app --reload
```

Luego abrir la documentacion interactiva de FastAPI:

```text
http://127.0.0.1:8000/docs
```

Desde ahi se puede probar el endpoint:

```text
POST /consolidar
```

Parametros esperados:

| Campo | Tipo | Descripcion |
|---|---|---|
| `archivo` | Archivo Excel | Archivo `.xlsx` con la informacion exogena |
| `nit` | Texto | NIT de la empresa reportante, sin digito de verificacion |

La respuesta es un archivo Excel descargable llamado:

```text
consolidado_exogena.xlsx
```

---

## Estructura Del Proyecto

```text
Preparador de exogenas/
    api.py                       <- Entrada web con FastAPI
    main.py                      <- Coordina validacion, lectura y generacion del consolidado
    calculo_ingresos.py          <- Consolidado de ingresos facturados
    calculo_notas_credito.py     <- Consolidado de notas credito emitidas
    calculo_devoluciones.py      <- Consolidado de devoluciones recibidas
    calculo_gastos.py            <- Consolidado de gastos con IVA
    calculo_gastos_excluidos.py  <- Consolidado de gastos sin IVA
    calculo_nomina.py            <- Consolidado de nomina electronica
    utils.py                     <- Constantes, columnas requeridas y funciones compartidas
    requirements.txt             <- Dependencias del proyecto
    .gitignore
```

---

## Validaciones Implementadas

Antes de generar el consolidado, la aplicacion realiza estas validaciones:

- El NIT se limpia con `.strip()`.
- El NIT debe ser numerico.
- El NIT debe tener entre 8 y 10 digitos.
- El archivo recibido debe poder abrirse como Excel.
- Se lee siempre la primera hoja del archivo.
- El archivo debe contener las columnas requeridas:
  - `Tipo de documento`
  - `NIT Emisor`
  - `Nombre Emisor`
  - `NIT Receptor`
  - `Nombre Receptor`
  - `IVA`
  - `Total`
- Las columnas `IVA` y `Total` deben contener valores numericos.
- Las columnas `NIT Emisor` y `NIT Receptor` se normalizan como texto.

En la API:

- Los errores de validacion se responden como HTTP `400`.
- Los errores inesperados se responden como HTTP `500`.

---

## Resultado Generado

El Excel generado contiene una hoja por cada tipo de operacion:

| Hoja | Contenido |
|---|---|
| `Ingresos` | Facturas emitidas por la empresa, agrupadas por receptor |
| `Notas Credito` | Notas credito emitidas por la empresa, agrupadas por receptor |
| `Devoluciones` | Notas credito recibidas por la empresa, agrupadas por emisor |
| `Gastos` | Facturas recibidas con IVA, agrupadas por emisor |
| `Gastos Excluidos` | Facturas recibidas sin IVA, agrupadas por emisor |
| `Nominas` | Nomina electronica emitida, agrupada por receptor |

Columnas actuales de salida:

- En hojas agrupadas por receptor:
  - `NIT Receptor`
  - `DV`
  - `Nombre Receptor`
  - `Base`
  - `IVA`
  - `Total`

- En hojas agrupadas por emisor:
  - `NIT Emisor`
  - `DV`
  - `Nombre Emisor`
  - `Base`
  - `IVA`
  - `Total`

---

## Logica De Negocio

La informacion exogena contiene documentos donde la empresa puede aparecer como emisora o como receptora. Cada modulo aplica filtros segun el rol de la empresa y el tipo de documento.

### Ingresos

Documentos donde la empresa es emisora. Corresponden a facturas generadas a clientes.

Filtro principal:

- `NIT Emisor == nit`
- Tipo de documento incluido en `TIPOS_INGRESO`

Se agrupa por:

- `NIT Receptor`
- `Nombre Receptor`

### Notas Credito

Documentos donde la empresa es emisora de una nota credito.

Filtro principal:

- `NIT Emisor == nit`
- Tipo de documento incluido en `TIPOS_NOTA_CREDITO`

Se agrupa por:

- `NIT Receptor`
- `Nombre Receptor`

### Devoluciones

Documentos donde la empresa es receptora de una nota credito emitida por un tercero.

Filtro principal:

- `NIT Receptor == nit`
- Tipo de documento incluido en `TIPOS_DEVOLUCION`

Se agrupa por:

- `NIT Emisor`
- `Nombre Emisor`

### Gastos

Documentos donde la empresa es receptora y el documento tiene IVA diferente de cero.

Filtro principal:

- `NIT Receptor == nit`
- Tipo de documento incluido en `TIPOS_GASTO`
- `IVA != 0`

Se agrupa por:

- `NIT Emisor`
- `Nombre Emisor`

### Gastos Excluidos

Incluye dos casos:

Caso 1: facturas recibidas de terceros sin IVA.

- `NIT Receptor == nit`
- Tipo de documento incluido en `TIPOS_GASTO_EXCLUIDO`
- `IVA == 0`

Caso 2: documento soporte emitido por la empresa.

- `NIT Emisor == nit`
- Tipo de documento incluido en `TIPOS_DOC_SOPORTE`

Para gastos excluidos, la columna `Base` se reporta en cero.

### Nomina

Documentos de nomina electronica donde la empresa es emisora.

Filtro principal:

- `NIT Emisor == nit`
- Tipo de documento incluido en `TIPOS_NOMINA`

Se agrupa por:

- `NIT Receptor`
- `Nombre Receptor`

Para nomina, `Base` e `IVA` se reportan en cero.

---

## Calculo De Base Y DV

La base gravable de ingresos, notas credito, devoluciones y gastos se calcula actualmente asi:

```text
Base = IVA / 0.19
```

Esto asume una tarifa general de IVA del 19%.

El digito de verificacion se calcula automaticamente usando el algoritmo de la DIAN. Si el NIT contiene letras, se considera un NIT extranjero y el campo `DV` queda vacio.

---

## Manejo De Errores En La API

Errores de validacion esperados:

- NIT invalido.
- Archivo que no puede abrirse como Excel.
- Columnas obligatorias faltantes.
- Valores no numericos o vacios en `IVA` o `Total`.

Estos errores se devuelven como HTTP `400`.

Errores inesperados durante el procesamiento se devuelven como HTTP `500`.

---

## Notas Tecnicas

- El procesamiento del archivo se realiza en memoria usando `BytesIO`.
- La API devuelve el Excel mediante `StreamingResponse`.
- El archivo de origen puede tener cualquier nombre de hoja; siempre se lee la primera.
- El DataFrame se reduce progresivamente despues de cada modulo para evitar reprocesar filas ya consolidadas.
- En `TIPOS_NOMINA` se conserva el valor `Nomima Individual De Ajustes` porque asi aparece en la fuente de datos.

---

## Pendientes Recomendados

- Estandarizar las columnas finales como `NIT`, `DV`, `Nombre`, `Base`, `IVA`, `Total`.
- Revisar si `Base = IVA / 0.19` es suficiente para todos los casos reales.
- Agregar logs internos para errores HTTP `500`.
- Crear pruebas automaticas para validar filtros y salidas por cada modulo.
- Evaluar si conviene separar lectura, validacion, calculo y escritura en funciones mas pequenas.
