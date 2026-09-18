---
name: actualizar-catalogo-ayudas-espana
description: Actualiza el Catálogo de Ayudas Sociales en España con las cuantías, requisitos, estado de la convocatoria (abierta/cerrada/permanente/gestión autonómica) y enlaces oficiales de las principales ayudas y prestaciones de ámbito estatal (Ingreso Mínimo Vital, CAPI, prestaciones por desempleo, Bono Alquiler Joven, bonos sociales de energía, pensiones no contributivas, becas MEC, Bono Cultural Joven...), y su sección de Preguntas Frecuentes (FAQ, con marcado FAQPage/JSON-LD, autogenerada a partir de los datos). Usar cuando el usuario pida "actualiza el catálogo de ayudas", "revisa las cuantías del IMV", "hay una ayuda nueva que añadir" o similar.
---

# Actualizar Catálogo de Ayudas Sociales en España

Panel público con un directorio filtrable de las principales ayudas y prestaciones de ámbito **estatal**
(no autonómicas ni municipales) vigentes en España. Toda su información vive en un único fichero de
datos:

- Dataset: [proyectos/catalogo-ayudas-espana/data.json](../../../proyectos/catalogo-ayudas-espana/data.json)
- Panel completo: [proyectos/catalogo-ayudas-espana/index.html](../../../proyectos/catalogo-ayudas-espana/index.html)
- Artículo/documentación del proyecto: [publicaciones/proyecto-catalogo-ayudas-espana.md](../../../publicaciones/proyecto-catalogo-ayudas-espana.md)

No hace falta tocar el HTML ni el JavaScript: basta con editar `data.json` siguiendo el esquema de abajo.

## Esquema de `data.json`

```jsonc
{
  "lastUpdated": "DD de Mes, AAAA",
  "resumenEjecutivo": "...",             // 4-6 frases, ver sección "Resumen ejecutivo"
  "sources": { ... },                     // una entrada por ayuda o por grupo de ayudas de la misma fuente
  "categorias": [
    { "id": "rentas-minimas", "nombre": "Rentas Mínimas", "icon": "fa-...", "color": "emerald" }
    // no cambies los "id" existentes sin revisar antes que ninguna ayuda los referencie con el id antiguo;
    // los colores válidos están en CAT_COLOR_CLASSES de index.html (emerald, rose, blue, amber, yellow, violet, sky, slate)
  ],
  "ayudas": [
    {
      "id": "imv",                                    // identificador estable, no lo cambies entre actualizaciones
      "nombre": "Ingreso Mínimo Vital (IMV)",
      "categoria": "rentas-minimas",                  // debe existir en "categorias"
      "organismo": "Seguridad Social (INSS)",
      "descripcion": "1-2 frases en lenguaje llano: qué es y para quién",
      "cuantia": "...",                                // texto libre, no solo un número: incluye la unidad y si varía
      "requisitos": ["...", "..."],                    // frases completas, no palabras sueltas
      "enlaceSolicitud": "https://...",                // el portal real de solicitud, no un artículo de prensa
      "enlaceInfo": "https://...",                      // página informativa oficial (puede coincidir con enlaceSolicitud)
      "estado": "abierto" | "cerrado" | "permanente" | "regional",
      "notas": "..." | null                             // avisos importantes (contradicciones entre fuentes oficiales, gestión fragmentada por CCAA, etc.); null si no aplica
    }
  ]
}
```

### El campo `estado` (importante, es lo que más cambia con el tiempo)

- `"permanente"`: sin convocatoria ni plazo, se puede solicitar cualquier día del año (IMV, prestaciones
  por desempleo, pensiones no contributivas...).
- `"abierto"`: tiene una ventana de solicitud puntual (beca, bono con plazas limitadas) y esa ventana
  está abierta hoy. Anota la fecha de cierre en `notas` si se conoce.
