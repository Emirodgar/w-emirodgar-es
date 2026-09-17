---
name: actualizar-quien-gobierna-cyl
description: Actualiza ¿Quién Gobierna CyL? con la composición vigente del Consejo de Gobierno de la Junta de Castilla y León (presidente, vicepresidencias y consejerías), sus competencias, partido, fecha de nombramiento, predecesor, ficha de Wikipedia y su sección de Preguntas Frecuentes (FAQ, con marcado FAQPage/JSON-LD, autogenerada a partir de los datos). Usar cuando el usuario pida "actualiza ¿Quién Gobierna CyL?", "actualiza el panel del Gobierno de Castilla y León", "hay un cambio de consejero/remodelación de gobierno" o similar.
---

# Actualizar ¿Quién Gobierna CyL?

Este proyecto es un panel público con la composición del Consejo de Gobierno de la Junta de Castilla y
León (presidente, vicepresidencias y consejerías), sus competencias, cuánto tiempo lleva cada uno en el
cargo y quién fue su predecesor. Toda su información vive en un único fichero de datos que consumen tanto
el panel completo como el widget de la home:

- Dataset: [proyectos/quien-gobierna-cyl/data.json](../../../proyectos/quien-gobierna-cyl/data.json)
- Panel completo: [proyectos/quien-gobierna-cyl/index.html](../../../proyectos/quien-gobierna-cyl/index.html) (lee `data.json` vía `fetch`)
- Widget de la home: [index.html](../../../index.html) (busca `quienGobiernaSparkline`, también lee el mismo `data.json`)
- Artículo/documentación del proyecto: [publicaciones/proyecto-quien-gobierna-cyl.md](../../../publicaciones/proyecto-quien-gobierna-cyl.md)

No hace falta tocar el HTML ni el JavaScript de ninguna de esas páginas: basta con editar `data.json`
siguiendo el esquema descrito abajo. Todo lo demás se renderiza dinámicamente a partir de ese fichero.

## Esquema de `data.json`

```jsonc
{
  "lastUpdated": "15 de Septiembre, 2026",
  "sparklineSvg": "<svg ...>...</svg>",   // SVG estático del widget de la home, ver sección "Sparkline SVG"
  "resumenEjecutivo": "...",              // 4-7 frases, ver sección "Resumen ejecutivo"
  "legislatura": {
    "numero": "XII", "coalicion": "PP-Vox",
    "fechaEleccion": "2026-03-15", "fechaInvestidura": "2026-06-09", "fechaFormacionGobierno": "2026-06-15",
    "escanosPP": 33, "escanosVox": 14, "totalEscanos": 81
  },
  "kpis": [
    { "id": "...", "title": "...", "value": "..." | number, "unit": "...", "detail": "...", "icon": "fa-...", "color": "..." }
    // 5 tarjetas KPI, ver sección "KPIs"
  ],
  "presidente": { /* objeto "persona", ver abajo */ },
  "vicepresidentes": [ /* 1-2 objetos "persona", con "vicepresidencia": "Primera"|"Segunda" y "competencias" */ ],
  "consejeros": [ /* resto de objetos "persona" */ ],
  "sources": { ... }
}
```

Cada objeto "persona" (presidente, vicepresidentes, consejeros) usa esta forma:

```jsonc
{
  "nombre": "Nombre completo",
  "cargo": "Consejero/a de ...",             // título completo tal cual se muestra en la ficha
  "partido": "PP" | "Vox",                    // solo estos dos valores tienen estilo propio (azul/verde); cualquier otro cae en gris
  "nacimiento": "DD de mes de AAAA, Lugar" | "AAAA, Lugar" | null,
  "enCargoDesde": "AAAA-MM-DD",                // fecha de toma de posesión en el cargo ACTUAL (aunque sea el mismo cargo de antes, tras una reinvestidura)
  "aniosEnCargo": 0,                           // años en el cargo actual concreto, redondeado hacia abajo
  "aniosEnGobierno": 0,                        // años consecutivos en el Consejo de Gobierno con independencia de la cartera (alimenta el gráfico de antigüedad)
  "estado": "Repite" | "Cara nueva en el Gobierno" | "Cambia de cartera · ..." | "Presidente desde ... ",
  "cargoAnterior": "..." | null,               // qué ocupaba justo antes, si fue dentro del propio Gobierno/instituciones autonómicas
  "competencias": ["...", "..."],              // 3-5 etiquetas cortas; los consejeros SIEMPRE lo llevan, el presidente no
  "trayectoria": "1-3 frases de biografía",
  "predecesor": {
    "nombre": "...", "partido": "...", "periodo": "AAAA-AAAA", "wikipedia": "https://..." | null
  } | null,
  "wikipedia": "https://es.wikipedia.org/wiki/..." | null   // solo si la ficha existe realmente, ver nota abajo
}
```

