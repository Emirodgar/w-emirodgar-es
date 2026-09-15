---
name: actualizar-macrodata-espana
description: Actualiza el panel MacroData España con las últimas cifras oficiales de IPC, prima de riesgo, tipos del BCE, Euríbor, PIB y la comparativa España vs. eurozona (IPCA, PIB, paro armonizado). Usar cuando el usuario pida "actualiza MacroData", "actualiza el panel económico", "refresca los indicadores económicos" o similar.
---

# Actualizar MacroData España

Este proyecto es un panel público de indicadores macroeconómicos de España. Toda su información
vive en un único fichero de datos que consumen tanto el panel completo como el widget de la home:

- Dataset: [proyectos/macrodata-espana/data.json](../../../proyectos/macrodata-espana/data.json)
- Panel completo: [proyectos/macrodata-espana/index.html](../../../proyectos/macrodata-espana/index.html) (lee `data.json` vía `fetch`)
- Widget de la home: [index.html](../../../index.html) (busca `macrodataSparkline`, también lee el mismo `data.json`)
- Artículo/documentación del proyecto: [publicaciones/proyecto-macrodata-espana.md](../../../publicaciones/proyecto-macrodata-espana.md)

No hace falta tocar el HTML ni el JavaScript de ninguna de esas páginas: basta con editar `data.json`
siguiendo el esquema descrito abajo. Todo lo demás se renderiza dinámicamente a partir de ese fichero.

## Esquema de `data.json`

```jsonc
{
  "lastUpdated": "05 de Septiembre, 2026",   // fecha en texto, formato "DD de Mes, AAAA"
  "resumenEjecutivo": "...",                  // 2-4 frases, ver sección "Resumen ejecutivo"
  "sparklineSvg": "<svg ...>...</svg>",       // SVG estático del widget de la home, ver sección "Sparkline SVG"
  "sources": { ... },                          // no cambiar salvo que cambie la fuente de un indicador
  "indicators": [
    {
      "id": "ipc" | "prima" | "bce" | "pib",  // no cambiar los ids, se usan como referencia visual
      "title": "...",
      "currentValue": 2.3,                     // último valor disponible
      "unit": "%" | "pb",
      "change": -0.2,                          // variación respecto al periodo anterior (mismo signo)
      "changeLabel": "vs mes anterior" | "Última decisión" | "Tasa interanual",
      "description": "...",
      "target": 2.0 | null,
      "icon": "...", "color": "..."            // no cambiar, son clases visuales fijas
    }
    // ... resto de indicadores, no añadir ni quitar entradas
  ],
  "historicalData": [
    { "month": "Sep 2025", "ipc": 3.5, "ipcSubyacente": 3.8, "primaRiesgo": 105, "tiposBCE": 4.25, "euribor": 4.12, "pib": 1.8 }
    // una entrada por mes, en orden cronológico ascendente
  ],
  "comparativaZonaEuro": [
    {
      "id": "ipc" | "pib" | "paro",  // no cambiar los ids ni añadir/quitar entradas
      "title": "...", "periodo": "Agosto 2026, dato preliminar",
      "valorEspana": 4.5, "valorZonaEuro": 3.3, "unidad": "%",
      "mejorSiMayor": false   // true si un valor más alto es mejor (PIB); false si es peor (inflación, paro)
    }
  ]
}
```

## Fuentes oficiales por indicador

Busca siempre el dato **más reciente ya publicado** (no proyecciones ni estimaciones de terceros) en:

1. **IPC general y subyacente** (`ipc`, `ipcSubyacente`): INE, Índice de Precios de Consumo — tasa de
   variación interanual. Nota de prensa mensual en ine.es (búsqueda: "INE IPC tasa interanual [mes] [año]").
2. **Prima de riesgo** (`primaRiesgo`): diferencial en puntos básicos entre la rentabilidad del bono
   español a 10 años y el bono alemán a 10 años (Bund). Fuentes: Banco de España, Tesoro Público, o un
   agregador fiable (p. ej. datosmacro.expansion.com, investing.com) contrastando con al menos dos fuentes
   si el dato no es oficial.
3. **Tipo de interés del BCE** (`tiposBCE`): tipo de la facilidad principal de financiación fijado por el
   Consejo de Gobierno del BCE (ecb.europa.eu, sección "Monetary policy decisions"). Solo cambia tras una
   reunión del BCE; si no ha habido reunión desde la última actualización, mantener el valor.
4. **Euríbor a 12 meses** (`euribor`): media mensual publicada por el Banco de España (o euribor-rates.eu /
   EMMI) para el mes cerrado más reciente.
