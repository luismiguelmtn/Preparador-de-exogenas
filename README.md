# Preparador de Exógenas DIAN

Herramienta en Python para consolidar la información exógena reportada a la DIAN. A partir de un archivo Excel exportado de la plataforma de facturación electrónica, genera un consolidado por tercero para cada tipo de operación tributaria.

---

## Requisitos

- Python 3.10 o superior
- Librerías listadas en `requirements.txt`

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## Cómo ejecutar

```bash
python main.py
```

El programa solicitará:

1. El archivo Excel con la información exógena (debe estar en la misma carpeta)
2. El NIT de la empresa reportante (sin dígito de verificación)

Al finalizar genera el archivo `consolidado_exogena.xlsx` en la misma carpeta.

---

## Estructura del proyecto

```
Preparador de exogenas/
    main.py                      ← Punto de entrada, coordina todos los módulos
    calculo_ingresos.py          ← Consolidado de ingresos facturados
    calculo_notas_credito.py     ← Consolidado de notas crédito emitidas
    calculo_devoluciones.py      ← Consolidado de devoluciones recibidas
    calculo_gastos.py            ← Consolidado de gastos con IVA
    calculo_gastos_excluidos.py  ← Consolidado de gastos sin IVA
    calculo_nomina.py            ← Consolidado de nómina electrónica
    utils.py                     ← Constantes y funciones compartidas
    requirements.txt             ← Dependencias del proyecto
    .gitignore
```

---

## Resultado

El archivo `consolidado_exogena.xlsx` contiene una hoja por cada tipo de operación:

| Hoja | Contenido |
|---|---|
| Ingresos | Facturas emitidas por la empresa, agrupadas por receptor |
| Notas Crédito | Notas crédito emitidas por la empresa, agrupadas por receptor |
| Devoluciones | Notas crédito recibidas por la empresa, agrupadas por emisor |
| Gastos | Facturas recibidas con IVA, agrupadas por emisor |
| Gastos Excluidos | Facturas recibidas sin IVA, agrupadas por emisor |
| Nóminas | Nómina electrónica emitida, agrupada por receptor |

Cada hoja incluye las columnas: `NIT`, `DV`, `Nombre`, `Base`, `IVA`, `Total`.

---

## Lógica de negocio

La información exógena contiene documentos donde la empresa puede aparecer como emisora o como receptora. Cada módulo aplica filtros distintos según la naturaleza de la operación.

### Ingresos
Documentos donde **la empresa es emisora** — son las facturas que ella generó a sus clientes. Se consolidan agrupando por `NIT Receptor` para totalizar lo facturado a cada cliente.

Tipos de documento: Factura electrónica, Documento equivalente POS, Factura electrónica de contingencia.

### Notas Crédito
Documentos donde **la empresa es emisora** de una nota crédito — son ajustes o correcciones que ella realizó sobre facturas propias. Se consolidan por `NIT Receptor`.

Tipo de documento: Nota de crédito electrónica.

### Devoluciones
Documentos donde **la empresa es receptora** de una nota crédito — son devoluciones que terceros le realizaron a ella. Se consolidan por `NIT Emisor` para identificar quién hizo la devolución.

Tipo de documento: Nota de crédito electrónica.

> La diferencia entre Notas Crédito y Devoluciones es el rol de la empresa: en las primeras es quien emite, en las segundas es quien recibe.

### Gastos
Documentos donde **la empresa es receptora** y el documento tiene IVA — son compras o servicios adquiridos que generan IVA descontable. Se consolidan por `NIT Emisor` para identificar cada proveedor.

La condición `IVA != 0` diferencia estos documentos de los gastos excluidos.

### Gastos Excluidos
Documentos donde **la empresa es receptora** y el documento tiene IVA igual a cero — son compras de bienes o servicios excluidos de IVA. Incluye también los documentos soporte emitidos por la propia empresa, que representan gastos propios sin IVA.

Para estos documentos la base gravable se reporta en cero.

### Nómina
Documentos de nómina electrónica donde **la empresa es emisora** — registra los pagos realizados a cada empleado. Se consolida por `NIT Receptor` (el empleado) para totalizar lo pagado a cada persona.

IVA y Base se reportan en cero ya que la nómina no genera estos conceptos.

> Nota: El archivo exógena incluye el tipo `'Nomima Individual De Ajustes'` con error tipográfico. Este valor se conserva tal como viene en la fuente para garantizar que los filtros funcionen correctamente.

---

## Notas técnicas

- El programa normaliza las columnas `NIT Emisor` y `NIT Receptor` a texto antes de procesar, para manejar correctamente NITs extranjeros que contienen letras.
- El dígito de verificación se calcula automáticamente usando el algoritmo oficial de la DIAN. Para NITs extranjeros la columna `DV` queda vacía.
- El DataFrame se reduce progresivamente después de cada módulo para evitar reprocesar filas ya consolidadas.
- El nombre de la hoja del archivo Excel de origen puede variar — el programa siempre lee la primera hoja sin importar su nombre.
