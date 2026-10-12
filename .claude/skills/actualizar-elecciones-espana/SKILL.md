---
name: actualizar-elecciones-espana
description: Actualiza el proyecto "Elecciones en España" (guía y seguimiento electoral) con la convocatoria vigente, los partidos y candidatos, la media de encuestas, las posiciones del test de afinidad y los resultados, y archiva las convocatorias ya celebradas en el histórico. Usar cuando el usuario pida "actualiza las encuestas electorales", "añade el candidato de X a Elecciones en España", "hay una nueva convocatoria electoral", "carga los resultados del 29N" o similar.
---

# Actualizar Elecciones en España

Proyecto público con una **plantilla fija** (`index.html`) que no se toca entre convocatorias. Toda la información vive en
ficheros JSON por convocatoria; la página los lee con `fetch`.

```
proyectos/elecciones-espana/
  index.html                       # plantilla única, NO editar para actualizar datos
  data/
    elecciones.json                # índice de convocatorias + lastUpdated
    <AAAA-MM-DD>/                  # una carpeta por convocatoria (fecha de la votación)
      convocatoria.json            # fechas, cámaras, hitos, veda de encuestas, fuentes
      partidos.json                # partidos, colores, escaños actuales, webs, programas
      candidatos.json              # cabezas de lista y su estado
      encuestas.json               # sondeos individuales (la media la calcula la página)
      afinidad.json                # afirmaciones del test y posición de cada partido (con fuente)
      resultados.json              # {"disponible": false} hasta el escrutinio
```

Panel: [proyectos/elecciones-espana/index.html](../../../proyectos/elecciones-espana/index.html) ·
Documentación: [publicaciones/proyecto-elecciones-espana.md](../../../publicaciones/proyecto-elecciones-espana.md)

Tras cualquier cambio, actualiza `lastUpdated` (formato «12 de Octubre, 2026») **y `lastUpdatedISO`** (AAAA-MM-DD) en `data/elecciones.json`.

## Páginas SEO generadas (IMPORTANTE)

Además del panel hay dos páginas con contenido estático que se **generan** a partir de estos mismos JSON
(para que los buscadores lean tablas, FAQ y JSON-LD sin ejecutar JavaScript):

- `a-quien-votar/index.html`: test de afinidad ampliado + explicación + FAQ.
- `programas-electorales/index.html`: comparador de posiciones por tema, con cita y fuente.
- `como-votar-por-correo/index.html`: guía del voto por correo (plazos oficiales de `convocatoria.json → votoPorCorreo`: solicitud, envío de documentación y entrega; revisa las fechas contra el calendario de la Junta Electoral Central y Correos en cada convocatoria).
- `encuestas-elecciones-generales/index.html`: media de encuestas, gráfico SVG, tablas por empresa e histórico completo. Se regenera a partir de `encuestas.json`; **si `ocultas` es true (o la fecha de hoy cae en la veda), genera una versión sin sondeos**.

**Después de tocar `afinidad.json`, `partidos.json`, `candidatos.json` o `convocatoria.json`, ejecuta:**

```bash
python -I scripts/elecciones/generar_paginas.py
```

y comprueba las cuatro páginas en el navegador. No edites esos HTML a mano: se sobrescriben. Las páginas se enlazan entre
sí y con el panel (navegación de grupo, bloque «Sigue explorando», migas y JSON-LD); si añades una página al grupo,
actualiza `GROUP_NAV` y `related()` en el script, y añádela a `sitemap.xml`.

## Reglas de neutralidad (no negociables)

1. Todos los partidos con el **mismo formato** y orden fijado por el criterio de `criterioOrden` (escaños del Congreso disuelto).
2. Ningún texto editorial. Las propuestas y posiciones se citan o parafrasean fielmente (máx. ~25 palabras) con **URL real** de la fuente.
3. **Nunca inventes una URL** ni una posición. Si no hay evidencia clara, `"posicion": "sin_posicion"`; el test lo excluye del cálculo de ese partido.
4. No inventes candidatos: si no está confirmado, `"nombre": null` y `"estado": "por_definir"` con la nota que corresponda.

## Esquemas

### `convocatoria.json`
`nombre`, `tipo` (`generales`|`autonomicas`|`municipales`|`europeas`), `fecha` (AAAA-MM-DD), `horarioVotacion`, `resumen`,
`camaras[]` (`id`: `congreso`|`senado`…, `nombre`, `escanos`, `mayoria`, `nota`), `vedaEncuestas` (`desde`, `hasta`, `nota`),
`hitos[]` (`fecha`, `fechaFin?`, `titulo`, `detalle`), `fuentes[]`. Fuente oficial del calendario: Junta Electoral Central
(`juntaelectoralcentral.es`) y BOE. Si cambia de ámbito (autonómicas…), cambia `camaras` y la página se adapta.

### `partidos.json`
`criterioOrden`, `partidos[]` con `id` (estable, mayúsculas, **el mismo id en candidatos, encuestas y afinidad**), `nombre`,
`siglas`, `color`, `ambito` (`estatal`|`autonomico`), `territorio?`, `ideologia`, `escanosActuales`, `web`, `programaUrl`
(`null` hasta que el programa oficial se publique; entonces URL directa al PDF/página oficial), `enTest` (true si entra en el
test de afinidad), `nota?`. `escanosOtros` opcional `{nombre, n, color}` para completar el total del hemiciclo.