- `"cerrado"`: la ventana de solicitud de este ciclo ya ha terminado. Anota en `notas` cuándo se espera
  la siguiente convocatoria si hay un patrón conocido (p. ej. "próxima convocatoria prevista en primavera
  de 2027").
- `"regional"`: el Estado regula y financia la ayuda, pero cada comunidad autónoma la tramita con su
  propia convocatoria, plazos y portal (p. ej. Bono Alquiler Joven). En estos casos `enlaceSolicitud`
  debe apuntar a la página del ministerio que enlaza al mapa de portales autonómicos, y `notas` debe
  explicitarlo — no elijas arbitrariamente el portal de una sola comunidad.

Revisa y actualiza `estado` en cada ejecución de esta skill: es el campo con más probabilidad de haber
cambiado desde la última vez (una convocatoria que estaba abierta puede haberse cerrado, o al revés).

## Pasos

1. Lee el `data.json` actual para conocer qué ayudas, cuantías y estados hay registrados.
2. Para cada ayuda, comprueba en la fuente oficial (nunca en un artículo de prensa o blog) si la cuantía,
   los requisitos o el `estado` han cambiado. Las cuantías más ligadas a revisión anual (IMV, becas,
   pensiones no contributivas, umbrales de renta) suelen actualizarse con los Presupuestos Generales del
   Estado o por real decreto a comienzos de año — comprueba siempre la fecha de la norma que sustenta la
   cifra.
3. Si detectas una ayuda nueva de ámbito estatal que no esté en el catálogo, o una que se haya derogado,
   pregunta al usuario antes de añadirla/eliminarla si tienes alguna duda sobre si de verdad es de ámbito
   estatal (y no autonómica) — el criterio de "solo ayudas estatales" es intencional, no lo relajes sin
   confirmación explícita.
4. Actualiza `lastUpdated` (formato "DD de Mes, AAAA").
5. Reescribe `resumenEjecutivo` (ver siguiente sección).
6. Guarda el fichero validando que sigue siendo JSON válido.
7. Enseña al usuario un resumen de qué ha cambiado (cuantías, estados de convocatoria, ayudas añadidas o
   eliminadas). No hagas commit ni push salvo que lo pida explícitamente.

## Resumen ejecutivo

4-6 frases en español, tono neutro. Menciona cuántas ayudas hay en el catálogo y cuántas se pueden
solicitar hoy sin plazo cerrado, destaca la cuantía del IMV como referencia, y si hay algún cambio
relevante desde la última actualización (una convocatoria que se ha abierto o cerrado, una cuantía que ha
subido) coméntalo explícitamente. Sin cifras inventadas: solo las que consten en `ayudas` tras la
actualización.

## Preguntas Frecuentes (FAQ)

El panel cierra con una sección de FAQ con marcado `FAQPage` (schema.org/JSON-LD) para SEO. **No se guarda
en `data.json`**: se genera en `index.html` (función `getFAQs()`), a partir de `ayudas` y `categorias` —
se mantiene siempre alineada con el catálogo vigente sin ningún paso manual adicional.

Solo tócala si el usuario pide explícitamente añadir, quitar o reformular alguna pregunta — en ese caso,
edita el array que construye `getFAQs()` en `index.html`, no un campo de `data.json`.

## Notas

- Este catálogo es deliberadamente **solo de ayudas estatales**. No añadas rentas mínimas de inserción
  autonómicas, ayudas de emergencia social municipales ni bonos regionales, aunque el usuario mencione una
  concreta — indícale que ese tipo de ayudas queda fuera del alcance de este panel (podría ser un proyecto
  distinto).
- Varias ayudas de vivienda (Bono Alquiler Joven, ayudas generales al alquiler) están reguladas por el
  Estado pero **gestionadas y tramitadas por cada comunidad autónoma**, con convocatorias, plazos y
  cuantías que pueden variar por región — de ahí el estado `"regional"`. No presentes un único plazo o
  cuantía nacional para estas ayudas sin la salvedad correspondiente en `notas`.
- Este catálogo no es asesoramiento legal — mantén ese aviso en el pie del panel.
- Si el usuario pide explícitamente publicar los cambios, sigue el flujo normal de git (revisar diff,
  commit con mensaje descriptivo); no lo hagas por iniciativa propia.