**Nunca inventes una URL de Wikipedia.** Antes de poner un valor en `wikipedia` (de la persona o de su
`predecesor`), comprueba que la página existe (una búsqueda o una petición a esa URL debe devolver
contenido real, no un 404). Si no hay ficha, deja `null` — el panel ya muestra "Sin ficha en Wikipedia"
en ese caso, es un estado válido y frecuente para nombramientos muy recientes.

## Cuándo y cómo comprobar cambios

A diferencia de los otros paneles de este sitio, aquí no hay una API de datos abiertos: la fuente es la
composición oficial del Gobierno más prensa. Comprueba, por este orden:

1. **Web oficial**: `https://gobierno.jcyl.es/web/es/gobierno-castilla-leon.html` — lista el presidente,
   las vicepresidencias y las consejerías vigentes. Es la fuente más fiable para saber SI ha cambiado algo
   (un cese, un nombramiento, una remodelación), aunque no siempre da fecha exacta ni partido.
2. **Wikipedia**: busca "Tercer gobierno de Alfonso Fernández Mañueco" (o el ordinal que corresponda si ya
   ha cambiado el Gobierno) y, si no existe todavía una página específica para la composición vigente, la
   página general "Junta de Castilla y León". Estas páginas suelen dar fechas exactas de toma de posesión
   y, para los cambios a mitad de legislatura, quién sustituye a quién.
3. **Prensa regional** (El Debate, El Español Castilla y León, La Gaceta de Salamanca, León Noticias,
   Ávila Red, Diario de Castilla y León, ConSalud para Sanidad, etc.) para biografías, partido de los
   nombramientos muy recientes que aún no tengan ficha de Wikipedia propia, y para confirmar el reparto de
   carteras por partido cuando cambia un pacto de coalición.

No ejecutes esta skill de forma rutinaria sin que haya indicios de cambio: a diferencia de los paneles de
datos abiertos, aquí no tiene sentido "refrescar" si no ha habido ningún nombramiento o cese nuevo desde
la última actualización. Empieza siempre comprobando la web oficial (paso 1) antes de tocar nada.

## Pasos

1. Lee el `data.json` actual para conocer la composición vigente registrada (quién ocupa cada cargo, desde
   cuándo) y compárala con la web oficial (paso 1 de arriba).
2. Si no hay cambios, no toques el fichero — dilo así al usuario y termina aquí.
3. Si hay cambios (cese, nombramiento, cambio de cartera, cambio de competencias):
   - Actualiza el objeto "persona" afectado (o añádelo/quítalo de `presidente`/`vicepresidentes`/
     `consejeros` según corresponda).
   - Si la persona que sale ya no aparece en ningún cargo, conviértela en el `predecesor` del nuevo
     titular de esa consejería (con su partido y periodo exacto), no la borres sin dejar rastro.
   - Recalcula `aniosEnCargo` y `aniosEnGobierno` de la persona afectada (y de cualquier otra si cambia su
     cartera) a partir de `enCargoDesde`, usando la fecha de esta actualización.
   - Revisa `estado` de la persona afectada ("Repite", "Cara nueva en el Gobierno", "Cambia de cartera...").
4. Recalcula los 5 `kpis` si cambia algún valor que resuman (miembros del Gobierno, reparto PP/Vox, caras
   nuevas, consejero más veterano, antigüedad del presidente).
5. Actualiza `legislatura` solo si hay elecciones nuevas o un cambio de coalición.
6. Actualiza `lastUpdated` con la fecha de ejecución (formato "DD de Mes, AAAA").
7. Reescribe `resumenEjecutivo` (ver siguiente sección).
8. Regenera `sparklineSvg` si cambia el reparto de carteras por partido (ver sección "Sparkline SVG");
   si solo cambia una persona sin alterar el reparto 9/3 (o el que corresponda), no hace falta tocarlo.
