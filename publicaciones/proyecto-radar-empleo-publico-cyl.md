---
title: Radar de Empleo Público CyL, panel público de oposiciones y convocatorias de Castilla y León
description:
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
author: Emirodgar
lang: es_ES
sitemap: 1
feed: 1
date: 2026-09-15
folder: proyectos
permalink: radar-empleo-publico-cyl
---

# Radar de Empleo Público CyL: oposiciones y convocatorias de Castilla y León

Saber cuántas oposiciones convoca la Junta de Castilla y León cada año, cuántas plazas ofrece y si alguna sigue con el plazo de solicitud abierto obliga a repasar boletín a boletín el BOCYL o el propio portal de empleo público. **Radar de Empleo Público CyL** es una prueba de concepto que reúne esa información en un único cuadro de mando, en la misma línea que [MacroData España](https://emirodgar.es/macrodata-espana) y [Panel Económico CyL](https://emirodgar.es/panel-economico-cyl).

> He desarrollado una versión navegable del panel que se puede [ver aquí](https://emirodgar.es/proyectos/radar-empleo-publico-cyl/).

## ¿Qué es Radar de Empleo Público CyL?

Es un dashboard web, pensado como proyecto educativo y experimental, que centraliza en una sola vista:

- **Convocatorias publicadas cada año**: procesos selectivos de la Junta de Castilla y León.
- **Plazas ofertadas**: suma de plazas convocadas por ejercicio.
- **Convocatorias con plazo abierto ahora mismo**: para saber de un vistazo si hay algo activo.
- **Plazas por sede de examen** y **convocatorias frente a bolsas de empleo temporal**.

## Un par de matices que solo se ven mirando los datos con detalle

El catálogo muestra una evolución muy irregular: de apenas 1-2 convocatorias anuales en 2020-2021 se pasó a picos como las 1.688 plazas de 2022 o las 2.588 de 2024, para bajar a 1.418 en 2025. Y aunque en 2025 y 2026 se han publicado más convocatorias que nunca, a día de hoy ninguna tiene el plazo de solicitud abierto: la actividad de oposiciones tiene ventanas muy concentradas en el tiempo, no un goteo constante.

El otro matiz es geográfico: el campo de sede del examen del dataset oficial indica mayoritariamente Valladolid, con independencia de dónde esté el puesto de destino, porque es donde suelen celebrarse los ejercicios de los procesos selectivos centralizados. El panel lo señala explícitamente para no confundir "dónde se hace el examen" con "dónde está la plaza".

## Fuentes de los datos

El panel se nutre del [portal de datos abiertos de la Junta de Castilla y León](https://analisis.datosabiertos.jcyl.es/), dataset "Convocatorias de Empleo Público", vía su API pública — el mismo portal que alimenta [Panel Económico CyL](https://emirodgar.es/panel-economico-cyl).

## Cómo se mantiene actualizado

El panel se actualiza mediante una skill de Claude Code creada para este proyecto, que consulta la API de datos abiertos de la Junta para refrescar convocatorias, plazas, bolsas de empleo y sedes, y recalcula qué convocatorias siguen con el plazo de solicitud abierto en la fecha de la actualización.

## Proyecto experimental

Como el resto de [proyectos e ideas de transformación digital](https://emirodgar.es/publicaciones-proyectos) que comparto, Radar de Empleo Público CyL es una prueba de concepto con fines educativos: no sustituye al portal oficial de empleo público de la Junta ni pretende cubrir cada bolsa o convocatoria puntual, sino ofrecer una vista de conjunto de su evolución.