5. **PIB** (`pib`): INE, Contabilidad Nacional Trimestral de España (CNTR) — tasa de variación interanual
   del trimestre más reciente publicado. El PIB es trimestral: no cambia cada mes, solo cuando el INE
   publica un nuevo trimestre.

Usa WebSearch/WebFetch para localizar la cifra en la fuente oficial. Si una fuente no tiene el dato del
periodo más reciente (p. ej. el INE aún no ha publicado el mes en curso), usa el último dato disponible y
no inventes cifras.

## Comparativa España vs. Zona Euro (`comparativaZonaEuro`)

Estos tres indicadores usan magnitudes de **Eurostat**, metodológicamente distintas de las nacionales del
INE que usa el resto del panel (por eso el valor de España en `comparativaZonaEuro.ipc` puede no coincidir
con `indicators.ipc`): no los confundas ni intentes "cuadrarlos".

1. **`ipc`**: IPC Armonizado (IPCA) — busca "Eurostat IPCA [mes] [año] España eurozona" o "flash estimate
   HICP inflation euro area [mes] [año]". Es un dato preliminar mensual.
2. **`pib`**: variación interanual del PIB — busca "Eurostat PIB [trimestre] [año] España eurozona
   interanual". Trimestral, con retraso de 1-2 meses respecto al cierre del trimestre.
3. **`paro`**: tasa de desempleo armonizada — busca "Eurostat tasa de desempleo [mes] [año] España
   eurozona". Mensual, con un desfase de publicación de 1-2 meses (distinta de la tasa de paro EPA
   trimestral del INE, que no está en este panel).

Actualiza `valorEspana`, `valorZonaEuro` y `periodo` para cada uno solo cuando haya un dato nuevo
publicado; no fuerces un cambio si Eurostat no ha actualizado esa serie desde la última ejecución. No
cambies `mejorSiMayor` (es una propiedad del tipo de métrica: PIB `true`, IPC y paro `false`).

## Pasos

1. Lee el `data.json` actual para conocer el último mes registrado en `historicalData` y los periodos ya
   usados en `comparativaZonaEuro`.
2. Para cada indicador nacional, busca el dato oficial más reciente (puede ser el mismo mes si aún no hay
   uno nuevo, o uno o varios meses posteriores si ha pasado tiempo desde la última actualización).
3. Si hay un mes nuevo que aún no está en `historicalData`, añade una entrada nueva al final del array
   (orden cronológico ascendente) con los seis valores (`ipc`, `ipcSubyacente`, `primaRiesgo`, `tiposBCE`,
   `euribor`, `pib`). Si un indicador trimestral (PIB) no tiene dato nuevo para ese mes, repite el último
   valor conocido en lugar de dejarlo vacío.
4. Actualiza el array `indicators`:
   - `currentValue`: el valor de la entrada más reciente de `historicalData` para ese indicador (para
     `prima` usa `primaRiesgo`, para `bce` usa `tiposBCE`).
   - `change`: diferencia entre el valor actual y el del periodo anterior (mismo signo que la variación
     real, sin redondear de forma distinta a los datos de origen).
5. Actualiza `comparativaZonaEuro` (ver sección anterior) para los indicadores que tengan dato nuevo de
   Eurostat.
6. Actualiza `lastUpdated` con la fecha en la que ejecutas la actualización (formato "DD de Mes, AAAA").
7. Reescribe `resumenEjecutivo` (ver siguiente sección).
8. Regenera `sparklineSvg` a partir de los últimos 6 meses de `historicalData` (ver sección "Sparkline SVG")
   — es obligatorio hacerlo cada vez que cambien esos 6 meses, o el gráfico de la home quedará desincronizado
   con las cifras que se muestran al lado. El sparkline sigue basado en el IPC nacional, no en la
   comparativa con la eurozona; no lo cambies salvo que el usuario lo pida.
9. Guarda el fichero validando que sigue siendo JSON válido (revisa comas y llaves).
10. Enseña al usuario un resumen de qué cifras han cambiado antes de dar la tarea por terminada. No hagas
    commit ni push salvo que el usuario lo pida explícitamente.

## Resumen ejecutivo

`resumenEjecutivo` es el texto que se muestra tanto en el panel completo como en el widget de la home.
Debe ser:

- 4-6 frases en español, tono neutro y periodístico (nada de recomendaciones de inversión).
- Abrir con el veredicto de la comparativa con la eurozona (en qué va mejor y en qué peor España), y
  después entrar en la lectura conjunta de los cuatro indicadores nacionales: p. ej. si la inflación
  converge con la subyacente, si el BCE ha movido tipos, cómo está la prima de riesgo y si el PIB sigue
  creciendo.
- Sin cifras inventadas: solo las que constan en `comparativaZonaEuro`/`indicators`/`historicalData` tras
  la actualización.