9. Guarda el fichero validando que sigue siendo JSON válido (revisa comas y llaves).
10. Enseña al usuario un resumen de qué ha cambiado (quién entra, quién sale, qué consejería y por qué
    partido). No hagas commit ni push salvo que el usuario lo pida explícitamente.

## Resumen ejecutivo

`resumenEjecutivo` es el texto que se muestra tanto en el panel completo como en el widget de la home.
Debe ser:

- 4-7 frases en español, tono neutro y periodístico, sin filiación política propia.
- Cubrir primero cuándo se formó el Gobierno vigente y su reparto por partido, después cualquier cambio
  relevante desde la última actualización (ceses, nombramientos, cambios de cartera), y por último algún
  dato de contexto llamativo (el más veterano, las caras nuevas, cambios de partido en una consejería).
- Sin cifras ni fechas inventadas: solo las que consten en `presidente`/`vicepresidentes`/`consejeros`/
  `legislatura` tras la actualización.

## KPIs

Los 5 `kpis` son tarjetas libres (no tienen un `id` fijo obligatorio como en otros paneles), pero
manteniendo estas 5 preguntas cubre bien el panel:

1. Desde cuándo es presidente el actual presidente, y cuántos años lleva.
2. Cuántas personas integran el Consejo de Gobierno en total.
3. Cómo se reparten las carteras por partido.
4. Cuántas son caras nuevas en el Gobierno (nunca habían estado antes en el Consejo de Gobierno, aunque
   ya fueran cargo público en otro sitio — p. ej. presidente de las Cortes no cuenta como "Gobierno").
5. Quién es el miembro más veterano del Gobierno (mayor `aniosEnGobierno`) y cuántos años lleva.

## Sparkline SVG

El widget de la home no usa Chart.js: `sparklineSvg` es un SVG estático y autocontenido (viewBox
`0 0 320 110`) con dos barras horizontales proporcionales al reparto de carteras por partido (incluyendo
la presidencia en el partido que corresponda) y sus etiquetas ("N PP", "N Vox"). Usa `#2563eb` para PP y
`#059669` para Vox, para que combine con `.legend-swatch--blue`/`.legend-swatch--emerald` de `styles.css`
y con `PARTY_STYLES` de `index.html` — si cambias esos colores en un sitio, cámbialos en los tres. Si
aparece un tercer partido en el Gobierno, añade una tercera barra y decide un color nuevo consistente en
los tres sitios.

## Preguntas Frecuentes (FAQ)

El panel cierra con una sección de FAQ con marcado `FAQPage` (schema.org/JSON-LD) para SEO. **No se guarda
en `data.json`**: se genera en `index.html` (función `getFAQs()`), tanto el texto visible como el JSON-LD
inyectado en `<script id="faqStructuredData">`, a partir de `presidente`, `vicepresidentes`, `kpis` y
`legislatura` — se mantiene siempre alineada con la composición vigente sin ningún paso manual adicional.
No tienes que escribir ni actualizar preguntas o respuestas: basta con mantener actualizados esos campos
(pasos de arriba) para que la FAQ quede correcta.

Solo tócala si el usuario pide explícitamente añadir, quitar o reformular alguna pregunta — en ese caso,
edita el array que construye `getFAQs()` en `index.html`, no un campo de `data.json`.

## Notas

- A diferencia de los paneles de datos abiertos de este sitio, aquí las fechas y trayectorias dependen de
  fuentes heterogéneas (prensa, Wikipedia): dos fuentes pueden discrepar en un año de nacimiento o una
  fecha exacta. Cuando eso ocurra, indícalo con cautela en `trayectoria` (p. ej. "born ~1966/1967") en vez
  de inventar una fecha única, y prioriza la fuente más oficial (Wikipedia > prensa especializada > prensa
  generalista).
- `competencias` es una síntesis propia a partir del nombre de la consejería y su cobertura de prensa, no
  un listado oficial y exhaustivo del decreto de estructura orgánica — no la presentes como tal.
- El campo `predecesor.nombre` puede incluir una aclaración entre paréntesis cuando el traspaso de
  competencias no sea limpio (p. ej. una consejería que fusiona competencias antes repartidas entre dos
  personas distintas) — es preferible eso a forzar un predecesor único y engañoso.
- Si el usuario pide explícitamente publicar los cambios, sigue el flujo normal de git (revisar diff,
  commit con mensaje descriptivo); no lo hagas por iniciativa propia.
