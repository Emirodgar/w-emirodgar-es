---
name: actualizar-simulador-hipotecas-espana
description: Actualiza el Simulador de Hipotecas en España con los últimos datos del INE (tipo medio hipotecario, importe medio, número de hipotecas, reparto fijo/variable/mixto) y la comparativa de ofertas bancarias (TIN/TAE). Incluye calculadora de cuota y escenarios de tipos con probabilidad derivada del termómetro de riesgo de MacroData España, y su sección de Preguntas Frecuentes (FAQ, con marcado FAQPage/JSON-LD, autogenerada a partir de los datos). Usar cuando el usuario pida "actualiza el simulador de hipotecas", "actualiza los datos hipotecarios", "revisa las ofertas de los bancos" o similar.
---

# Actualizar Simulador de Hipotecas en España

Panel público con el mercado hipotecario español, una comparativa de ofertas bancarias y una
calculadora de cuota con predicción de escenarios de tipos. Toda su información propia vive en un
único fichero de datos:

- Dataset: [proyectos/simulador-hipotecas-espana/data.json](../../../proyectos/simulador-hipotecas-espana/data.json)
- Panel completo: [proyectos/simulador-hipotecas-espana/index.html](../../../proyectos/simulador-hipotecas-espana/index.html)
- Artículo/documentación del proyecto: [publicaciones/proyecto-simulador-hipotecas-espana.md](../../../publicaciones/proyecto-simulador-hipotecas-espana.md)

**Importante**: este panel NO guarda el Euríbor ni el termómetro de riesgo de recesión en su propio
`data.json` — los lee en vivo, vía `fetch('../macrodata-espana/data.json')`, del panel
[MacroData España](../../../proyectos/macrodata-espana/data.json). Si necesitas actualizar el Euríbor o
el termómetro, hazlo en MacroData España (skill `actualizar-macrodata-espana`), no aquí; este panel se
sincroniza solo.

## Esquema de `data.json`

```jsonc
{
  "lastUpdated": "DD de Mes, AAAA",
  "resumenEjecutivo": "...",              // 4-6 frases, ver sección "Resumen ejecutivo"
  "sources": { ... },
  "indicators": [
    {
      "id": "tipoMedio" | "importeMedio" | "numHipotecas" | "pctFijo",  // no cambiar los ids, no añadir/quitar entradas
      "title": "...", "currentValue": 3.05, "unit": "%" | "€" | "hipotecas/mes",
      "change": 0.05, "changeLabel": "vs mes anterior", "description": "...",
      "icon": "...", "color": "..."
    }
  ],
  "historicalData": [
    { "month": "Ago 2026", "tipoMedio": 3.05, "importeMedio": 152000, "numHipotecas": 41000, "pctFijo": 54, "pctVariable": 31, "pctMixto": 15 }
    // una entrada por mes, orden cronológico ascendente; pctFijo+pctVariable+pctMixto debe sumar ~100
  ],
  "bancos": [
    {
      "nombre": "CaixaBank", "tinFijo": 2.85, "taeFijo": 3.05, "tinVariable": 0.85,
      "taeVariableAprox": 3.4, "condiciones": "Requiere domiciliar nómina y contratar seguros de hogar y vida",
      "fuente": "URL de la web/comparador del banco", "fechaConsulta": "AAAA-MM-DD"
    }
    // 5-6 bancos principales (CaixaBank, Santander, BBVA, Sabadell, ING, Bankinter u otros relevantes)
  ],
  "calculadoraDefaults": { "importe": 150000, "plazo": 25, "diferencialVariable": 0.75 }
}
```

## Fuentes y cómo actualizarlas

1. **Indicadores del INE** (`tipoMedio`, `importeMedio`, `numHipotecas`, `pctFijo`): INE, "Estadística de
   Hipotecas" (nota de prensa mensual, busca "INE hipotecas tipo interés medio [mes] [año]"). Publica con
   ~2 meses de desfase. `pctFijo` es el porcentaje de hipotecas a tipo fijo sobre el total constituido ese
   mes; el resto (`pctVariable`/`pctMixto`) también viene desglosado en la misma nota de prensa.
