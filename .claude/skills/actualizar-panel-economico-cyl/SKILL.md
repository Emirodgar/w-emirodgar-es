---
name: actualizar-panel-economico-cyl
description: Actualiza el Panel Económico CyL con el presupuesto autonómico vigente, las subvenciones concedidas, el catálogo de líneas de ayuda y el mercado laboral (paro, afiliación, contratos, detalle por provincia) de la Junta de Castilla y León. Usar cuando el usuario pida "actualiza el Panel Económico CyL", "actualiza el panel de presupuestos de Castilla y León", "refresca los datos de subvenciones/empleo de CyL" o similar.
---

# Actualizar Panel Económico CyL

Este proyecto es un panel público sobre la economía de Castilla y León: presupuesto autonómico,
subvenciones/ayudas y mercado laboral (con detalle por provincia). Toda su información vive en un único
fichero de datos que consumen tanto el panel completo como el widget de la home:

- Dataset: [proyectos/panel-economico-cyl/data.json](../../../proyectos/panel-economico-cyl/data.json)
- Panel completo: [proyectos/panel-economico-cyl/index.html](../../../proyectos/panel-economico-cyl/index.html) (lee `data.json` vía `fetch`)
- Widget de la home: [index.html](../../../index.html) (busca `panelCylSparkline`, también lee el mismo `data.json`)
- Artículo/documentación del proyecto: [publicaciones/proyecto-panel-economico-cyl.md](../../../publicaciones/proyecto-panel-economico-cyl.md)

No hace falta tocar el HTML ni el JavaScript de ninguna de esas páginas: basta con editar `data.json`
siguiendo el esquema descrito abajo. Todo lo demás se renderiza dinámicamente a partir de ese fichero. El
panel tiene dos bloques independientes: **Presupuesto y Subvenciones** (`indicators`, `historicalData`) y
**Mercado Laboral y Actividad Económica** (`indicatorsEmpleo`, `empleoMensual`, `provincias`).

## Esquema de `data.json`

```jsonc
{
  "lastUpdated": "15 de Septiembre, 2026",   // fecha en texto, formato "DD de Mes, AAAA"
  "resumenEjecutivo": "...",                  // 5-7 frases, ver sección "Resumen ejecutivo"
  "sparklineSvg": "<svg ...>...</svg>",       // SVG estático del widget de la home, ver sección "Sparkline SVG"
  "sources": { ... },                          // no cambiar salvo que cambie la fuente de un indicador
  "indicators": [
    {
      "id": "presupuesto" | "brecha" | "concedido" | "catalogo",  // no cambiar los ids
      "title": "...", "currentValue": 14562, "unit": "M€" | "líneas",
      "change": -0.2 | null,   // null si el indicador no tiene un "periodo anterior" comparable (p. ej. "brecha")
      "changeLabel": "...", "description": "...", "target": null,
      "icon": "...", "color": "..."            // no cambiar, son clases visuales fijas
    }
    // ... resto de indicadores, no añadir ni quitar entradas
  ],
  "historicalData": [
    { "year": "2024", "presupuestoTotal": 14562, "importeConcedido": null, "lineasAyudaPublicadas": 108 }
    // una entrada por año, en orden cronológico ascendente; usar null cuando no hay dato para ese año
  ],
  "indicatorsEmpleo": [
    {
      "id": "paro" | "afiliacion" | "contratos" | "indefinidos",  // no cambiar los ids
      "title": "...", "currentValue": 98323, "unit": "personas" | "contratos" | "%",
      "change": 144, "changeLabel": "...", "description": "...", "target": null,
      "icon": "...", "color": "..."
    }
  ],
  "empleoMensual": [
    { "mes": "Ago 2026", "paro": 98323, "afiliacion": 1019088, "contratosIndefinidos": 16799, "contratosTemporales": 37299 }
    // una entrada por mes, orden cronológico ascendente, últimos 13 meses
  ],
  "provincias": [
    { "provincia": "Valladolid", "paro": 21844, "afiliacion": 235569, "contratos": 11476, "pctIndefinido": 34.4 }
    // una entrada por cada una de las 9 provincias, con el dato del mes más reciente disponible
  ],
  "notas": { ... }  // aclaraciones sobre huecos o discontinuidades de las fuentes; mantener y actualizar si aplica
}
```

