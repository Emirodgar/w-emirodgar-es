---
name: actualizar-radar-empleo-publico-cyl
description: Actualiza el Radar de Empleo Público CyL con las convocatorias, plazas ofertadas, bolsas de empleo, sedes de examen y la plantilla de la Junta por provincia. Usar cuando el usuario pida "actualiza el Radar de Empleo Público CyL", "actualiza el panel de oposiciones de Castilla y León", "refresca las convocatorias/plantilla de CyL" o similar.
---

# Actualizar Radar de Empleo Público CyL

Este proyecto es un panel público sobre las convocatorias de empleo público (oposiciones y bolsas de
empleo) y la plantilla real de la Junta de Castilla y León, con detalle por provincia. Toda su
información vive en un único fichero de datos que consumen tanto el panel completo como el widget de la
home:

- Dataset: [proyectos/radar-empleo-publico-cyl/data.json](../../../proyectos/radar-empleo-publico-cyl/data.json)
- Panel completo: [proyectos/radar-empleo-publico-cyl/index.html](../../../proyectos/radar-empleo-publico-cyl/index.html) (lee `data.json` vía `fetch`)
- Widget de la home: [index.html](../../../index.html) (busca `radarEmpleoSparkline`, también lee el mismo `data.json`)
- Artículo/documentación del proyecto: [publicaciones/proyecto-radar-empleo-publico-cyl.md](../../../publicaciones/proyecto-radar-empleo-publico-cyl.md)

No hace falta tocar el HTML ni el JavaScript de ninguna de esas páginas: basta con editar `data.json`
siguiendo el esquema descrito abajo. Todo lo demás se renderiza dinámicamente a partir de ese fichero.

## Esquema de `data.json`

```jsonc
{
  "lastUpdated": "15 de Septiembre, 2026",
  "resumenEjecutivo": "...",                  // 2-4 frases, ver sección "Resumen ejecutivo"
  "sparklineSvg": "<svg ...>...</svg>",       // SVG estático del widget de la home, ver sección "Sparkline SVG"
  "sources": { ... },
  "indicators": [
    {
      "id": "convocatorias" | "plazas" | "historico" | "abiertas" | "efectivos",  // no cambiar los ids
      "title": "...", "currentValue": 77, "unit": "convocatorias" | "plazas" | "efectivos",
      "change": 19 | null, "changeLabel": "...", "description": "...", "target": null,
      "icon": "...", "color": "..."
    }
  ],
  "historicalData": [
    { "year": "2025", "convocatorias": 77, "plazas": 1418, "bolsasEmpleo": 0 }
    // una entrada por año, en orden cronológico ascendente
  ],
  "sedes": [
    { "sede": "Valladolid", "plazas": 4132 }
    // reparto de plazas por sede de EXAMEN, de mayor a menor; incluir "Sin especificar" si hay nulos
  ],
  "provincias": [
    { "provincia": "Valladolid", "efectivos": 21173, "efectivosAnterior": 20977, "variacion": 196 }
    // plantilla real de la Junta por provincia (destino, no sede de examen); una entrada por cada
    // una de las 9 provincias
  ],
  "notas": { ... }
}
```

No confundas `sedes` (dónde se examinan las oposiciones, dataset `convocatorias-de-empleo-publico`) con
`provincias` (dónde trabaja realmente el personal, dataset `estadisticas-de-personal`): son fuentes y
preguntas distintas y ambas tienen su propio gráfico en el panel.

## Fuente de datos: dataset `convocatorias-de-empleo-publico`

Es un dataset del portal de datos abiertos de la Junta, consultable sin autenticación vía API
OpenDataSoft. Todas las consultas siguientes filtran por `tipo='Convocatoria'` salvo que se indique lo
contrario (el dataset también incluye `tipo='Bolsa de Empleo'`, que se trata aparte).

### 1. Convocatorias y plazas por año

```
https://analisis.datosabiertos.jcyl.es/api/explore/v2.1/catalog/datasets/convocatorias-de-empleo-publico/records?where=tipo%3D%27Convocatoria%27&select=year(fechabocyl)%20as%20y,count(*)%20as%20n,sum(numeroplazas)%20as%20plazas&group_by=year(fechabocyl)&order_by=y
```

Actualiza `historicalData`: `convocatorias` = `n`, `plazas` = `plazas`, para cada año. Añade el año en
curso si no está, o actualízalo si sigue incompleto (indícalo en `notas`, igual que se hizo con 2026 en
la primera versión).

### 2. Bolsas de empleo por año

```
https://analisis.datosabiertos.jcyl.es/api/explore/v2.1/catalog/datasets/convocatorias-de-empleo-publico/records?where=tipo%3D%27Bolsa%20de%20Empleo%27&select=year(fechabocyl)%20as%20y,count(*)%20as%20n&group_by=year(fechabocyl)&order_by=y
```

Actualiza `bolsasEmpleo` en `historicalData` para cada año (usa `0` si un año no aparece en el
resultado, no lo dejes vacío).

### 3. Plazas por sede de examen

