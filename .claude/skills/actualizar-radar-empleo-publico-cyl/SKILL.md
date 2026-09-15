---
name: actualizar-radar-empleo-publico-cyl
description: Actualiza el Radar de Empleo Público CyL con las convocatorias, plazas ofertadas, bolsas de empleo, sedes de examen, la plantilla de la Junta por provincia, los perfiles profesionales más demandados y el listado de las últimas convocatorias publicadas. Usar cuando el usuario pida "actualiza el Radar de Empleo Público CyL", "actualiza el panel de oposiciones de Castilla y León", "refresca las convocatorias/plantilla de CyL" o similar.
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
  "perfiles": [
    { "perfil": "Administración General", "convocatorias": 21, "plazas": 2179 }
    // reparto de plazas por perfil profesional, ver sección 7 más abajo; no añadir/quitar perfiles
    // salvo que se reclasifique todo el histórico (ver esa sección)
  ],
  "convocatoriasRecientes": [
    {
      "titulo": "...", "municipio": "Valladolid", "plazas": 8,
      "fechaPublicacion": "2026-07-27", "fechaLimite": "2026-08-24",
      "estado": "abierta" | "cerrada", "enlace": "https://empleopublico.jcyl.es/..."
    }
    // las 15 convocatorias más recientes por fechaPublicacion, orden descendente
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

### 7. Perfiles profesionales más demandados

Vuelve al dataset `convocatorias-de-empleo-publico`. Descarga el `titulo` y `numeroplazas` de todas las
convocatorias (`tipo='Convocatoria'`) publicadas desde el 1 de enero de 2023 (usa
`where=tipo%3D%27Convocatoria%27%20AND%20fechabocyl%20%3E%3D%20date%272023-01-01%27`), paginando con
`limit`/`offset` si hace falta (esta API pagina en bloques de 100). No amplíes el rango a años anteriores:
las convocatorias de 2019-2022 son en su mayoría concursos de "estabilización de empleo temporal Ley
20/2021" que agrupan varios cuerpos distintos bajo un único título (p. ej. "Concurso Titulado Superior y
Titulado de Grado Medio") y no se pueden clasificar de forma fiable por perfil.

Clasifica cada `titulo` en uno de estos 8 perfiles, por coincidencia de palabras clave (case-insensitive),
en este orden de prioridad (para cuando un título encaje en más de uno, gana el primero que coincida):

1. **Sanidad**: médic, sanitari, sanidad, salud, farmac, veterinari, ats, due, enfermer, matrona, odont,
   dentist, psiquiatr, fisioterap, epidemiolog, laboratorio, químic, biólog
2. **Ingeniería y Técnicos**: ingenier, arquitect, geólog, delineante, informátic, "técnico de sistemas",
   "técnico de información"
3. **Administración General**: "cuerpo superior", "cuerpo de gestión", "cuerpo auxiliar", administrativ,
   "auxiliar administrativ", "técnico de administración", letrad, auditoría
4. **Servicios Sociales y Educación**: "trabajador social", "trabajadores sociales", educador, "integrador
   social", "servicios sociales", discapacidad, psicólog, pedagog, "atención directa", terapeuta,
   logopeda, "asistente social", "asistentes sociales", "educación infantil", "apoyo al menor", "gestión
   cultural", museo, psicomotricista
5. **Medio Ambiente y Montes**: "medio ambiente", "agente medioambiental", "agentes medioambientales",
   montes, pecuari, incendio, forestal
6. **Oficios y Mantenimiento**: conductor, cocina, mantenimiento, oficial, celador, "personal de
   servicios", almacener, gobernant, biblioteca, archiv, subalterno, "auxiliar de carreteras", capataz,
   tractorista, encargad, "operador de centro de mando"
7. **Inspección y Consumo**: inspector
8. **Otros perfiles**: cualquier título que no encaje en ninguno de los anteriores (debería ser una
   fracción pequeña, por debajo del 10% de las plazas del periodo — si sale mucho mayor, revisa si algún
   patrón de título nuevo y frecuente merece su propia categoría o encaja en una existente)

Reescribe `perfiles` por completo con la suma de `convocatorias` (nº de filas) y `plazas`
(`numeroplazas`) de cada perfil, para todo el rango 2023-en curso (no solo el año más reciente). No crees
una categoría nueva sin decírselo antes al usuario: los 8 perfiles anteriores son fijos salvo que se pida
explícitamente ampliarlos.

### 8. Últimas convocatorias publicadas

```
https://analisis.datosabiertos.jcyl.es/api/explore/v2.1/catalog/datasets/convocatorias-de-empleo-publico/records?where=tipo%3D%27Convocatoria%27&select=titulo,numeroplazas,municipio,fechabocyl,fechafinalizacion,enlace_al_contenido&order_by=fechabocyl%20desc&limit=15
```

Reescribe `convocatoriasRecientes` por completo con estas 15 filas: `fechaPublicacion` = `fechabocyl`,
`fechaLimite` = `fechafinalizacion`, `municipio` = el valor del campo (o `"Sin especificar"` si es `null`),
`enlace` = `enlace_al_contenido`. Calcula `estado` comparando `fechaLimite` con la fecha de esta
actualización: `"abierta"` si `fechaLimite >= hoy`, `"cerrada"` en caso contrario — no dejes un `estado`
de una ejecución anterior sin recalcular, ya que una convocatoria puede cerrarse entre una actualización y
la siguiente sin que cambie ningún otro dato suyo.

## Pasos

1. Lee el `data.json` actual para conocer el último año/mes registrado en `historicalData`/`provincias`/
   `convocatoriasRecientes` y el estado de `notas` (qué años están marcados como incompletos, qué fecha
   semestral se usó para `efectivos`).
2. Ejecuta las 8 consultas anteriores contra la API (la de plantilla, sección 6, solo si hay una fecha
   semestral más reciente disponible; la de perfiles, sección 7, siempre que haya convocatorias nuevas
   desde la última actualización, para no reclasificar sin necesidad).
3. Actualiza `historicalData`, `sedes`, `provincias` (si aplica), `perfiles` (si aplica) y los 5
   indicadores con los valores obtenidos, calculando `change` frente al periodo anterior comparable cuando
   aplique (déjalo en `null` para `historico`, que no tiene un "periodo anterior" natural).
4. Reescribe `convocatoriasRecientes` por completo (sección 8) — esto debe hacerse siempre, incluso si no
   hay convocatorias nuevas, porque el campo `estado` de las ya existentes puede haber cambiado de
   "abierta" a "cerrada".
5. Actualiza `lastUpdated` con la fecha de ejecución (formato "DD de Mes, AAAA").
6. Reescribe `resumenEjecutivo` (ver siguiente sección).
7. Regenera `sparklineSvg` a partir de la serie de `plazas` en `historicalData` (ver sección "Sparkline
   SVG") — obligatorio cada vez que cambie esa serie. El sparkline sigue basado en plazas de oposiciones,
   no en la plantilla ni en los perfiles; no lo cambies salvo que el usuario lo pida.
8. Actualiza `notas` si un año pasa de "incompleto" a "completo", si se publica una fecha semestral nueva
   de plantilla, o si detectas cualquier otro cambio en la disponibilidad de los campos del dataset.
9. Guarda el fichero validando que sigue siendo JSON válido (revisa comas y llaves).
10. Enseña al usuario un resumen de qué cifras han cambiado, y en particular si hay alguna convocatoria
    con plazo abierto ahora mismo (es el dato con más interés práctico del panel). No hagas commit ni push
    salvo que el usuario lo pida explícitamente.

## Resumen ejecutivo

`resumenEjecutivo` es el texto que se muestra tanto en el panel completo como en el widget de la home.
Debe ser:

- 5-7 frases en español, tono neutro y periodístico.
- Cubrir primero convocatorias/plazas (cómo ha evolucionado el número, si hay algo con el plazo abierto
  ahora mismo — es lo más útil para quien consulta el panel — y cualquier concentración relevante por
  sede de examen), después el perfil profesional que más plazas concentra si hay un cambio relevante, y
  por último la plantilla por provincia (variación interanual del total autonómico, y qué provincias suben
  o bajan si el contraste es relevante).
- Sin cifras inventadas: solo las que consten en `indicators`/`historicalData`/`sedes`/`provincias`/
  `perfiles`/`convocatoriasRecientes` tras la actualización.

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
sigue usando Chart.js con sus 6 gráficos interactivos — eso no cambia, solo se quitó Chart.js de la home.

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
- La clasificación por perfil (`perfiles`) es una interpretación propia por palabras clave, no un campo
  oficial del dataset — puede haber casos límite discutibles, sobre todo en "Otros perfiles"; no la
  presentes como una taxonomía oficial de la Junta en `resumenEjecutivo` ni en la documentación.
- Si el usuario pide explícitamente publicar los cambios, sigue el flujo normal de git (revisar diff,
  commit con mensaje descriptivo); no lo hagas por iniciativa propia.