## Sparkline SVG

El widget de la home ya no usa Chart.js (se quitó deliberadamente para no cargar una librería de ~200 KB
por un gráfico decorativo pequeño): `sparklineSvg` es un SVG estático, autocontenido, con la evolución del
IPC general y subyacente de los últimos 6 meses de `historicalData`. La home simplemente hace
`elemento.innerHTML = dataset.sparklineSvg`, así que el SVG debe ser válido por sí solo (sin dependencias
externas) y usar comillas dobles en sus atributos (se guarda como string JSON).

No lo edites a mano: ejecuta este script (ajustando solo la ruta si hace falta) cada vez que cambien los
últimos 6 meses de `historicalData`, y copia el resultado tal cual al campo `sparklineSvg`:

```python
import json
from collections import OrderedDict

path = 'proyectos/macrodata-espana/data.json'
with open(path, encoding='utf-8') as f:
    data = json.load(f, object_pairs_hook=OrderedDict)

hist = data['historicalData'][-6:]
ipc = [h['ipc'] for h in hist]
sub = [h['ipcSubyacente'] for h in hist]

all_vals = ipc + sub
vmin, vmax = min(all_vals), max(all_vals)
rng = vmax - vmin
pad = rng * 0.15 if rng > 0 else 0.5
pmin, pmax = vmin - pad, vmax + pad
prange = pmax - pmin

x0, x1 = 12, 308
y_top, y_bottom = 10, 100
n = len(hist)
step = (x1 - x0) / (n - 1)

def xy(i, v):
    x = x0 + i * step
    y = y_bottom - ((v - pmin) / prange) * (y_bottom - y_top)
    return round(x, 1), round(y, 1)

ipc_pts = [xy(i, v) for i, v in enumerate(ipc)]
sub_pts = [xy(i, v) for i, v in enumerate(sub)]

def fmt(pts):
    return " ".join(f"{x},{y}" for x, y in pts)

ipc_line = fmt(ipc_pts)
sub_line = fmt(sub_pts)
area = f"{ipc_line} {x1},{y_bottom} {x0},{y_bottom}"

circles = "".join(
    f'<circle cx="{x}" cy="{y}" r="{2.5 if i < n-1 else 3}" fill="#e11d48"/>'
    for i, (x, y) in enumerate(ipc_pts)
)

svg = (
    '<svg viewBox="0 0 320 110" xmlns="http://www.w3.org/2000/svg" '
    'preserveAspectRatio="none" role="img" '
    'aria-label="Evolucion del IPC general y subyacente, ultimos 6 meses" '
    'style="width:100%;height:100%">'
    f'<polygon points="{area}" fill="rgba(225,29,72,0.08)"/>'
    f'<polyline points="{sub_line}" fill="none" stroke="#fb7185" stroke-width="2" '
    'stroke-dasharray="5,4" stroke-linecap="round" stroke-linejoin="round"/>'
    f'<polyline points="{ipc_line}" fill="none" stroke="#e11d48" stroke-width="2.5" '
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

Qué hace: normaliza los 6 valores de IPC general y subyacente entre el mínimo y el máximo (con un 15% de
margen visual), los reparte en 6 puntos a lo largo de un `viewBox` de 320×110, y dibuja el área bajo la
línea general (relleno rosa claro), la línea general (sólida) y la subyacente (discontinua), con puntos en
cada mes de la línea general. Los colores (`#e11d48` general, `#fb7185` subyacente) están fijados a mano
para que combinen con la leyenda estática de `index.html` (`.legend-swatch`) — si algún día cambian esos
colores en el CSS, cámbialos también aquí.

El panel completo ([proyectos/macrodata-espana/index.html](../../../proyectos/macrodata-espana/index.html))
sigue usando Chart.js con sus 4 gráficos interactivos y el selector de rango — eso no cambia, solo se quitó
Chart.js de la home.

## Notas

- Los datos publicados antes de la primera ejecución de esta skill son una muestra ilustrativa, no cifras
  reales. Indícaselo al usuario si detectas que `resumenEjecutivo` todavía contiene el aviso de "datos de
  muestra".
- No es necesario tocar `sources` salvo que cambie la metodología o la fuente de un indicador.
- Los tres indicadores de `comparativaZonaEuro` tienen calendarios de publicación distintos entre sí
  (IPCA mensual con dato preliminar rápido, PIB trimestral con más retraso, paro mensual con retraso
  intermedio): es normal que en una ejecución solo cambien uno o dos.
- Si el usuario pide explícitamente publicar los cambios, sigue el flujo normal de git (revisar diff,
  commit con mensaje descriptivo); no lo hagas por iniciativa propia.