No existe ya un campo `materias` ni un gráfico de reparto por materia: se retiró porque no aportaba
suficiente valor visual (era un desglose secundario del catálogo de ayudas). No lo reintroduzcas salvo que
el usuario lo pida explícitamente.

## Fuentes y cómo consultarlas

### 1. Catálogo de líneas de ayuda (dataset `ayudas-y-subvenciones`)

```
https://analisis.datosabiertos.jcyl.es/api/explore/v2.1/catalog/datasets/ayudas-y-subvenciones/records?select=year(fecha_publicacion)%20as%20y,count(*)%20as%20n&group_by=year(fecha_publicacion)&order_by=y&limit=30
```

Devuelve el número de líneas publicadas por año (campo `year(fecha_publicacion)`, ignora el campo `y`
que sale siempre `null` — es una peculiaridad de esta API con alias de expresiones agrupadas). Usa estos
valores para actualizar `lineasAyudaPublicadas` en `historicalData` (añade el año más reciente si no está,
o actualiza el del año en curso si sigue siendo parcial). Para el indicador `catalogo` (tarjeta KPI), usa
el valor del año más reciente con dato consolidado (no el año en curso si está muy incompleto) como
`currentValue`, y el del año anterior para calcular `change`.

### 2. Subvenciones concedidas (dataset `subvenciones-concedidas`)

```
https://analisis.datosabiertos.jcyl.es/api/explore/v2.1/catalog/datasets/subvenciones-concedidas/records?select=max(fecha_de_la_concesion)%20as%20maxf
```

Este dataset dejó de actualizarse en marzo de 2022 la última vez que se revisó. **Comprueba primero si
`maxf` ha avanzado** respecto a lo que ya conste en `notas.concedido2022`/`sources.concedido`:

- Si sigue igual (no hay dato posterior a 2022), no toques `historicalData` ni el indicador `concedido`:
  el panel ya refleja correctamente que 2021 es el último año completo.
- Si el dataset se ha reanudado, consulta la agregación por año:
  ```
  https://analisis.datosabiertos.jcyl.es/api/explore/v2.1/catalog/datasets/subvenciones-concedidas/records?select=year(fecha_de_la_concesion)%20as%20y,sum(importe_concesion)%20as%20total,count(*)%20as%20n&group_by=year(fecha_de_la_concesion)&order_by=y&limit=30
  ```
  añade los años nuevos y completos a `historicalData` (excluye años parciales, igual que se hizo con 2022),
  actualiza el indicador `concedido` y actualiza `sources.concedido` y `notas.concedido2022` para reflejar
  que el dataset ya está vivo de nuevo.

### 3. Presupuesto autonómico vigente

No existe una API estructurada fiable para esto: usa WebSearch/WebFetch para localizar, en fuentes
oficiales (BOE, BOCYL, hacienda.jcyl.es) o prensa económica regional solvente (El Debate, El Español,
Diario de León, Castilla y León Económica), dos cosas para el ejercicio en curso:

1. **Si se ha aprobado una Ley de Presupuestos** para el año en curso (o el usuario indica que se acaban
   de aprobar tras las elecciones autonómicas de marzo de 2026): añade una fila nueva a `historicalData`
   con el importe total consolidado aprobado (no el "techo de gasto no financiero", que es una magnitud
   menor y distinta — usa siempre el total del proyecto/ley de presupuestos, la cifra que la prensa suele
   titular como "presupuesto récord de X millones").
2. **Si sigue prorrogado**: repite el valor del año prorrogado (2024: 14.562 M€) en la fila de
   `historicalData` del año en curso, igual que ya se hizo para 2025 y 2026.

