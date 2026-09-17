---
title: Simulador de Hipotecas en España, calculadora con predicción de escenarios de tipos
description:
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
author: Emirodgar
lang: es_ES
sitemap: 1
feed: 1
date: 2026-09-17
folder: proyectos
permalink: simulador-hipotecas-espana
---

# Simulador de Hipotecas en España: calculadora con predicción de escenarios de tipos

Decidir entre una hipoteca fija o variable obliga a comparar ofertas de varios bancos, entender el Euríbor y, sobre todo, hacerse una pregunta incómoda: ¿y si suben los tipos? **Simulador de Hipotecas en España** es una prueba de concepto que reúne el mercado hipotecario español, una comparativa de bancos y una calculadora de cuota en un único panel, en la misma línea que [MacroData España](https://emirodgar.es/macrodata-espana), de donde toma en vivo el Euríbor y el termómetro de riesgo de recesión.

> He desarrollado una versión navegable del panel que se puede [ver aquí](https://emirodgar.es/proyectos/simulador-hipotecas-espana/).

## ¿Qué es Simulador de Hipotecas en España?

Es un dashboard web, pensado como proyecto educativo y experimental, que centraliza en una sola vista:

- **El mercado hipotecario español**: tipo de interés medio, importe medio concedido, número de hipotecas constituidas y el reparto entre hipoteca fija, variable y mixta, con datos del INE.
- **Una comparativa de bancos**: TIN y TAE de fija y variable de varias entidades principales, con sus condiciones y bonificaciones habituales.
- **Una calculadora de cuota**: introduces importe, plazo y tipo de interés (o eliges un banco de la comparativa) y calcula tu cuota mensual, el coste total y los intereses totales, comparando fija frente a variable.
- **Escenarios de "qué pasaría si"**: para hipotecas variables, muestra cómo cambiaría tu cuota si el Euríbor sube, se mantiene o baja un punto, cada uno con una probabilidad estimada.
- **Preguntas frecuentes**: qué son el TIN, la TAE, el diferencial, o cómo se calculan las probabilidades de los escenarios.

## Cómo se calculan las probabilidades de los escenarios

Este es el componente más particular del panel. En lugar de inventar una predicción de mercado, reutiliza el [termómetro de riesgo de recesión](https://emirodgar.es/macrodata-espana) de MacroData España —pero no su número agregado, sino sus componentes de crecimiento, empleo e inflación por separado, porque el agregado no dice en qué dirección apunta el riesgo—:

- Un crecimiento débil o un paro al alza empujan la probabilidad hacia una **bajada** de tipos: los bancos centrales suelen recortar tipos para estimular una economía que se enfría.
- Una inflación alejada del objetivo del 2% del BCE empuja la probabilidad hacia una **subida** o el mantenimiento de los tipos.

Con eso se reparte una probabilidad entre subir, mantenerse o bajar, que se recalcula en el momento cada vez que cambian los datos de MacroData España. Es un modelo propio y simplificado con fines divulgativos: **no es una predicción de mercado ni asesoramiento financiero**, y así se indica de forma visible en el propio panel.

## Fuentes de los datos

- **Mercado hipotecario**: INE, Estadística de Hipotecas (tipo de interés medio, importe medio, número de hipotecas constituidas y reparto fijo/variable/mixto).
- **Comparativa de bancos**: webs y comparadores públicos de cada entidad, con la fecha de consulta de cada oferta.
- **Euríbor y termómetro de riesgo de recesión**: leídos en vivo del panel [MacroData España](https://emirodgar.es/macrodata-espana), sin duplicar el dato en este panel.

## Cómo se mantiene actualizado

El panel se actualiza mediante una skill de Claude Code creada para este proyecto, que revisa la última publicación del INE y las ofertas vigentes de cada banco. El Euríbor y el termómetro de riesgo no requieren mantenimiento aquí: se sincronizan automáticamente con MacroData España.

## Proyecto experimental — no es asesoramiento financiero

Como el resto de [proyectos e ideas de transformación digital](https://emirodgar.es/publicaciones-proyectos) que comparto, este simulador es una prueba de concepto con fines educativos. La calculadora usa la fórmula estándar de amortización francesa, sin tener en cuenta tu solvencia, tus ingresos ni los gastos de formalización, y los escenarios de tipos son ilustrativos, no una predicción fiable. No sustituye a una oferta vinculante de tu banco ni al consejo de un asesor financiero profesional.
