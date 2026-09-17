---
name: actualizar-macrodata-espana
description: Actualiza el panel MacroData España con las últimas cifras oficiales de IPC, prima de riesgo, tipos del BCE, Euríbor, tipo de la Fed, PIB, tasa de paro EPA, la comparativa España vs. eurozona (IPCA, PIB, paro armonizado), el termómetro de riesgo de recesión y la sección de Preguntas Frecuentes (FAQ, con marcado FAQPage/JSON-LD, autogenerada a partir de los datos). Usar cuando el usuario pida "actualiza MacroData", "actualiza el panel económico", "refresca los indicadores económicos" o similar.
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
      "id": "ipc" | "prima" | "bce" | "euribor" | "fed" | "pib" | "paro",  // no cambiar los ids, se usan como referencia visual Y los lee el termómetro de riesgo (ver más abajo)
      "title": "...",
      "currentValue": 2.3,                     // último valor disponible
      "unit": "%" | "pb",
      "change": -0.2,                          // variación respecto al periodo anterior (mismo signo); para "paro" es SIEMPRE variación interanual (ver sección de la Fed/paro), no intermensual
      "changeLabel": "vs mes anterior" | "Última decisión" | "Tasa interanual" | "vs hace un año (...)",
      "description": "...",
      "target": 2.0 | null,
      "icon": "...", "color": "..."            // no cambiar, son clases visuales fijas
    }
    // ... resto de indicadores, no añadir ni quitar entradas (son 7: ipc, prima, bce, euribor, fed, pib, paro)
  ],
  "historicalData": [
    { "month": "Sep 2025", "ipc": 3.5, "ipcSubyacente": 3.8, "primaRiesgo": 105, "tiposBCE": 4.25, "euribor": 4.12, "fed": 4.375, "pib": 1.8, "paro": 10.45 }
    // una entrada por mes, en orden cronológico ascendente; "fed" y "paro" son obligatorios en cada entrada igual que el resto
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
5. **Tipo de interés de la Fed** (`fed`): rango objetivo del tipo de los fondos federales (federal funds
   rate) fijado por el FOMC de la Reserva Federal de EE. UU. (federalreserve.gov, sección "Meeting
   calendars and information", o prensa financiera — busca "Fed interest rate decision [mes] [año]"). Solo
   cambia tras una reunión del FOMC (~8 al año, no mensuales); si no ha habido reunión desde la última
   actualización, mantén el valor. Como el rango es un intervalo (p. ej. "3,75%-4,00%"), usa el **punto
   medio** como `currentValue` (3,875 en ese ejemplo) y detalla el rango completo en `description`. Es un
   dato puramente informativo/comparativo: no forma parte de la política monetaria de España ni de la
   eurozona, y no entra en la fórmula del termómetro de riesgo de recesión (ver más abajo).
6. **PIB** (`pib`): INE, Contabilidad Nacional Trimestral de España (CNTR) — tasa de variación interanual
   del trimestre más reciente publicado. El PIB es trimestral: no cambia cada mes, solo cuando el INE
   publica un nuevo trimestre.
7. **Tasa de paro EPA** (`paro`): INE, Encuesta de Población Activa (EPA) — tasa de paro del trimestre más
   reciente publicado (nota de prensa trimestral en ine.es, busca "INE EPA tasa de paro [trimestre] [año]").
   Trimestral, igual que el PIB: repite el valor en los meses de un mismo trimestre. A diferencia del resto
   de indicadores, `change` aquí es la **variación interanual** (valor de este trimestre menos el mismo
   trimestre de hace un año), no la variación intertrimestral — así lo usa directamente el termómetro de
   riesgo de recesión como proxy del momentum del mercado laboral. Pon en `changeLabel` el trimestre de
   comparación exacto, p. ej. `"vs hace un año (2T25: 10,29%)"`. Distinta metodológicamente de la tasa de
   paro armonizada de Eurostat que ya usa `comparativaZonaEuro.paro` — no las confundas ni intentes
   "cuadrarlas": son dos fuentes y metodologías distintas conviviendo a propósito en el mismo panel.

Usa WebSearch/WebFetch para localizar la cifra en la fuente oficial. Si una fuente no tiene el dato del
periodo más reciente (p. ej. el INE aún no ha publicado el mes en curso, o la EPA del trimestre en curso
todavía no ha salido), usa el último dato disponible (repitiéndolo en los meses del trimestre que aún no
tiene cifra nueva, igual que ya se hace con el PIB) y no inventes cifras.

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
   (orden cronológico ascendente) con los ocho valores (`ipc`, `ipcSubyacente`, `primaRiesgo`, `tiposBCE`,
   `euribor`, `fed`, `pib`, `paro`). Si un indicador trimestral (PIB, paro) no tiene dato nuevo para ese
   mes, repite el último valor conocido en lugar de dejarlo vacío; lo mismo para `fed` si no ha habido
   reunión del FOMC ese mes.
4. Actualiza el array `indicators`:
   - `currentValue`: el valor de la entrada más reciente de `historicalData` para ese indicador (para
     `prima` usa `primaRiesgo`, para `bce` usa `tiposBCE`; para `fed` usa el punto medio del rango vigente,
     que puede ser posterior al último mes de `historicalData` si acaba de haber una reunión del FOMC, igual
     que ya pasa con `bce` y el BCE).
   - `change`: diferencia entre el valor actual y el del periodo anterior (mismo signo que la variación
     real, sin redondear de forma distinta a los datos de origen) — **excepto `paro`**, donde `change` es
     la variación interanual (ver punto 7 de la sección anterior), no intermensual/intertrimestral.
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

- 5-8 frases en español, tono neutro y periodístico (nada de recomendaciones de inversión).
- Abrir con el veredicto de la comparativa con la eurozona (en qué va mejor y en qué peor España), y
  después entrar en la lectura conjunta de los indicadores nacionales: si la inflación converge con la
  subyacente, si el BCE ha movido tipos, cómo está la prima de riesgo, el Euríbor, si el PIB sigue
  creciendo y cómo evoluciona la tasa de paro EPA (interanual). Menciona el movimiento de la Fed solo
  cuando haya novedad (cambio de tipos) o aporte contraste relevante con el BCE.
- Cerrar con una frase cualitativa sobre la lectura del termómetro de riesgo de recesión (nivel/banda y,
  si aporta valor, cuál es hoy el principal factor de riesgo de los cuatro) — ver la sección de arriba
  sobre cómo citarlo sin inventar el número exacto.
- Sin cifras inventadas: solo las que constan en `comparativaZonaEuro`/`indicators`/`historicalData` tras
  la actualización.

## Termómetro de riesgo de recesión

El panel muestra un termómetro visual (0-100) que **no se guarda en `data.json`**: se recalcula en cada
carga de la página, en `index.html`, a partir de cinco valores del array `indicators` (`pib.currentValue`,
`paro.change`, `ipc.currentValue`, `prima.currentValue`, `bce.currentValue`). Es un índice propio de este
proyecto, no de ninguna institución oficial — no representa la posición de ningún banco central ni
organismo. Su fórmula (función `computeRecessionRisk()` en `index.html`) es:

- **Crecimiento — 35%**: PIB interanual ≥2,5% → 0 riesgo; ≤-1% → 100 riesgo (interpolación lineal).
- **Empleo — 25%**: variación interanual del paro ≤0 (estable o baja) → 0 riesgo; ≥+2 puntos → 100 riesgo.
- **Inflación — 15%**: distancia absoluta del IPC al objetivo del 2% del BCE; ≤0,5 puntos → 0 riesgo;
  ≥4,5 puntos → 100 riesgo (penaliza tanto inflación alta como deflación).
- **Condiciones financieras — 25%**: media de dos sub-riesgos, tipo del BCE (0%→0 riesgo, 5%→100 riesgo) y
  prima de riesgo (0pb→0 riesgo, 300pb→100 riesgo).

**No toques esta fórmula ni sus umbrales sin que el usuario lo pida explícitamente** — están documentados
también en `sources.riesgoRecesion`, que sí debes mantener sincronizado si algún día cambian los pesos o
los umbrales. Como se recalcula solo a partir de `indicators`, basta con mantener esos cinco campos
actualizados (pasos 2-4 de arriba) para que el termómetro quede correcto automáticamente; no hay ningún
campo adicional que rellenar a mano. Si mencionas su lectura en `resumenEjecutivo`, indícalo de forma
aproximada y cualitativa (p. ej. "el termómetro marca un nivel bajo, en torno a X puntos sobre 100") en
vez de citar el número exacto, ya que tú no ejecutas el JavaScript del panel y no puedes calcular el
resultado exacto sin reproducir la fórmula a mano — si quieres citarlo con precisión, reprodúcela con los
valores nuevos de `indicators` antes de escribir la cifra.

## Preguntas Frecuentes (FAQ)

El panel cierra con una sección de FAQ con marcado `FAQPage` (schema.org/JSON-LD) para SEO. **Tampoco se
guarda en `data.json`**: se genera en `index.html` (función `getFAQs()`), tanto el texto visible como el
JSON-LD inyectado en `<script id="faqStructuredData">`, a partir de `indicators`, `comparativaZonaEuro` y
`computeRecessionRisk()` — igual que el termómetro, se mantiene siempre alineada con las cifras vigentes
sin ningún paso manual adicional. No tienes que escribir ni actualizar preguntas o respuestas: basta con
mantener actualizados `indicators`/`comparativaZonaEuro` (pasos de arriba) para que la FAQ quede correcta.

Solo tócala si el usuario pide explícitamente añadir, quitar o reformular alguna pregunta — en ese caso,
edita el array que construye `getFAQs()` en `index.html`, no un campo de `data.json`. Si añades una
pregunta con datos dinámicos, interpólalos con `formatNumber()` igual que las demás, para mantener el
formato de miles/decimales en español consistente con el resto del panel.

Este mismo patrón (FAQ generada en JS + FAQPage/JSON-LD) se repite, con preguntas propias de cada dominio,
en los otros tres paneles del sitio (Panel Económico CyL, Radar de Empleo Público CyL, ¿Quién Gobierna
CyL?) — si el usuario pide ampliar/corregir las FAQ "en todos los paneles", repite el cambio en los
`getFAQs()` de los cuatro `index.html`, no solo en el de MacroData España.

## Gráfico de evolución del termómetro

Debajo del termómetro, el panel muestra un gráfico de línea con la puntuación de riesgo de los últimos 6
meses (`riesgoHistoricoChart`, función `computeHistoricalRiskSeries()` en `index.html`). Tampoco se guarda
en `data.json`: se recalcula mes a mes a partir de `historicalData`, con la misma fórmula y los mismos
pesos que `computeRecessionRisk()` — la única diferencia es el componente de empleo, que aquí compara
contra el último valor de `paro` distinto disponible en la propia serie (variación intertrimestral),
porque solo se almacenan ~12 meses de histórico y no siempre hay un dato de "hace un año" disponible. Por
esto mismo, el último punto del gráfico puede diferir ligeramente del número mostrado en el termómetro de
arriba (que usa `indicators.bce`/`indicators.fed`, a veces más recientes que la última fila de
`historicalData`) — es un comportamiento esperado y ya documentado en el propio panel, no lo "corrijas"
forzando que coincidan. No requiere ningún paso de mantenimiento adicional: basta con mantener
`historicalData` actualizado (pasos de arriba).

## Termómetro de riesgo de recesión también en la home

La fórmula de `computeRecessionRisk()` está **duplicada intencionadamente** en dos sitios: en
`proyectos/macrodata-espana/index.html` (el panel) y en el `index.html` de la raíz del sitio (sección
`#riesgo-recesion` de la home, que lee el mismo `proyectos/macrodata-espana/data.json` vía `fetch` para
mostrar el mismo termómetro con un botón "Ver análisis de parámetros económicos" enlazando al panel). No
hay forma de compartir código JS entre ambos ficheros en este sitio estático, así que **si algún día
cambian los pesos o los umbrales de la fórmula, hay que actualizarlos en los dos sitios** (busca
`riskLerp`/`RISK_BANDS`/`computeRecessionRisk` en ambos `index.html`). Como de costumbre, no toques esta
fórmula sin que el usuario lo pida explícitamente.

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
- El FOMC de la Fed y el Consejo de Gobierno del BCE tienen calendarios de reuniones distintos y no
  sincronizados: es normal que en una misma actualización cambie uno de los dos tipos oficiales (`bce`,
  `fed`) y el otro no.
- `paro` (EPA nacional) y `comparativaZonaEuro.paro` (armonizada de Eurostat) son series distintas a
  propósito: no fuerces que coincidan ni elimines una de las dos.
- Si el usuario pide explícitamente publicar los cambios, sigue el flujo normal de git (revisar diff,
  commit con mensaje descriptivo); no lo hagas por iniciativa propia.
