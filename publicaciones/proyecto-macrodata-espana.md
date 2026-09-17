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

Seguir el pulso de la economía española debería ser tan sencillo como mirar un cuadro de mando, pero los datos relevantes están repartidos entre el INE, el Banco de España, el Banco Central Europeo y la Reserva Federal, cada uno con su propio formato y calendario de publicación. **MacroData España** es una prueba de concepto que reúne en un único panel los indicadores que mejor explican la coyuntura económica del país: inflación, prima de riesgo, tipos de interés, PIB y paro, además de un termómetro propio que traduce todo ello en un único indicador de riesgo de recesión.

> He desarrollado una versión navegable del panel que se puede [ver aquí](https://emirodgar.es/proyectos/macrodata-espana/).

## ¿Qué es MacroData España?

Es un dashboard web, pensado como proyecto educativo y experimental, que centraliza en una sola vista:

- **Termómetro de riesgo de recesión**: un índice propio (0-100), visualizado como un termómetro, que combina el crecimiento, el empleo, la inflación y las condiciones financieras del propio panel en una sola lectura de riesgo.
- **¿Cómo avanza España frente a la eurozona?**: un termómetro comparativo que compara inflación, crecimiento del PIB y tasa de paro con la media de la eurozona, para saber de un vistazo si España va mejor o peor.
- **Inflación (IPC)**: variación interanual del índice general y del subyacente.
- **Prima de riesgo**: diferencial entre el bono español y el bono alemán a 10 años.
- **Tipos de interés**: el tipo oficial del BCE y el de la Reserva Federal de EE. UU., frente al Euríbor a 12 meses.
- **Crecimiento del PIB**: tasa de variación interanual de la economía española.
- **Tasa de paro (EPA)**: tasa de paro trimestral de la Encuesta de Población Activa, con su variación interanual.
- **Preguntas frecuentes**: qué significan los términos del panel (IPC, prima de riesgo, Euríbor, PIB, EPA...) y cómo interpretar sus datos, con respuestas que se generan a partir de las cifras vigentes —nunca quedan desactualizadas— y llevan marcado de datos estructurados (FAQPage) para buscadores.

Cada indicador se muestra con su valor actual, su variación respecto al periodo anterior y su evolución histórica en gráficas interactivas, además de una tabla con el detalle mes a mes.

## España, más fuerte y más inflacionaria que la eurozona

El termómetro con el que abre el panel deja un patrón claro: España crece muy por encima de la media europea (2,7% interanual frente al 1,2% de la eurozona en el 2º trimestre), pero paga esa fortaleza con más inflación (4,5% frente al 3,3% de agosto, en términos armonizados) y, sobre todo, con una tasa de paro que casi triplica la media de la eurozona (10% frente al 6,4% en julio). Es la fotografía habitual de la economía española de los últimos años: crecimiento fuerte, pero con un mercado laboral que sigue sin converger con el resto de la eurozona.

## ¿Por qué estos indicadores?

Son las variables que más habitualmente aparecen en la conversación pública sobre la economía española porque, combinadas, cuentan una misma historia desde ángulos distintos:

- El **IPC** mide el coste de la vida y condiciona el poder adquisitivo de los hogares.
- La **prima de riesgo** resume la confianza de los mercados en la solvencia del país.
- Los **tipos de interés** (BCE, Fed y Euríbor) determinan el coste de la financiación, desde las hipotecas hasta la deuda pública, y permiten comparar el ciclo monetario europeo con el estadounidense.
- El **PIB** es la medida de referencia del crecimiento económico agregado.
- La **tasa de paro** mide la salud del mercado laboral, uno de los puntos más débiles de la economía española frente a sus vecinos europeos.

## Un termómetro para resumirlo todo en un solo número

Tener siete indicadores no siempre facilita responder a la pregunta que de verdad importa: ¿hay riesgo de que la economía se frene en seco? Por eso el panel incorpora un **termómetro de riesgo de recesión**, un índice propio de 0 a 100 que combina cuatro señales con distinto peso: el crecimiento del PIB (35%), la variación interanual del paro (25%, como proxy del momentum del mercado laboral), la distancia de la inflación respecto al objetivo del 2% del BCE (15%) y las condiciones financieras —tipo del BCE y prima de riesgo— (25%). El resultado se traduce en cuatro bandas (bajo, moderado, elevado, alto) y se representa, literalmente, como un termómetro.

Es importante ser claro sobre sus límites: es un índice propio y simplificado con fines divulgativos, no una predicción ni un modelo econométrico validado, y no lo publica ni respalda ninguna institución. No incorpora el tipo de la Fed, ya que se centra en las condiciones domésticas de España. Su metodología completa —pesos y umbrales exactos— está siempre visible en el propio panel.

## Fuentes de los datos

El panel está diseñado para nutrirse de fuentes oficiales:

- **IPC general y subyacente**: [INE, Índice de Precios de Consumo](https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736176802).
- **Prima de riesgo**: diferencial de rentabilidad entre el bono español y el bono alemán a 10 años, calculado a partir de los datos de mercado del [Banco de España](https://www.bde.es/) y el Tesoro Público.
- **Tipos del BCE**: decisiones de política monetaria publicadas por el [Banco Central Europeo](https://www.ecb.europa.eu/).
- **Euríbor a 12 meses**: media mensual publicada por el Banco de España, calculada según la metodología de EMMI.
- **Tipo de la Fed**: rango objetivo del tipo de los fondos federales fijado por el FOMC de la [Reserva Federal de EE. UU.](https://www.federalreserve.gov/), mostrado como referencia comparativa internacional.
- **PIB**: [INE, Contabilidad Nacional Trimestral de España](https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736164439).
- **Tasa de paro (EPA)**: [INE, Encuesta de Población Activa](https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736176918), tasa de paro trimestral.
- **Comparativa con la eurozona**: [Eurostat](https://ec.europa.eu/eurostat), para el IPC armonizado (IPCA), el PIB y la tasa de paro armonizada de España y del conjunto de la eurozona — magnitudes metodológicamente distintas a las del IPC del INE o la tasa de paro EPA, por lo que pueden no coincidir exactamente con los otros indicadores del panel.
- **Termómetro de riesgo de recesión**: índice propio de este panel calculado a partir de los indicadores anteriores (PIB, paro, IPC, prima de riesgo y tipo del BCE); no procede de ninguna fuente externa.

Los datos se sustituyen por cifras reales cada vez que se ejecuta la skill de mantenimiento del proyecto (ver más abajo), que deja constancia de la fecha de la última actualización en el propio panel. La única excepción es la prima de riesgo: al no disponer de un feed de mercado diario integrado en el panel, su serie histórica mensual combina lecturas puntuales publicadas en prensa económica con una interpolación entre ellas, por lo que debe tomarse como una aproximación y no como una cifra oficial cerrada.

## Cómo se mantiene actualizado

El panel se actualiza mediante una skill de Claude Code creada para este proyecto. Al ejecutarla, busca la última cifra publicada de cada indicador en sus fuentes oficiales, añade el nuevo dato al histórico y actualiza el resumen ejecutivo que aparece tanto en el panel como en la portada de Emirodgar.es.

## Proyecto experimental

Como el resto de [proyectos e ideas de transformación digital](https://emirodgar.es/publicaciones-proyectos) que comparto, MacroData España es una prueba de concepto con fines educativos: no sustituye a las estadísticas oficiales ni pretende ser una fuente autorizada, sino una forma sencilla de visualizar de un vistazo hacia dónde se mueve la economía española.