Actualiza el indicador `presupuesto` (`currentValue`, `change`, `changeLabel`) y, si hay un nuevo proyecto
de presupuestos rechazado o pendiente de votación, actualiza también el indicador `brecha` (diferencia
entre el importe de ese proyecto y el presupuesto realmente vigente) — si no hay proyecto vivo en ese
momento (por ejemplo, ya se aprobó uno), pon `brecha` a `0` con `changeLabel: "Sin proyecto pendiente"` en
lugar de eliminar la tarjeta.

### 4. Paro registrado (dataset `paro-provincias`)

Serie mensual (una fila por provincia y por mes, más una fila `provincia='CYL'` con el total
autonómico — **no sumes las 9 provincias tú mismo, usa siempre la fila `CYL`, o duplicarás el total**).

```
https://analisis.datosabiertos.jcyl.es/api/explore/v2.1/catalog/datasets/paro-provincias/records?where=provincia=%27CYL%27&select=fecha,total&order_by=fecha%20desc&limit=13
```

Actualiza los últimos 13 meses de `empleoMensual.paro` y el indicador `paro` (compara el último mes con el
mismo mes del año anterior, no con el mes inmediatamente anterior, porque el paro registrado tiene un
patrón estacional fuerte).

### 5. Afiliación media a la Seguridad Social (dataset `afiliacion-media-a-la-seguridad-social-en-las-provincias-de-castilla-y-leon`)

```
https://analisis.datosabiertos.jcyl.es/api/explore/v2.1/catalog/datasets/afiliacion-media-a-la-seguridad-social-en-las-provincias-de-castilla-y-leon/records?where=provincia=%27CYL%27&select=fecha,total&order_by=fecha%20desc&limit=13
```

Igual que el paro: usa la fila `CYL`, actualiza `empleoMensual.afiliacion` y el indicador `afiliacion`
comparando interanualmente (mismo mes, año anterior).

### 6. Contratos registrados (dataset `contratos-realizados-en-las-provincias-de-castilla-y-leon`)

```
https://analisis.datosabiertos.jcyl.es/api/explore/v2.1/catalog/datasets/contratos-realizados-en-las-provincias-de-castilla-y-leon/records?where=provincia=%27CYL%27&select=fecha,total,indefinido,temporal&order_by=fecha%20desc&limit=13
```

Actualiza `empleoMensual.contratosIndefinidos`/`contratosTemporales` con `indefinido`/`temporal`. Para los
indicadores `contratos` (total del mes, interanual) e `indefinidos` (porcentaje `indefinido/total*100` del
mes, comparado con el mismo porcentaje del mismo mes del año anterior — no arrastres el `%` en bruto sin
recalcularlo si cambia el total).

### 7. Detalle por provincia

Repite las consultas 4, 5 y 6 sin el filtro `provincia='CYL'`, para el mes más reciente disponible (usa la
fecha máxima común a los tres datasets — normalmente coincide, pero comprueba `max(fecha)` en cada uno
antes de asumirlo):

```
https://analisis.datosabiertos.jcyl.es/api/explore/v2.1/catalog/datasets/paro-provincias/records?where=fecha=date%27AAAA-MM-DD%27&select=provincia,total&order_by=total%20desc&limit=15
https://analisis.datosabiertos.jcyl.es/api/explore/v2.1/catalog/datasets/afiliacion-media-a-la-seguridad-social-en-las-provincias-de-castilla-y-leon/records?where=fecha=date%27AAAA-MM-DD%27&select=provincia,total&order_by=total%20desc&limit=15
https://analisis.datosabiertos.jcyl.es/api/explore/v2.1/catalog/datasets/contratos-realizados-en-las-provincias-de-castilla-y-leon/records?where=fecha=date%27AAAA-MM-DD%27&select=provincia,total,indefinido,temporal&order_by=total%20desc&limit=15
```

