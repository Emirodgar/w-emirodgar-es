---
name: actualizar-catalogo-ayudas-cyl-salamanca
description: Actualiza el catálogo "Ayudas de Castilla y León y Salamanca" con las cuantías, requisitos, estado de la convocatoria y enlaces oficiales de las ayudas autonómicas de la Junta de Castilla y León y de las ayudas municipales/provinciales del Ayuntamiento de Salamanca y la Diputación de Salamanca (Renta Garantizada de Ciudadanía, Bono Nacimiento, ayudas de comedor y transporte escolar, dependencia, urgencia social, vivienda, Bono Bus...), su calculadora de elegibilidad y su sección de Preguntas Frecuentes. Usar cuando el usuario pida "actualiza el catálogo de ayudas de Castilla y León", "revisa la Renta Garantizada de Ciudadanía", "hay una ayuda nueva de Salamanca que añadir" o similar.
---

# Actualizar Ayudas de Castilla y León y Salamanca

Panel público con un directorio filtrable de ayudas de **ámbito autonómico** (Junta de Castilla y León) y de **ámbito municipal o provincial de Salamanca** (Ayuntamiento de Salamanca y Diputación de Salamanca). No incluye ayudas de ámbito estatal (esas viven en el proyecto separado `catalogo-ayudas-espana`) ni ayudas de otros ayuntamientos de la provincia distintos de la capital.

- Dataset: [proyectos/catalogo-ayudas-cyl-salamanca/data.json](../../../proyectos/catalogo-ayudas-cyl-salamanca/data.json)
- Panel completo: [proyectos/catalogo-ayudas-cyl-salamanca/index.html](../../../proyectos/catalogo-ayudas-cyl-salamanca/index.html)
- Artículo/documentación del proyecto: [publicaciones/proyecto-catalogo-ayudas-cyl-salamanca.md](../../../publicaciones/proyecto-catalogo-ayudas-cyl-salamanca.md)

## Esquema de `data.json`

Igual que en `catalogo-ayudas-espana`, con un campo adicional obligatorio: `"ambito"`.

```jsonc
{
  "lastUpdated": "DD de Mes, AAAA",
  "resumenEjecutivo": "...",
  "sources": { ... },
  "categorias": [
    { "id": "rentas-minimas", "nombre": "Rentas Mínimas y Emergencia Social", "icon": "fa-...", "color": "emerald" }
    // colores válidos: los de CAT_COLOR_CLASSES en index.html (emerald, rose, blue, amber, yellow, violet, sky, slate)
  ],
  "ayudas": [
    {
      "id": "rgc",                                     // estable, no lo cambies entre actualizaciones
      "nombre": "Renta Garantizada de Ciudadanía (RGC)",
      "categoria": "rentas-minimas",                   // debe existir en "categorias"
      "organismo": "Gerencia de Servicios Sociales de Castilla y León",
      "descripcion": "1-2 frases en lenguaje llano",
      "cuantia": "...",                                 // texto libre con unidad, no solo un número
      "requisitos": ["...", "..."],
      "enlaceSolicitud": "https://...",                 // portal oficial real, no un artículo de prensa
      "enlaceInfo": "https://...",
      "estado": "abierto" | "cerrado" | "permanente" | "automatico",
      "ambito": "autonomico" | "municipal" | "provincial",   // ver más abajo, es el campo distintivo de este panel
      "notas": "..." | null
    }
  ]
}
```

### El campo `ambito` (específico de este panel)

- `"autonomico"`: la regula y paga la Junta de Castilla y León. Disponible para cualquier residente de la
  comunidad, no solo de Salamanca.
- `"municipal"`: la gestiona el Ayuntamiento de Salamanca. **Solo aplica a residentes de la ciudad de
  Salamanca**, no del resto de la provincia.
- `"provincial"`: la gestiona la Diputación de Salamanca, dirigida a los municipios de la provincia
  **distintos de la capital** (la Diputación no presta estos servicios dentro de la propia ciudad de
  Salamanca, que tiene su propio ayuntamiento).

Este campo lo usa tanto el badge visual de cada ficha (`AMBITO_BADGE` en `index.html`) como el filtro de
ámbito del panel y la calculadora de elegibilidad (`evaluarElegibilidad()`, que descarta automáticamente
una ayuda "municipal" si el perfil no reside en la capital, y una "provincial" si no reside en la
provincia fuera de la capital). No añadas una ayuda sin este campo.