### `candidatos.json`
`nota?`, `candidatos[]`: `partidoId`, `nombre`, `cargo`, `estado` (`anunciado`|`por_definir`|`proclamada`), `nota?`.
Cuando las Juntas Electorales proclamen las candidaturas (2 de noviembre en 2026) pasa a `proclamada`.

### `encuestas.json`
`ocultas` (bool), `metodologia`, `fuentes[]`, `sondeos[]`: `fecha`, `empresa`, `medio`, `muestra`, `tipo` (`privada`|`oficial`; el CIS es
`oficial` y queda fuera de la media por defecto), `voto` `{ "PP": 33.4, ... }` (solo los partidos que el sondeo reporta; los
ids deben existir en `partidos.json`). Fuente de partida: <https://www.politicaelectoral.com/es/espana/generales-2026/nacional>
y la página de Wikipedia «Encuestas de opinión para las elecciones generales de España de 2026»; verifica cada sondeo (fecha de
campo, muestra) contra la ficha de la empresa o el medio cuando sea posible. Añade solo sondeos nuevos, no reescribas los antiguos.

### `afinidad.json`
`aviso`, `afirmaciones[]`: `id`, `tema`, `texto`, `contexto?`, `corto?` (true = también entra en el test corto del panel; el test completo de `/a-quien-votar/` usa todas), `posiciones` `{ "PP": { "posicion": "favor"|"contra"|"matizada"|"sin_posicion",
"cita": "...", "fuente": "https://...", "fecha": "AAAA-MM" } }`. Solo para partidos con `enTest: true`. Cuando se publiquen los
programas 2026, **sustituye** las posiciones basadas en programas anteriores por las del programa nuevo y actualiza `fecha` y `fuente`.

### `resultados.json`
`{"disponible": false}` hasta el escrutinio. Después: `disponible: true`, `fechaEscrutinio`, `participacion`, `escanos` `{id: n}`
(suma = total del Congreso), `votoPct` `{id: %}`, `nota?`. Fuente: Ministerio del Interior (`infoelectoral.interior.gob.es`).

## Flujos

### A) Seguimiento semanal (encuestas)
1. Busca sondeos nuevos de grandes empresas (Sigma Dos, 40dB, GAD3, NC Report, SocioMétrica, DYM, Ipsos, More in Common, Ateneo del Dato,
   EM-Analytics, Data10, CIS…). Añádelos a `sondeos` sin duplicar (misma empresa + misma fecha).
2. Actualiza `lastUpdated`. Comprueba en el navegador (`preview_start` → `static-site`) que el gráfico y la tabla cargan sin errores.

### B) Candidatos y programas
Actualiza `candidatos.json` según anuncios oficiales de cada partido. Cuando un partido publique su programa, rellena `programaUrl`
en `partidos.json` con la URL oficial y revisa `afinidad.json` para ese partido.

### C) Veda de encuestas (OBLIGATORIO antes del 24 de noviembre de 2026)
La ley electoral prohíbe publicar encuestas los 5 días previos al voto (24-28 nov y el 29). La página las oculta sola en esas fechas por
seguridad, pero el JSON sigue siendo público en el repositorio. Por tanto, **el 23 de noviembre por la noche**: copia `encuestas.json` fuera
del repo, sustitúyelo por `{"ocultas": true, "sondeos": []}`, **ejecuta `generar_paginas.py`** (la página `/encuestas-elecciones-generales/` queda sin sondeos y el HTML estático ya no los contiene), haz commit y despliega. Tras la votación, restaura el fichero y vuelve a ejecutar el generador.

### D) Resultados (noche del 29N y escrutinio del 4 al 7 de diciembre)
Rellena `resultados.json`, restaura las encuestas, pon `partidos.json.escanosActuales` sin tocar (es el Congreso disuelto) y, cuando se
constituyan las Cortes, cambia el `estado` de la convocatoria a `historica` en `data/elecciones.json`.

### E) Nueva convocatoria
1. Crea `data/<fecha>/` copiando los 6 ficheros de la anterior y vacíalos (partidos y colores se reaprovechan).
2. Añade la convocatoria a `data/elecciones.json` con `estado: "proxima"` y deja la anterior en `historica`.
3. Rellena `convocatoria.json` con el calendario oficial; si el ámbito cambia (p. ej. autonómicas), ajusta `camaras` y los textos de `resumen`.
4. La página elige sola la convocatoria no histórica más próxima; `?e=<id>` fuerza una concreta.

## Checklist de verificación
- [ ] `preview_start` con `static-site` y abrir `/proyectos/elecciones-espana/` sin errores en consola.
- [ ] Todos los `partidoId` y claves de `voto`/`posiciones` existen en `partidos.json`.
- [ ] La suma de escaños del hemiciclo es el total del Congreso (`escanosActuales` + `escanosOtros`).
- [ ] Ninguna URL de `fuente` o `programaUrl` está inventada.
- [ ] Has ejecutado `scripts/elecciones/generar_paginas.py` y las páginas `/a-quien-votar/` y `/programas-electorales/` reflejan los datos nuevos.