Sustituye `AAAA-MM-DD` por el último día del mes más reciente. Excluye la fila `provincia='CYL'` de estas
tres consultas (es el total, no una provincia) y usa los códigos `VA/LE/BU/SA/SE/PA/ZA/AV/SO` para mapear
al nombre completo de la provincia (Valladolid/León/Burgos/Salamanca/Segovia/Palencia/Zamora/Ávila/Soria).
Reescribe el array `provincias` completo con los 9 registros (calcula `pctIndefinido` = `indefinido/total*100`,
redondeado a 1 decimal), ordenado como prefieras — la tabla y el gráfico ya lo reordenan en pantalla.

## Pasos

1. Lee el `data.json` actual para conocer el último año/mes registrado en `historicalData`/`empleoMensual`
   y el estado de cada fuente (`sources`, `notas`).
2. Consulta las fuentes en este orden: catálogo de ayudas (API), subvenciones concedidas (API, solo para
   comprobar si se ha reanudado), presupuesto autonómico (WebSearch/WebFetch), paro/afiliación/contratos
   CyL (API), detalle por provincia (API).
3. Añade o actualiza las filas de `historicalData` y `empleoMensual` que correspondan, siempre en orden
   cronológico ascendente y sin inventar cifras: si una fuente no tiene dato nuevo, deja el campo como
   estaba (o `null` si nunca lo tuvo). En `empleoMensual`, mantén siempre los últimos 13 meses (añade el
   mes nuevo al final y elimina el más antiguo si ya hay 13).
4. Reescribe `provincias` por completo con el mes más reciente.
5. Actualiza los arrays `indicators` e `indicatorsEmpleo` con los valores más recientes y su `change`
   frente al periodo anterior comparable (interanual para los indicadores de empleo, no intermensual).
6. Actualiza `lastUpdated` con la fecha de ejecución (formato "DD de Mes, AAAA").
7. Reescribe `resumenEjecutivo` (ver siguiente sección).
8. Regenera `sparklineSvg` a partir de los últimos años de `lineasAyudaPublicadas` en `historicalData`
   (ver sección "Sparkline SVG") — obligatorio cada vez que cambie esa serie. El sparkline de la home sigue
   basado en el catálogo de ayudas, no en los datos de empleo; no lo cambies salvo que el usuario lo pida.
9. Si corriges o completas un hueco de datos (por ejemplo, el dataset de concesiones se reanuda), actualiza
   también `sources` y `notas` para que sigan describiendo la situación real.
10. Guarda el fichero validando que sigue siendo JSON válido (revisa comas y llaves).
11. Enseña al usuario un resumen de qué cifras han cambiado antes de dar la tarea por terminada. No hagas
    commit ni push salvo que el usuario lo pida explícitamente.

## Resumen ejecutivo

`resumenEjecutivo` es el texto que se muestra tanto en el panel completo como en el widget de la home.
Debe ser:

- 5-7 frases en español, tono neutro y periodístico (nada de recomendaciones).
- Cubrir ambos bloques: primero la situación presupuestaria (aprobado/prorrogado) y las subvenciones/
  catálogo de ayudas, después el mercado laboral (paro, afiliación, temporalidad) y algún contraste entre
  provincias si es relevante (p. ej. la que más/menos temporalidad tiene, o la que concentra más volumen).
- Sin cifras inventadas: solo las que consten en `indicators`/`indicatorsEmpleo`/`historicalData`/
  `empleoMensual`/`provincias` tras la actualización.

## Sparkline SVG

El widget de la home ya no usa Chart.js (por peso de la librería para un gráfico decorativo pequeño):
`sparklineSvg` es un SVG estático, autocontenido, con la evolución de `lineasAyudaPublicadas` de los
últimos años de `historicalData` (usa los últimos 6-8 años disponibles, ajusta `n` en el script si cambia
la cantidad). La home simplemente hace `elemento.innerHTML = dataset.sparklineSvg`, así que el SVG debe
ser válido por sí solo (sin dependencias externas) y usar comillas dobles en sus atributos.

No lo edites a mano: ejecuta este script (ajustando solo la ruta si hace falta) cada vez que cambie la
serie de `lineasAyudaPublicadas`, y copia el resultado tal cual al campo `sparklineSvg`:

