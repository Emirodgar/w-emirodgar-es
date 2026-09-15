---
title: Panel Económico CyL, panel público de presupuestos y subvenciones de Castilla y León
description:
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
author: Emirodgar
lang: es_ES
sitemap: 1
feed: 1
date: 2026-09-15
folder: proyectos
permalink: panel-economico-cyl
---

# Panel Económico CyL: presupuestos y subvenciones de Castilla y León

Saber cuánto presupuesto tiene realmente en vigor la Junta de Castilla y León, o qué está aprobando en materia de ayudas y subvenciones, obliga a cruzar leyes de presupuestos, notas de prensa y el portal de datos abiertos de la propia Junta. **Panel Económico CyL** es una prueba de concepto que reúne esa información en un único cuadro de mando, en la misma línea que [MacroData España](https://emirodgar.es/macrodata-espana).

> He desarrollado una versión navegable del panel que se puede [ver aquí](https://emirodgar.es/proyectos/panel-economico-cyl/).

## ¿Qué es Panel Económico CyL?

Es un dashboard web, pensado como proyecto educativo y experimental, que centraliza en una sola vista:

- **Presupuesto autonómico vigente**: el presupuesto realmente en vigor cada año, distinguiendo entre lo aprobado y lo prorrogado.
- **Importe concedido en subvenciones**: la serie histórica de concesiones publicada por la Junta.
- **Catálogo de líneas de ayuda**: cuántas líneas de ayuda y subvención se publican cada año.
- **Reparto por materia**: en qué áreas se concentran las líneas de ayuda vigentes.

## Un hallazgo poco conocido: dos prórrogas presupuestarias seguidas

La primera versión del panel ya deja un dato llamativo: las Cortes de Castilla y León rechazaron en noviembre de 2025 el proyecto de Presupuestos para 2026 (15.715 millones de euros), por lo que la Comunidad arrastra su segunda prórroga presupuestaria consecutiva y sigue funcionando con el presupuesto de 2024 (14.562 millones). Es la sexta prórroga en siete años.

A esto se suma otra circunstancia menos visible: el portal de datos abiertos de la Junta dejó de publicar el detalle de subvenciones concedidas en marzo de 2022, así que el último ejercicio completo con cifras de concesión disponible es 2021. En cambio, el catálogo de líneas de ayuda vigentes sí se sigue actualizando con normalidad.

## Fuentes de los datos

El panel combina dos tipos de fuentes:

- **Presupuesto autonómico**: leyes de Presupuestos Generales de la Comunidad (BOE/BOCYL) y cobertura de prensa económica regional sobre su tramitación en las Cortes.
- **Subvenciones concedidas** y **catálogo de líneas de ayuda**: [portal de datos abiertos de la Junta de Castilla y León](https://analisis.datosabiertos.jcyl.es/), datasets "Subvenciones concedidas" y "Ayudas y Subvenciones", vía su API pública.

## Cómo se mantiene actualizado

El panel se actualiza mediante una skill de Claude Code creada para este proyecto, que consulta la API de datos abiertos de la Junta y contrasta la situación presupuestaria con fuentes oficiales y de prensa, dejando constancia de la fecha de la última actualización en el propio panel.

## Proyecto experimental

Como el resto de [proyectos e ideas de transformación digital](https://emirodgar.es/publicaciones-proyectos) que comparto, Panel Económico CyL es una prueba de concepto con fines educativos: no sustituye a las fuentes oficiales ni pretende ser una auditoría exhaustiva, sino una forma sencilla de ver de un vistazo cómo evolucionan las cuentas públicas y las ayudas de Castilla y León.