```
https://analisis.datosabiertos.jcyl.es/api/explore/v2.1/catalog/datasets/convocatorias-de-empleo-publico/records?where=tipo%3D%27Convocatoria%27&select=municipio,count(*)%20as%20n,sum(numeroplazas)%20as%20plazas&group_by=municipio&order_by=plazas%20desc&limit=15
```

Reescribe `sedes` de mayor a menor `plazas`. El valor `municipio: null` corresponde a convocatorias sin
sede especificada: inclúyelo como `{"sede": "Sin especificar", "plazas": ...}`, no lo omitas (es una
fracción grande del total y ocultarlo distorsionaría el gráfico).

### 4. Total histórico acumulado

```
https://analisis.datosabiertos.jcyl.es/api/explore/v2.1/catalog/datasets/convocatorias-de-empleo-publico/records?where=tipo%3D%27Convocatoria%27&select=sum(numeroplazas)%20as%20total
```

Usa este valor para el indicador `historico` (`currentValue`), y actualiza su `changeLabel` si cambia el
rango de años cubierto (por ejemplo, "Total del catálogo histórico disponible (2020-2027)").

### 5. Convocatorias con plazo abierto ahora mismo

```
https://analisis.datosabiertos.jcyl.es/api/explore/v2.1/catalog/datasets/convocatorias-de-empleo-publico/records?where=tipo%3D%27Convocatoria%27%20AND%20fechafinalizacion%20%3E%3D%20date%27AAAA-MM-DD%27&order_by=fechafinalizacion%20asc
```

Sustituye `AAAA-MM-DD` por la fecha de hoy. Usa el `total_count` para el indicador `abiertas`. Si es `0`,
consulta también la convocatoria más reciente (`order_by=fechabocyl%20desc&limit=1`) para poner en la
`description` cuál fue la última publicada y cuándo, igual que en la primera versión del panel. Si hay
convocatorias abiertas, lista en la `description` cuántas y, si caben, sus títulos y fecha límite más
próxima.

### 6. Plantilla de la Junta por provincia (dataset `estadisticas-de-personal`)

Este dataset es distinto del anterior: es semestral (una foto en enero y otra en julio de cada año, no
mensual ni por convocatoria), y da la plantilla real por provincia de destino.

```
https://analisis.datosabiertos.jcyl.es/api/explore/v2.1/catalog/datasets/estadisticas-de-personal/records?select=fecha&group_by=fecha&order_by=fecha%20desc&limit=3
```

Comprueba primero si hay una fecha más reciente que la que ya conste en `notas.efectivosFrecuencia`/el
`indicators.efectivos.title` actual (formato "Personal de la Junta (Mes AAAA)"). Si no hay fecha nueva, no
toques `indicators.efectivos` ni `provincias` — no vuelvas a calcular con datos ya usados. Si la hay:

```
https://analisis.datosabiertos.jcyl.es/api/explore/v2.1/catalog/datasets/estadisticas-de-personal/records?where=fecha=date%27AAAA-MM-DD%27&select=provincia,sum(efectivos)%20as%20total&group_by=provincia&order_by=total%20desc&limit=15
```

Sustituye `AAAA-MM-DD` por la fecha más reciente, y repite la misma consulta con la fecha de un año antes
(mismo mes, año anterior) para calcular la variación interanual de cada provincia. El campo `provincia`
viene en mayúsculas para algunas provincias y con mayúscula inicial para otras (p. ej. `VALLADOLID` vs
`León`): normaliza siempre a "Mayúscula inicial" (Valladolid, León, Burgos, Salamanca, Zamora, Ávila,
Segovia, Palencia, Soria) al escribir `provincias`. Reescribe el array `provincias` completo con las 9
filas (`efectivos` = valor del mes nuevo, `efectivosAnterior` = valor de hace un año, `variacion` =
diferencia). Suma las 9 provincias (o, si quieres evitar redondeos, repite la consulta sin `group_by` para
el total autonómico) para actualizar el indicador `efectivos` (`currentValue`, `change`, `changeLabel` con
el mes/año de comparación, `title` con el mes/año del dato nuevo).

## Pasos

1. Lee el `data.json` actual para conocer el último año/mes registrado en `historicalData`/`provincias` y
   el estado de `notas` (qué años están marcados como incompletos, qué fecha semestral se usó para
   `efectivos`).
2. Ejecuta las 6 consultas anteriores contra la API (la de plantilla, sección 6, solo si hay una fecha
   semestral más reciente disponible).
3. Actualiza `historicalData`, `sedes`, `provincias` (si aplica) y los 5 indicadores con los valores
   obtenidos, calculando `change` frente al periodo anterior comparable cuando aplique (déjalo en `null`
   para `historico`, que no tiene un "periodo anterior" natural).