```python
import json
from collections import OrderedDict

path = 'proyectos/panel-economico-cyl/data.json'
with open(path, encoding='utf-8') as f:
    data = json.load(f, object_pairs_hook=OrderedDict)

hist = [h for h in data['historicalData'] if h.get('lineasAyudaPublicadas') is not None][-8:]
vals = [h['lineasAyudaPublicadas'] for h in hist]

vmin, vmax = min(vals), max(vals)
rng = vmax - vmin
pad = rng * 0.15 if rng > 0 else max(vmax * 0.15, 1)
pmin, pmax = vmin - pad, vmax + pad
prange = pmax - pmin

x0, x1 = 12, 308
y_top, y_bottom = 10, 100
n = len(vals)
step = (x1 - x0) / (n - 1)

def xy(i, v):
    x = x0 + i * step
    y = y_bottom - ((v - pmin) / prange) * (y_bottom - y_top)
    return round(x, 1), round(y, 1)

pts = [xy(i, v) for i, v in enumerate(vals)]

def fmt(pts):
    return " ".join(f"{x},{y}" for x, y in pts)

line = fmt(pts)
area = f"{line} {x1},{y_bottom} {x0},{y_bottom}"

circles = "".join(
    f'<circle cx="{x}" cy="{y}" r="{2.5 if i < n-1 else 3}" fill="#7c3aed"/>'
    for i, (x, y) in enumerate(pts)
)

svg = (
    '<svg viewBox="0 0 320 110" xmlns="http://www.w3.org/2000/svg" '
    'preserveAspectRatio="none" role="img" '
    'aria-label="Evolucion de lineas de ayuda publicadas por la Junta de Castilla y Leon" '
    'style="width:100%;height:100%">'
    f'<polygon points="{area}" fill="rgba(124,58,237,0.08)"/>'
    f'<polyline points="{line}" fill="none" stroke="#7c3aed" stroke-width="2.5" '
    'stroke-linecap="round" stroke-linejoin="round"/>'
    f'{circles}'
    '</svg>'
)

new_data = OrderedDict()
for k, v in data.items():
    new_data[k] = v
    if k == 'resumenEjecutivo':
        new_data['sparklineSvg'] = svg

with open(path, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)
    f.write('\n')
```

Qué hace: normaliza los valores de `lineasAyudaPublicadas` (últimos 6-8 años con dato) entre el mínimo y
el máximo (con un 15% de margen visual), los reparte a lo largo de un `viewBox` de 320×110, y dibuja el
área bajo la línea (relleno violeta claro) y la línea (sólida, violeta), con puntos en cada año. El color
(`#7c3aed`) está fijado a mano para que combine con la leyenda estática de `index.html`
(`.legend-swatch--violet`) — si cambia ese color en `styles.css`, cámbialo también aquí.

El panel completo ([proyectos/panel-economico-cyl/index.html](../../../proyectos/panel-economico-cyl/index.html))
sigue usando Chart.js con sus 7 gráficos interactivos (3 de presupuesto/subvenciones + 4 de mercado
laboral) — eso no cambia, solo se quitó Chart.js de la home.

## Notas

- Los datos publicados en la versión ampliada de este panel (septiembre de 2026) ya son cifras reales
  obtenidas de la API de datos abiertos de la Junta y de fuentes de prensa/BOE, no una muestra ilustrativa.
- No es necesario tocar `sources` salvo que cambie la metodología, la fuente de un indicador, o se resuelva
  el hueco de datos de `subvenciones-concedidas`.
- Los datos de empleo (paro, afiliación, contratos) se publican con un desfase de aproximadamente un mes:
  no esperes que "el mes en curso" tenga ya dato disponible.
- Este panel no cubre presupuestos municipales, contratación pública (PLACSP), PIB provincial ni el BOCYL
  en general — solo presupuesto autonómico, subvenciones, catálogo de ayudas y el mercado laboral (paro,
  afiliación, contratos) por provincia.
- Si el usuario pide explícitamente publicar los cambios, sigue el flujo normal de git (revisar diff,
  commit con mensaje descriptivo); no lo hagas por iniciativa propia.
