---
title: MacroData España, panel público de indicadores macroeconómicos
description:
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
author: Emirodgar
lang: es_ES
sitemap: 1
feed: 1
date: 2026-09-10
folder: proyectos
permalink: macrodata-espana
---

# MacroData España: panel de indicadores macroeconómicos

Seguir el pulso de la economía española debería ser tan sencillo como mirar un cuadro de mando, pero los datos relevantes están repartidos entre el INE, el Banco de España y el Banco Central Europeo, cada uno con su propio formato y calendario de publicación. **MacroData España** es una prueba de concepto que reúne en un único panel los indicadores que mejor explican la coyuntura económica del país: inflación, prima de riesgo, tipos de interés y crecimiento del PIB.

> He desarrollado una versión navegable del panel que se puede [ver aquí](https://emirodgar.es/proyectos/macrodata-espana/).

## ¿Qué es MacroData España?

Es un dashboard web, pensado como proyecto educativo y experimental, que centraliza en una sola vista:

- **Inflación (IPC)**: variación interanual del índice general y del subyacente.
- **Prima de riesgo**: diferencial entre el bono español y el bono alemán a 10 años.
- **Tipos de interés**: el tipo oficial del BCE frente al Euríbor a 12 meses.
- **Crecimiento del PIB**: tasa de variación interanual de la economía española.

Cada indicador se muestra con su valor actual, su variación respecto al periodo anterior y su evolución histórica en gráficas interactivas, además de una tabla con el detalle mes a mes.

## ¿Por qué estos cuatro indicadores?

Son las cuatro variables que más habitualmente aparecen en la conversación pública sobre la economía española porque, combinadas, cuentan una misma historia desde ángulos distintos:

- El **IPC** mide el coste de la vida y condiciona el poder adquisitivo de los hogares.
- La **prima de riesgo** resume la confianza de los mercados en la solvencia del país.
- Los **tipos de interés** (BCE y Euríbor) determinan el coste de la financiación, desde las hipotecas hasta la deuda pública.
- El **PIB** es la medida de referencia del crecimiento económico agregado.

## Fuentes de los datos

El panel está diseñado para nutrirse de fuentes oficiales:

- **IPC general y subyacente**: [INE, Índice de Precios de Consumo](https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736176802).
- **Prima de riesgo**: diferencial de rentabilidad entre el bono español y el bono alemán a 10 años, calculado a partir de los datos de mercado del [Banco de España](https://www.bde.es/) y el Tesoro Público.
- **Tipos del BCE**: decisiones de política monetaria publicadas por el [Banco Central Europeo](https://www.ecb.europa.eu/).
- **Euríbor a 12 meses**: media mensual publicada por el Banco de España, calculada según la metodología de EMMI.
- **PIB**: [INE, Contabilidad Nacional Trimestral de España](https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736164439).

Los datos se sustituyen por cifras reales cada vez que se ejecuta la skill de mantenimiento del proyecto (ver más abajo), que deja constancia de la fecha de la última actualización en el propio panel. La única excepción es la prima de riesgo: al no disponer de un feed de mercado diario integrado en el panel, su serie histórica mensual combina lecturas puntuales publicadas en prensa económica con una interpolación entre ellas, por lo que debe tomarse como una aproximación y no como una cifra oficial cerrada.

## Cómo se mantiene actualizado

El panel se actualiza mediante una skill de Claude Code creada para este proyecto. Al ejecutarla, busca la última cifra publicada de cada indicador en sus fuentes oficiales, añade el nuevo dato al histórico y actualiza el resumen ejecutivo que aparece tanto en el panel como en la portada de Emirodgar.es.

## Proyecto experimental

Como el resto de [proyectos e ideas de transformación digital](https://emirodgar.es/publicaciones-proyectos) que comparto, MacroData España es una prueba de concepto con fines educativos: no sustituye a las estadísticas oficiales ni pretende ser una fuente autorizada, sino una forma sencilla de visualizar de un vistazo hacia dónde se mueve la economía española.
