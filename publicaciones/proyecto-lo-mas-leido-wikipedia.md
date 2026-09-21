---
title: Lo Más Leído en Wikipedia, resumen semanal en español del Top 25 Report
description:
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
author: Emirodgar
lang: es_ES
sitemap: 1
feed: 1
date: 2026-09-21
folder: proyectos
permalink: lo-mas-leido-wikipedia
---

# Lo Más Leído en Wikipedia: resumen semanal en español del Top 25 Report

Cada semana, la Wikipedia en inglés publica el [Top 25 Report](https://en.wikipedia.org/wiki/Wikipedia:Top_25_Report), un informe elaborado por editores voluntarios con los 25 artículos más visitados de esa semana y un comentario sobre por qué han generado tanto interés. Es una fotografía muy fiel de qué está pasando en el mundo —o qué está reviviendo el algoritmo colectivo de la curiosidad—, pero está en inglés y no siempre es fácil de seguir semana a semana. **Lo Más Leído en Wikipedia** es una prueba de concepto que resume ese informe en español cada semana, en la misma línea que el resto de [proyectos y paneles en vivo](https://emirodgar.es/publicaciones-proyectos) que comparto.

> He desarrollado una versión navegable del panel que se puede [ver aquí](https://emirodgar.es/proyectos/lo-mas-leido-wikipedia/).

## ¿Qué es Lo Más Leído en Wikipedia?

Es un dashboard web, pensado como proyecto educativo y experimental, que centraliza en una sola vista:

- **Los 25 artículos más leídos de la semana**, con sus visitas y un resumen en español —redacción propia, no traducción— de por qué han generado interés.
- **Una clasificación temática propia** (Cine y TV, Deportes, Sucesos y Justicia, Historia y Sociedad, Política, Fallecimientos, Internet y Cultura Digital), ya que el informe original no clasifica los artículos por tema.
- **El reparto de visitas por categoría**, para ver de un vistazo si la semana la ha dominado el cine, el deporte, la actualidad política o un suceso puntual.
- **Un histórico semana a semana** de las visitas totales del Top 25 y de qué artículo ha liderado el ranking, para poder seguir la evolución con el tiempo.

## Cómo se genera cada semana

El panel se actualiza mediante una skill de Claude Code creada para este proyecto y una tarea programada semanal: cada semana se consulta el Top 25 Report original, se extraen el ranking, las visitas y los enlaces de cada artículo, se clasifican en una de las siete categorías temáticas fijas y se redactan en español, de forma independiente, los motivos de su popularidad —sin traducir literalmente el comentario original, tanto por una cuestión de estilo como de derechos de autor—. Con cada actualización se recalculan los indicadores, el gráfico de categorías y el histórico semanal, que conserva las últimas 12 semanas.

## Un matiz importante sobre los datos

El ranking del Top 25 Report no distingue entre "noticia puntual" y "artículo de referencia": junto a temas claramente ligados a la actualidad de la semana (un estreno de cine, un resultado electoral, un torneo deportivo) conviven artículos que se consultan de forma recurrente, como el que recopila los fallecimientos del año en curso. Verlos mezclados en el mismo ranking es, de hecho, parte de lo interesante del informe: muestra tanto lo que es noticia esta semana como lo que la gente sigue consultando por costumbre.

## Fuentes de los datos

El panel se nutre del [Top 25 Report](https://en.wikipedia.org/wiki/Wikipedia:Top_25_Report) de la Wikipedia en inglés, que a su vez se basa en las estadísticas oficiales de visitas de la Wikimedia Foundation. La clasificación temática de cada artículo y los resúmenes en español son elaboración propia a partir de esos datos, no contenido oficial del informe.

## Proyecto experimental

Como el resto de [proyectos e ideas de transformación digital](https://emirodgar.es/publicaciones-proyectos) que comparto, Lo Más Leído en Wikipedia es una prueba de concepto con fines educativos: no sustituye al Top 25 Report original ni pretende ser una traducción oficial, sino ofrecer una forma rápida de seguir en español qué genera más interés en Wikipedia cada semana.