### El campo `estado`

Igual que en `catalogo-ayudas-espana`: `"permanente"` (sin plazo), `"abierto"` (convocatoria puntual
abierta ahora), `"cerrado"` (convocatoria puntual ya cerrada, anota en `notas` cuándo se espera la
siguiente si se conoce el patrón), `"automatico"` (concesión de oficio, sin solicitud). Este panel no usa
el valor `"regional"` de `catalogo-ayudas-espana` porque el campo `ambito` ya cubre esa distinción.

## Calculadora de elegibilidad (al principio del panel)

Igual que en `catalogo-ayudas-espana`, con un campo adicional: `perfilResidencia` (dónde vive la persona:
capital, provincia fuera de la capital, otro municipio de CyL, o fuera de CyL), que junto con el campo
`ambito` de cada ayuda determina automáticamente en `evaluarElegibilidad()` si esa ayuda puede aplicar,
antes de comprobar ninguna otra regla.

Las reglas específicas por ayuda viven en el objeto `ELEGIBILIDAD` de `index.html` (una función por
`id`). Varias ayudas de dependencia y mayores (`pecef-dependencia-cyl`, `sad-diputacion`,
`teleasistencia-diputacion`) **no tienen regla propia a propósito**: no hay ningún dato fiable en el
formulario para aproximar el grado de dependencia real, así que se dejan sin filtrar (se muestran
siempre, sujetas solo al filtro de ámbito/residencia) en vez de arriesgarse a ocultarlas por error.

Si añades una ayuda nueva a `data.json`, considera si añadir también su regla en `ELEGIBILIDAD` — si no lo
haces, la ayuda se mostrará siempre que se aplique el filtro (comportamiento seguro por defecto, pero
menos útil). Si cambias un umbral oficial (RGC, urgencia social...), actualiza también la fórmula
correspondiente en `index.html` (`rgcThreshold`, `urgenciaSocialThreshold`).

## Pasos

1. Lee el `data.json` actual para conocer qué ayudas, cuantías, estados y ámbitos hay registrados.
2. Para cada ayuda, comprueba en la fuente oficial (nunca en un artículo de prensa o blog, salvo que sea la
   única fuente disponible y quede explícitamente anotado en `notas`) si la cuantía, los requisitos o el
   `estado` han cambiado.
3. Presta especial atención a las cifras marcadas como no confirmadas en fuente primaria en `notas` (varias
   ayudas de dependencia, urgencia social y servicios a domicilio de la Diputación no publican importes en
   euros en su web oficial): si encuentras la cifra exacta en una fuente primaria, actualízala y elimina la
   advertencia; si sigues sin encontrarla, mantén la advertencia.
4. Si detectas una ayuda nueva de la Junta de Castilla y León, del Ayuntamiento de Salamanca o de la
   Diputación de Salamanca que no esté en el catálogo, o una que se haya derogado, confirma con el usuario
   si tienes alguna duda sobre el ámbito exacto (autonómico/municipal/provincial) — no lo asumas.
5. Actualiza `lastUpdated` y reescribe `resumenEjecutivo`.
6. Guarda el fichero validando que sigue siendo JSON válido.
7. Enseña al usuario un resumen de qué ha cambiado. No hagas commit ni push salvo que lo pida explícitamente.

## Preguntas Frecuentes (FAQ)

Igual que en `catalogo-ayudas-espana`: se generan en `index.html` (función `getFAQs()`), no en
`data.json`. Solo tócala si el usuario pide explícitamente añadir, quitar o reformular alguna pregunta.

## Notas

- Este catálogo es deliberadamente de ámbito **autonómico (Castilla y León) y municipal/provincial de
  Salamanca únicamente**. No añadas ayudas estatales (van en `catalogo-ayudas-espana`) ni ayudas de otros
  ayuntamientos de la provincia distintos de la capital (esas dependen de la Diputación y ya están
  cubiertas por el ámbito `"provincial"`; no se listan ayudas pueblo por pueblo).
- Varias cifras de dependencia, urgencia social y servicios a domicilio no están confirmadas en fuente
  primaria — mantén la advertencia correspondiente en `notas` mientras sea así.
- Este catálogo no es asesoramiento legal — mantén ese aviso en el pie del panel.
- Si el usuario pide explícitamente publicar los cambios, sigue el flujo normal de git; no lo hagas por
  iniciativa propia.
