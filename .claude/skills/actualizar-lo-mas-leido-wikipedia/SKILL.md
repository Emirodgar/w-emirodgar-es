---
name: actualizar-lo-mas-leido-wikipedia
description: Actualiza el panel "Lo Más Leído en Wikipedia" con el Top 25 Report semanal de la Wikipedia en inglés (los 25 artículos más visitados), traducido, resumido y clasificado por categoría temática en español, junto con el histórico semanal y su sección de Preguntas Frecuentes (FAQ, con marcado FAQPage/JSON-LD, autogenerada a partir de los datos). Usar cuando el usuario pida "actualiza Lo Más Leído en Wikipedia", "actualiza el Top 25 de Wikipedia", "hay un nuevo informe semanal de Wikipedia que resumir" o similar, y también en la ejecución programada semanal de este proyecto.
---

# Actualizar Lo Más Leído en Wikipedia

Este proyecto es un panel público que resume en español, cada semana, el [Top 25 Report](https://en.wikipedia.org/wiki/Wikipedia:Top_25_Report)
de la Wikipedia en inglés: los 25 artículos más visitados de la semana, con sus visitas, una
clasificación temática propia y un resumen en español de por qué cada uno generó interés. Toda su
información vive en un único fichero de datos que consumen tanto el panel completo como el widget de la
home:

- Dataset: [proyectos/lo-mas-leido-wikipedia/data.json](../../../proyectos/lo-mas-leido-wikipedia/data.json)
- Panel completo: [proyectos/lo-mas-leido-wikipedia/index.html](../../../proyectos/lo-mas-leido-wikipedia/index.html) (lee `data.json` vía `fetch`)
- Widget de la home: [index.html](../../../index.html) (busca `wikipediaTopSparkline`, también lee el mismo `data.json`)
- Artículo/documentación del proyecto: [publicaciones/proyecto-lo-mas-leido-wikipedia.md](../../../publicaciones/proyecto-lo-mas-leido-wikipedia.md)

No hace falta tocar el HTML ni el JavaScript de ninguna de esas páginas: basta con editar `data.json`
siguiendo el esquema descrito abajo. Todo lo demás (tablas, gráficos, KPIs, FAQ) se renderiza
dinámicamente a partir de ese fichero.

## Fuente de datos: Top 25 Report

La página del informe se edita en el mismo sitio cada semana (no hay una URL nueva por semana): siempre
muestra la edición más reciente disponible.

```
https://en.wikipedia.org/w/index.php?title=Wikipedia:Top_25_Report&useparsoid=0
```

Usa siempre esa URL con `useparsoid=0` (renderizado wikitext clásico, más estable para extraer la tabla
que el renderizado Parsoid por defecto). Antes de nada, comprueba el título de la sección
"Most Popular Wikipedia Articles of the Week (Mes Día to Día, Año)" para saber qué semana cubre el
informe, y compáralo con `semanaAnalizada.etiqueta` del `data.json` actual:

- Si la semana del informe es **la misma** que ya está en `data.json`, no hay nada nuevo que actualizar:
  avisa al usuario de que el informe todavía no se ha renovado (normalmente se publica los domingos) y no
  toques el fichero.
- Si es una semana **posterior**, sigue con los pasos de abajo.

## Esquema de `data.json`

```jsonc
{
  "lastUpdated": "21 de Septiembre, 2026",           // fecha de ESTA actualización (ejecución de la skill)
  "semanaAnalizada": {
    "etiqueta": "6-12 de septiembre de 2026",         // tal y como aparece en el título del informe, traducido
    "inicio": "2026-09-06", "fin": "2026-09-12"
  },
  "resumenEjecutivo": "...",                          // 5-7 frases, ver sección "Resumen ejecutivo"
  "sparklineSvg": "<svg ...>...</svg>",               // SVG estático del widget de la home, ver sección "Sparkline SVG"
  "sources": { ... },                                 // no cambia salvo que cambie la metodología
  "indicators": [
    {
      "id": "articuloTop" | "totalVisitas" | "categoriaDominante" | "diversidadTematica", // no cambiar los ids
      "title": "...", "currentValue": 1901020, "unit": "visitas" | "de 25 artículos" | "categorías",
      "change": null, "changeLabel": "...", "description": "...", "target": null,
      "icon": "...", "color": "..."
    }
  ],
  "topArticulos": [
    {
      "rank": 1, "titulo": "Killing of the Clancy children",         // título EXACTO del artículo en inglés (para el enlace)
      "categoria": "Sucesos y Justicia",                             // una de las 7 categorías fijas, ver sección siguiente
      "visitas": 1901020,
      "enlace": "https://en.wikipedia.org/wiki/Killing_of_the_Clancy_children",
      "resumen": "..."                                               // 1-2 frases en español, redacción PROPIA (ver sección "Resúmenes")
    }
    // exactamente 25 filas, rank 1-25 en orden de visitas descendente
  ],
  "categorias": [
    { "categoria": "Cine y TV", "articulos": 11, "visitas": 6661339 }
    // una fila por cada categoría presente esa semana, recalculada desde topArticulos, orden descendente por visitas
  ],
  "historicoSemanal": [
    { "semana": "6-12 de septiembre de 2026", "articuloTop": "Killing of the Clancy children", "visitasArticuloTop": 1901020, "visitasTotalesTop25": 19267433, "categoriaDominante": "Cine y TV" }
    // una entrada por semana, en orden cronológico ascendente; máximo 12 entradas (ver "Pasos")
  ],
  "notas": { ... }
}
```

## 1. Extraer el ranking de la semana

Lee la tabla `Rank | Article | Class | Views | Image | Notes/about` de la página del informe. Para cada
una de las 25 filas necesitas: `rank`, el título exacto del artículo (para reconstruir su URL en
`https://en.wikipedia.org/wiki/<Título_con_guiones_bajos>`, respetando mayúsculas/minúsculas y caracteres
especiales codificados igual que en el enlace original de la tabla), y `views` (quita las comas de miles
al guardarlo como número).

No copies la columna "Notes/about" tal cual: solo úsala como fuente de hechos para redactar tu propio
resumen en español (ver sección "Resúmenes en español"). Ignora la columna "Class" (es la valoración de
calidad del artículo dentro de Wikipedia, no aporta nada a este panel) y la columna "Image" (no se
incrustan imágenes en este panel, para evitar problemas de licencias).

## 2. Clasificar cada artículo por categoría temática

El Top 25 Report no clasifica los artículos por tema: la clasificación es propia de este panel. Usa
siempre una de estas 7 categorías fijas (no crees una categoría nueva sin decírselo antes al usuario):

1. **Deportes**: cualquier evento, competición o deportista (tenis, fútbol, JJOO, etc.)
2. **Cine y TV**: películas, series, documentales, personas cuya relevancia de la semana viene de un
   estreno, y biografiados cuya popularidad resurge por una adaptación (p. ej. un gurú histórico que
   vuelve a las visitas por una película biográfica sobre él)
3. **Sucesos y Justicia**: crímenes, juicios, investigaciones, fraudes, condenas
4. **Historia y Sociedad**: aniversarios, conmemoraciones, hechos históricos y sus derivados (fotografías
   icónicas, vuelos, lugares) que generan visitas por una fecha señalada
5. **Política**: elecciones, partidos, políticos, instituciones, medidas de gobierno
6. **Fallecimientos**: artículos que agregan o resumen fallecimientos (p. ej. "Deaths in <año>"),
   distintos de un fallecimiento concreto que encaje mejor en otra categoría (p. ej. un futbolista
   fallecido va en Deportes si el motivo de sus visitas es su carrera, no su muerte)
7. **Internet y Cultura Digital**: sitios web, plataformas, fenómenos de internet, IA, tecnología no
   encuadrada en otra categoría

Si un artículo encaja en más de una, elige la categoría que mejor explique **por qué esa semana concreta**
está generando visitas (el motivo que da el propio informe), no un encuadre genérico del tema.

## 3. Redactar los resúmenes en español

**No traduzcas literalmente** el texto de la columna "Notes/about": redacta tu propio resumen en español,
en 1-2 frases, a partir de los hechos que menciona (qué ha pasado, por qué es noticia, cualquier cifra
relevante). Esto es tanto una cuestión de estilo (coherencia con el resto del panel) como de derechos de
autor: el comentario original es una obra con su propio estilo editorial y no debe reproducirse ni
parafrasearse frase a frase. Puedes usar cifras y hechos concretos (nombres, fechas, resultados), pero la
redacción y estructura de la frase deben ser tuyas.

Si el contenido de la columna "Notes/about" no basta para entender por qué el artículo es tendencia (es
poco frecuente, pero ocurre con artículos "de referencia" como "Deaths in <año>"), un resumen genérico y
honesto basta (ver el ejemplo ya usado para "Deaths in 2026" en el `data.json` actual).

## 4. Recalcular `categorias`, indicadores e histórico

1. Agrupa `topArticulos` por `categoria` y suma `articulos` (recuento) y `visitas` para cada una; ordena
   el array `categorias` de mayor a menor `visitas`.
2. Indicador `articuloTop`: el artículo de `rank: 1` (`title` = `"Artículo Más Leído: <título>"`,
   `currentValue` = sus visitas, `description` = una frase breve sobre el motivo).
3. Indicador `totalVisitas`: suma de `visitas` de las 25 filas.
4. Indicador `categoriaDominante`: la categoría con más `articulos` en `categorias` (a igualdad, la de más
   `visitas`); `title` = `"Categoría Dominante: <categoría>"`, `currentValue` = su nº de artículos,
   `changeLabel` = `"<visitas de esa categoría> visitas conjuntas (<porcentaje>% del Top 25)"`.
5. Indicador `diversidadTematica`: nº de categorías distintas presentes esa semana (`currentValue`),
   `description` listando esas categorías separadas por comas.
6. Si ya hay al menos una semana previa en `historicoSemanal`, calcula `change` de `totalVisitas` frente a
   la semana anterior (`visitasTotalesTop25` de la última entrada antes de añadir la nueva) y actualiza su
   `changeLabel` a algo como `"vs semana anterior (X visitas)"`. Si es la primera comparación disponible,
   dilo explícitamente en `changeLabel` en vez de dejarlo genérico.
7. Añade una fila nueva a `historicoSemanal` con los datos de esta semana. Si el array ya tiene 12
   entradas, elimina la más antigua (la primera) antes de añadir la nueva, para no crecer sin límite.

## 5. Actualizar cabecera y resumen ejecutivo

1. `lastUpdated`: fecha de ejecución de la skill (formato "DD de Mes, AAAA"), no la fecha del informe.
2. `semanaAnalizada`: la semana que cubre el informe (etiqueta en español + fechas ISO de inicio y fin).
3. `resumenEjecutivo`: 5-7 frases en español, tono neutro y periodístico, redacción propia. Cubre en este
   orden: (a) el artículo más leído y los siguientes 2-3 puestos más destacados, con sus visitas; (b) el
   total de visitas del Top 25 y la categoría dominante, con su peso relativo; (c) uno o dos patrones
   temáticos relevantes de la semana (p. ej. un evento deportivo, una serie de estrenos, una efeméride);
   (d) si hay al menos dos semanas en `historicoSemanal`, una frase comparando esta semana con la anterior
   (visitas totales al alza o a la baja, cambio de categoría dominante, etc.); si es la primera semana
   registrada, dilo explícitamente en vez de inventar una comparación. Sin cifras inventadas: solo las que
   consten en `indicators`/`topArticulos`/`categorias` tras la actualización.

## 6. Sparkline SVG

El widget de la home no usa Chart.js: `sparklineSvg` es un SVG estático y autocontenido con las 5 barras
horizontales de los artículos con más visitas de la semana (no una serie temporal, ya que los artículos
cambian cada semana). Usa este script cada vez que cambie `topArticulos`, y copia el resultado tal cual al
campo `sparklineSvg`:

```python
import json

path = 'proyectos/lo-mas-leido-wikipedia/data.json'
with open(path, encoding='utf-8') as f:
    data = json.load(f)

top5 = sorted(data['topArticulos'], key=lambda a: -a['visitas'])[:5]
maxv = top5[0]['visitas']
x0, x1 = 118, 308
rows_y = [14, 34, 54, 74, 94]

def short_label(i, titulo):
    # Ajusta a mano si el título en inglés no cabe o conviene una etiqueta más clara en español;
    # como mínimo, antepone el puesto en el ranking.
    t = titulo if len(titulo) <= 22 else titulo[:21] + "…"
    return f"{i+1}. {t}"

parts = []
for i, (art, y) in enumerate(zip(top5, rows_y)):
    w = round((art['visitas'] / maxv) * (x1 - x0), 1)
    label = short_label(i, art['titulo'])
    parts.append(f'<text x="0" y="{y+4}" font-family="Inter, sans-serif" font-size="9" fill="#475569">{label}</text>')
    parts.append(f'<rect x="{x0}" y="{y-6}" width="{max(w,2)}" height="12" rx="3" fill="#4338ca"/>')

svg = (
    '<svg viewBox="0 0 320 110" xmlns="http://www.w3.org/2000/svg" '
    'role="img" aria-label="Los 5 articulos mas leidos de Wikipedia esta semana" '
    'style="width:100%;height:100%">'
    + "".join(parts) +
    '</svg>'
)

data['sparklineSvg'] = svg
with open(path, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write('\n')
```

El color (`#4338ca`, índigo) está fijado a mano para que combine con `.legend-swatch--violet` en
`styles.css` — si cambia ese color, cámbialo también aquí. Revisa las etiquetas generadas por
`short_label`: si un título en inglés queda confuso o demasiado técnico para la home, sustitúyelo a mano
por una etiqueta corta en español antes de guardar (como se hizo con "1. Caso Clancy" o
"5. Fallecidos en 2026" en la primera versión).

## Pasos

1. Lee el `data.json` actual para saber qué semana está registrada (`semanaAnalizada.etiqueta`) y cuántas
   entradas hay ya en `historicoSemanal`.
2. Carga `https://en.wikipedia.org/w/index.php?title=Wikipedia:Top_25_Report&useparsoid=0` y comprueba la
   semana del informe. Si coincide con la ya registrada, avisa al usuario y termina sin tocar el fichero.
3. Extrae las 25 filas (rank, título, enlace, visitas) — paso 1.
4. Clasifica cada artículo en una de las 7 categorías — paso 2.
5. Redacta el resumen en español de cada uno de los 25 artículos — paso 3.
6. Recalcula `categorias`, los 4 indicadores y añade la nueva fila a `historicoSemanal` (retirando la más
   antigua si ya hay 12) — paso 4.
7. Actualiza `lastUpdated`, `semanaAnalizada` y reescribe `resumenEjecutivo` — paso 5.
8. Regenera `sparklineSvg` con el script de la sección 6 — obligatorio cada vez que cambie `topArticulos`.
9. Actualiza `notas` si procede (por ejemplo, retira `notas.primeraSemana` en cuanto haya una segunda
   semana registrada, y sustitúyela si hace falta por alguna aclaración nueva).
10. Guarda el fichero validando que sigue siendo JSON válido (revisa comas y llaves; ejecutar
    `python -c "import json; json.load(open('proyectos/lo-mas-leido-wikipedia/data.json', encoding='utf-8'))"`
    es una forma rápida de comprobarlo).
11. Enseña al usuario un resumen de la semana (artículo más leído, categoría dominante, y cualquier cambio
    relevante frente a la semana anterior si ya hay histórico). No hagas commit ni push salvo que el
    usuario lo pida explícitamente.

## Preguntas Frecuentes (FAQ)

El panel cierra con una sección de FAQ con marcado `FAQPage` (schema.org/JSON-LD) para SEO. **No se guarda
en `data.json`**: se genera en `index.html` (función `getFAQs()`), tanto el texto visible como el JSON-LD
inyectado en `<script id="faqStructuredData">`, a partir de `semanaAnalizada`, `topArticulos` y
`categorias` — se mantiene siempre alineada con las cifras vigentes sin ningún paso manual adicional. No
tienes que escribir ni actualizar preguntas o respuestas: basta con mantener actualizados esos campos
(pasos de arriba) para que la FAQ quede correcta.

Solo tócala si el usuario pide explícitamente añadir, quitar o reformular alguna pregunta — en ese caso,
edita la función `getFAQs()` en `index.html`, no un campo de `data.json`.

## Notas

- Esta skill está pensada para ejecutarse tanto manualmente ("actualiza Lo Más Leído en Wikipedia") como
  desde una tarea programada semanal (ver la tarea creada con la skill `schedule` de Claude Code). En
  ambos casos, los pasos son los mismos.
- El Top 25 Report se publica habitualmente los domingos con los datos de la semana que acaba de
  terminar; no fuerces una actualización si la semana del informe no ha cambiado desde la última vez.
- No incrustes imágenes de los artículos: la columna "Image" del informe original no se usa en este panel,
  para evitar problemas de licencias de las imágenes de cada artículo.
- La clasificación por categoría y los resúmenes en español son interpretación y redacción propias, no
  contenido oficial de Wikipedia ni una traducción certificada — mantén esa aclaración en el panel
  (`sources`) y en la documentación del proyecto aunque cambien los datos semana a semana.
- Si el usuario pide explícitamente publicar los cambios, sigue el flujo normal de git (revisar diff,
  commit con mensaje descriptivo); no lo hagas por iniciativa propia.
