---
title: Panel Económico CyL, panel público de presupuestos, subvenciones y mercado laboral de Castilla y León
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

# Panel Económico CyL: presupuestos, subvenciones y mercado laboral de Castilla y León

Saber cuánto presupuesto tiene realmente en vigor la Junta de Castilla y León, qué está aprobando en materia de ayudas y subvenciones, o si la economía regional avanza bien y cómo se compara cada provincia, obliga a cruzar leyes de presupuestos, notas de prensa y varios datasets del portal de datos abiertos de la propia Junta. **Panel Económico CyL** es una prueba de concepto que reúne esa información en un único cuadro de mando, en la misma línea que [MacroData España](https://emirodgar.es/macrodata-espana).

> He desarrollado una versión navegable del panel que se puede [ver aquí](https://emirodgar.es/proyectos/panel-economico-cyl/).

## ¿Qué es Panel Económico CyL?

Es un dashboard web, pensado como proyecto educativo y experimental, que abre con un termómetro
comparativo y luego se organiza en dos bloques:

**¿Cómo avanza Castilla y León?**
Cuatro indicadores clave —crecimiento del PIB, tasa de paro EPA, variación del paro registrado y
variación de la afiliación a la Seguridad Social— comparados con el dato equivalente de España, para
responder de un vistazo si la Comunidad va mejor o peor que la media nacional en cada uno.

**Presupuesto y subvenciones**
- **Presupuesto autonómico vigente**: el presupuesto realmente en vigor cada año, distinguiendo entre lo aprobado y lo prorrogado.
- **Importe concedido en subvenciones**: la serie histórica de concesiones publicada por la Junta.
- **Catálogo de líneas de ayuda**: cuántas líneas de ayuda y subvención se publican cada año.

**Mercado laboral y actividad económica**
- **Paro registrado** y **afiliación a la Seguridad Social**: su evolución mensual en el conjunto de la Comunidad.
- **Contratos registrados**, con el desglose entre indefinidos y temporales.
- **Detalle por provincia**: cómo se reparten el paro, la afiliación y la contratación entre las 9 provincias, para comparar de un vistazo cómo se desarrolla cada una.

## Un panorama con más sombras que luces frente a España

El termómetro con el que abre el panel deja un balance poco favorable: de los cuatro indicadores comparables con España, solo la tasa de paro EPA (8,37% frente al 9,87% nacional) le es claramente favorable a Castilla y León. En los otros tres —PIB, afiliación a la Seguridad Social y variación del paro registrado— la Comunidad mejora en términos absolutos, pero crece o mejora por debajo del ritmo español.

Las Cortes de Castilla y León rechazaron en noviembre de 2025 el proyecto de Presupuestos para 2026 (15.715 millones de euros), por lo que la Comunidad arrastra su segunda prórroga presupuestaria consecutiva y sigue funcionando con el presupuesto de 2024 (14.562 millones) — es la sexta prórroga en siete años. A esto se suma que el portal de datos abiertos de la Junta dejó de publicar el detalle de subvenciones concedidas en marzo de 2022, así que el último ejercicio completo con cifras de concesión disponible es 2021.

En el plano laboral, el panel deja ver una Castilla y León con luces y sombras: la afiliación a la Seguridad Social crece (+1,9% interanual en agosto de 2026) mientras el paro registrado apenas se mueve, pero la contratación sigue dominada por la temporalidad (solo el 31,1% de los contratos de agosto fueron indefinidos) y esa proporción varía muchísimo por provincia: de un 13,9% en Palencia a un 39,2% en León.

## Fuentes de los datos

El panel combina varios tipos de fuentes:

- **Presupuesto autonómico**: leyes de Presupuestos Generales de la Comunidad (BOE/BOCYL) y cobertura de prensa económica regional sobre su tramitación en las Cortes.
- **Subvenciones concedidas** y **catálogo de líneas de ayuda**: [portal de datos abiertos de la Junta de Castilla y León](https://analisis.datosabiertos.jcyl.es/), datasets "Subvenciones concedidas" y "Ayudas y Subvenciones".
- **Paro, afiliación y contratos**: el mismo portal de datos abiertos, datasets "Paro registrado en las provincias de Castilla y León", "Afiliación media a la Seguridad Social en las provincias de Castilla y León" y "Contratos realizados en las provincias de Castilla y León" — todos ellos vía su API pública, con series mensuales y desglose por provincia.
- **Comparativa con España**: INE (Contabilidad Regional Trimestral y Encuesta de Población Activa), SEPE (paro registrado) y Ministerio de Inclusión, Seguridad Social y Migraciones (afiliación), para los datos nacionales del termómetro.

## Cómo se mantiene actualizado

El panel se actualiza mediante una skill de Claude Code creada para este proyecto, que consulta la API de datos abiertos de la Junta y contrasta la situación presupuestaria con fuentes oficiales y de prensa, dejando constancia de la fecha de la última actualización en el propio panel.

## Proyecto experimental

Como el resto de [proyectos e ideas de transformación digital](https://emirodgar.es/publicaciones-proyectos) que comparto, Panel Económico CyL es una prueba de concepto con fines educativos: no sustituye a las fuentes oficiales ni pretende ser una auditoría exhaustiva, sino una forma sencilla de ver de un vistazo cómo evolucionan las cuentas públicas y las ayudas de Castilla y León.