4. Actualiza `lastUpdated` con la fecha de ejecución (formato "DD de Mes, AAAA").
5. Reescribe `resumenEjecutivo` (ver siguiente sección).
6. Regenera `sparklineSvg` a partir de la serie de `plazas` en `historicalData` (ver sección "Sparkline
   SVG") — obligatorio cada vez que cambie esa serie. El sparkline sigue basado en plazas de oposiciones,
   no en la plantilla; no lo cambies salvo que el usuario lo pida.
7. Actualiza `notas` si un año pasa de "incompleto" a "completo", si se publica una fecha semestral nueva
   de plantilla, o si detectas cualquier otro cambio en la disponibilidad de los campos del dataset.
8. Guarda el fichero validando que sigue siendo JSON válido (revisa comas y llaves).
9. Enseña al usuario un resumen de qué cifras han cambiado, y en particular si hay alguna convocatoria
   con plazo abierto ahora mismo (es el dato con más interés práctico del panel). No hagas commit ni push
   salvo que el usuario lo pida explícitamente.

## Resumen ejecutivo

`resumenEjecutivo` es el texto que se muestra tanto en el panel completo como en el widget de la home.
Debe ser:

- 4-6 frases en español, tono neutro y periodístico.
- Cubrir primero convocatorias/plazas (cómo ha evolucionado el número, si hay algo con el plazo abierto
  ahora mismo — es lo más útil para quien consulta el panel — y cualquier concentración relevante por
  sede de examen), y después la plantilla por provincia (variación interanual del total autonómico, y qué
  provincias suben o bajan si el contraste es relevante).
- Sin cifras inventadas: solo las que consten en `indicators`/`historicalData`/`sedes`/`provincias` tras
  la actualización.

## Sparkline SVG

El widget de la home ya no usa Chart.js: `sparklineSvg` es un SVG estático, autocontenido, con la
evolución de `plazas` de los últimos años de `historicalData` (usa los últimos 6-7 años disponibles). La
home simplemente hace `elemento.innerHTML = dataset.sparklineSvg`, así que el SVG debe ser válido por sí
solo (sin dependencias externas) y usar comillas dobles en sus atributos.

No lo edites a mano: ejecuta este script (ajustando solo la ruta si hace falta) cada vez que cambie la
serie de `plazas`, y copia el resultado tal cual al campo `sparklineSvg`:

```python
import json
from collections import OrderedDict

path = 'proyectos/radar-empleo-publico-cyl/data.json'
with open(path, encoding='utf-8') as f:
    data = json.load(f, object_pairs_hook=OrderedDict)

hist = [h for h in data['historicalData'] if h.get('plazas') is not None][-7:]
vals = [h['plazas'] for h in hist]

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
    f'<circle cx="{x}" cy="{y}" r="{2.5 if i < n-1 else 3}" fill="#2563eb"/>'
    for i, (x, y) in enumerate(pts)
)

svg = (
    '<svg viewBox="0 0 320 110" xmlns="http://www.w3.org/2000/svg" '
    'preserveAspectRatio="none" role="img" '
    'aria-label="Evolucion de plazas ofertadas en convocatorias de empleo publico de Castilla y Leon" '
    'style="width:100%;height:100%">'
    f'<polygon points="{area}" fill="rgba(37,99,235,0.08)"/>'
    f'<polyline points="{line}" fill="none" stroke="#2563eb" stroke-width="2.5" '
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

Qué hace: normaliza los valores de `plazas` (últimos 6-7 años) entre el mínimo y el máximo (con un 15% de
margen visual), los reparte a lo largo de un `viewBox` de 320×110, y dibuja el área bajo la línea (relleno
azul claro) y la línea (sólida, azul), con puntos en cada año. El color (`#2563eb`) está fijado a mano
para que combine con la leyenda estática de `index.html` (`.legend-swatch--blue`) — si cambia ese color en
`styles.css`, cámbialo también aquí.

El panel completo ([proyectos/radar-empleo-publico-cyl/index.html](../../../proyectos/radar-empleo-publico-cyl/index.html))
sigue usando Chart.js con sus 5 gráficos interactivos — eso no cambia, solo se quitó Chart.js de la home.

## Notas

- Los datos publicados en la versión ampliada de este panel (septiembre de 2026) ya son cifras reales
  obtenidas de la API de datos abiertos de la Junta, no una muestra ilustrativa.
- El dataset de convocatorias no incluye un campo limpio de subgrupo (A1/A2/C1/C2) ni de cuerpo/
  especialidad agregable (esa información solo aparece en tablas de texto libre dentro de cada
  convocatoria); no intentes extraerla automáticamente salvo que el usuario pida explícitamente ampliar
  el panel en esa dirección.
- El campo `municipio` de `convocatorias-de-empleo-publico` refleja la sede del examen, no el destino de
  la plaza — mantén esa aclaración en el panel y en `notas.sede` aunque cambien las cifras. El array
  `provincias` (dataset `estadisticas-de-personal`) sí es la provincia real de destino del personal.
- `estadisticas-de-personal` se actualiza solo dos veces al año (enero/julio): no esperes un dato nuevo
  cada vez que ejecutes esta skill, y no lo fuerces a cambiar solo por "hace tiempo que no se actualiza".
- Si el usuario pide explícitamente publicar los cambios, sigue el flujo normal de git (revisar diff,
  commit con mensaje descriptivo); no lo hagas por iniciativa propia.
