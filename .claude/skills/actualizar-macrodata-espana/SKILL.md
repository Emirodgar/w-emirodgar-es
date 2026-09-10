---
name: actualizar-macrodata-espana
description: Actualiza el panel MacroData España con las últimas cifras oficiales de IPC, prima de riesgo, tipos del BCE, Euríbor y PIB. Usar cuando el usuario pida "actualiza MacroData", "actualiza el panel económico", "refresca los indicadores económicos" o similar.
---

# Actualizar MacroData España

Este proyecto es un panel público de indicadores macroeconómicos de España. Toda su información
vive en un único fichero de datos que consumen tanto el panel completo como el widget de la home:

- Dataset: [proyectos/macrodata-espana/data.json](../../../proyectos/macrodata-espana/data.json)
- Panel completo: [proyectos/macrodata-espana/index.html](../../../proyectos/macrodata-espana/index.html) (lee `data.json` vía `fetch`)
- Widget de la home: [index.html](../../../index.html) (busca `macrodataMiniChart`, también lee el mismo `data.json`)
- Artículo/documentación del proyecto: [publicaciones/proyecto-macrodata-espana.md](../../../publicaciones/proyecto-macrodata-espana.md)

No hace falta tocar el HTML ni el JavaScript de ninguna de esas páginas: basta con editar `data.json`
siguiendo el esquema descrito abajo. Todo lo demás se renderiza dinámicamente a partir de ese fichero.

## Esquema de `data.json`

```jsonc
{
  "lastUpdated": "05 de Septiembre, 2026",   // fecha en texto, formato "DD de Mes, AAAA"
  "resumenEjecutivo": "...",                  // 2-4 frases, ver sección "Resumen ejecutivo"
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

## Pasos

1. Lee el `data.json` actual para conocer el último mes registrado en `historicalData`.
2. Para cada indicador, busca el dato oficial más reciente (puede ser el mismo mes si aún no hay uno nuevo,
   o uno o varios meses posteriores si ha pasado tiempo desde la última actualización).
3. Si hay un mes nuevo que aún no está en `historicalData`, añade una entrada nueva al final del array
   (orden cronológico ascendente) con los seis valores (`ipc`, `ipcSubyacente`, `primaRiesgo`, `tiposBCE`,
   `euribor`, `pib`). Si un indicador trimestral (PIB) no tiene dato nuevo para ese mes, repite el último
   valor conocido en lugar de dejarlo vacío.
4. Actualiza el array `indicators`:
   - `currentValue`: el valor de la entrada más reciente de `historicalData` para ese indicador (para
     `prima` usa `primaRiesgo`, para `bce` usa `tiposBCE`).
   - `change`: diferencia entre el valor actual y el del periodo anterior (mismo signo que la variación
     real, sin redondear de forma distinta a los datos de origen).
5. Actualiza `lastUpdated` con la fecha en la que ejecutas la actualización (formato "DD de Mes, AAAA").
6. Reescribe `resumenEjecutivo` (ver siguiente sección).
7. Guarda el fichero validando que sigue siendo JSON válido (revisa comas y llaves).
8. Enseña al usuario un resumen de qué cifras han cambiado antes de dar la tarea por terminada. No hagas
   commit ni push salvo que el usuario lo pida explícitamente.

## Resumen ejecutivo

`resumenEjecutivo` es el texto que se muestra tanto en el panel completo como en el widget de la home.
Debe ser:

- 2-4 frases en español, tono neutro y periodístico (nada de recomendaciones de inversión).
- Centrado en la lectura conjunta de los cuatro indicadores: p. ej. si la inflación converge con la
  subyacente, si el BCE ha movido tipos, cómo está la prima de riesgo y si el PIB sigue creciendo.
- Sin cifras inventadas: solo las que constan en `indicators`/`historicalData` tras la actualización.

## Notas

- Los datos publicados antes de la primera ejecución de esta skill son una muestra ilustrativa, no cifras
  reales. Indícaselo al usuario si detectas que `resumenEjecutivo` todavía contiene el aviso de "datos de
  muestra".
- No es necesario tocar `sources` salvo que cambie la metodología o la fuente de un indicador.
- Si el usuario pide explícitamente publicar los cambios, sigue el flujo normal de git (revisar diff,
  commit con mensaje descriptivo); no lo hagas por iniciativa propia.