2. **Comparativa de bancos** (`bancos`): las webs públicas o comparadores de cada entidad (CaixaBank,
   Santander, BBVA, Sabadell, ING, Bankinter, u otras relevantes en ese momento). Usa el TIN/TAE
   publicitado para el perfil "estándar" bonificado (con nómina y seguros, que es lo habitual en la
   publicidad) y anota en `condiciones` qué bonificaciones exige. Estas ofertas cambian con más frecuencia
   que el resto del panel — revísalas cada vez que se ejecute esta skill, no solo cuando cambien los datos
   del INE. Usa siempre WebSearch/WebFetch para verificar el dato en la fuente actual; no reutilices cifras
   de una ejecución anterior sin comprobarlas.
3. **Euríbor y termómetro de riesgo**: no se tocan aquí (ver nota de arriba). Si notas que el Euríbor
   mostrado en este panel está desactualizado, el problema está en MacroData España, no en este `data.json`.

## Pasos

1. Lee el `data.json` actual para conocer el último mes registrado y la fecha de consulta de cada banco.
2. Busca el dato más reciente publicado por el INE para los 4 indicadores; si hay un mes nuevo, añade una
   entrada a `historicalData` (o actualiza la última si seguía marcada como provisional).
3. Actualiza `indicators` con el valor más reciente de cada uno y su variación respecto al periodo
   anterior comparable.
4. Revisa la oferta pública de cada banco en `bancos` y actualiza los que hayan cambiado sus condiciones;
   actualiza siempre `fechaConsulta` aunque el tipo no haya cambiado, para dejar constancia de que se ha
   revisado.
5. Actualiza `lastUpdated` (formato "DD de Mes, AAAA").
6. Reescribe `resumenEjecutivo` (ver siguiente sección).
7. Guarda el fichero validando que sigue siendo JSON válido.
8. Enseña al usuario un resumen de qué ha cambiado. No hagas commit ni push salvo que lo pida
   explícitamente.

## Resumen ejecutivo

4-6 frases en español, tono neutro. Cubre primero el tipo medio hipotecario y su tendencia, después el
reparto fijo/variable/mixto (y si hay un cambio de tendencia relevante), y cierra con una mención al
Euríbor actual (léelo de MacroData España, no lo inventes) y, si aporta valor, una nota cualitativa sobre
el termómetro de riesgo (mismo criterio que en la skill de MacroData España: descríbelo de forma
aproximada, no cites un número exacto que no hayas recalculado tú mismo).

## Calculadora y escenarios de tipos (no requieren mantenimiento)

La cuota se calcula con la fórmula estándar de amortización francesa (`calcularCuota()` en `index.html`),
sobre los valores que introduce el usuario en el formulario — no hay nada que mantener aquí.

Los 3 escenarios ("sube 1 punto", "se mantiene", "baja 1 punto") y sus probabilidades
(`computeTipoEscenarios()`) se derivan en el momento, a partir de los componentes de crecimiento, empleo e
inflación del termómetro de riesgo de MacroData España (fetch en vivo, ver nota de arriba). Es un modelo
propio y simplificado, con pesos fijos (crecimiento 60% + empleo 40% → presión bajista; inflación → presión
alcista) y una magnitud de escenario fija (±1 punto de Euríbor). **No toques esta fórmula ni sus pesos sin
que el usuario lo pida explícitamente** — si el usuario pide ajustarla, hazlo en `computeTipoEscenarios()`
y documenta el cambio aquí.

## Preguntas Frecuentes (FAQ)

El panel cierra con una sección de FAQ con marcado `FAQPage` (schema.org/JSON-LD) para SEO. **No se guarda
en `data.json`**: se genera en `index.html` (función `getFAQs()`), a partir de `indicators`, `bancos`, el
Euríbor en vivo y las probabilidades de escenarios — se mantiene siempre alineada con las cifras vigentes
sin ningún paso manual adicional.

Solo tócala si el usuario pide explícitamente añadir, quitar o reformular alguna pregunta — en ese caso,
edita el array que construye `getFAQs()` en `index.html`, no un campo de `data.json`.

## Notas

- Este panel depende de que `proyectos/macrodata-espana/data.json` exista y tenga los campos
  `indicators` (`euribor`, `pib`, `paro`, `ipc`) — si esa estructura cambia alguna vez, revisa también
  `getEuriborActual()` y `getRiskComponentsFromMacrodata()` en este `index.html`.
- Este panel no es asesoramiento financiero ni una oferta vinculante — mantén ese aviso en el pie del
  panel y no lo elimines aunque se pida "simplificar" el texto.
- Si el usuario pide explícitamente publicar los cambios, sigue el flujo normal de git (revisar diff,
  commit con mensaje descriptivo); no lo hagas por iniciativa propia.
