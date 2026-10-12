---
title: Elecciones en España, guía visual y seguimiento de cada convocatoria electoral
description: Proyecto experimental con el calendario, los partidos, la media de encuestas, un test de afinidad y el histórico de cada convocatoria electoral, empezando por las generales del 29 de noviembre de 2026.
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
author: Emirodgar
lang: es_ES
sitemap: 1
feed: 1
date: 2026-10-12
folder: proyectos
permalink: elecciones-espana
---

# Elecciones en España: quién se presenta, qué proponen y cómo van las encuestas

Cuando se convocan elecciones, la información útil para decidir el voto está repartida entre el BOE, las webs de los partidos, los medios y los agregadores de encuestas. **Elecciones en España** es una prueba de concepto que la reúne en un único panel visual, en la misma línea que [MacroData España](https://emirodgar.es/macrodata-espana) y [¿Quién Gobierna CyL?](https://emirodgar.es/quien-gobierna-cyl). Empieza con las **elecciones generales del 29 de noviembre de 2026**.

> He desarrollado una versión navegable del panel que se puede [ver aquí](https://emirodgar.es/proyectos/elecciones-espana/).

## Qué incluye

- **Cuenta atrás y calendario electoral**, con el estado de cada hito (campaña, voto por correo, jornada de reflexión, escrutinio, constitución de las Cortes).
- **Media de encuestas** con evolución en el tiempo, el cambio frente a dos semanas antes y la tabla completa de sondeos con su empresa, fecha y muestra.
- **Quién se presenta**: una tarjeta idéntica para cada partido, con su candidato, su estado (anunciado o por definir), su web y el enlace a su programa oficial cuando se publique.
- **El Congreso hoy**: hemiciclo con los 350 escaños del Congreso disuelto y la línea de la mayoría absoluta.
- **Test de afinidad**: afirmaciones sobre políticas concretas; al final, la coincidencia con cada partido, con la cita y la fuente de cada posición. El cálculo se hace en el navegador y no se guarda nada.
- **Cómo se vota**, con un simulador de la ley D'Hondt, y unas **preguntas frecuentes** generadas a partir de los datos.
- **Histórico**: cada convocatoria queda archivada con sus resultados.

El proyecto se completa con dos guías específicas: [¿A quién votar? Test de afinidad completo](https://emirodgar.es/a-quien-votar/), con temas prioritarios y explicación de cada resultado, y el [comparador de programas electorales](https://emirodgar.es/programas-electorales/), con las posiciones de cada partido por temas y su fuente.

## Una plantilla fija para todas las elecciones

La página no cambia entre convocatorias. Cada una vive en su propia carpeta de ficheros JSON (`convocatoria`, `partidos`, `candidatos`, `encuestas`, `afinidad`, `resultados`) y un índice `elecciones.json` decide cuál es la próxima y cuáles son histórico. Para unas autonómicas o unas europeas basta con crear una nueva carpeta con el mismo esquema.

## Cómo se calcula la media de encuestas

Cada sondeo se pondera por su antigüedad (vida media de 14 días) y por la raíz de su muestra, y solo cuentan los publicados en los 30 días previos al último. Para cada partido se promedian únicamente los sondeos que lo incluyen. El CIS se muestra pero queda fuera de la media por defecto, porque su metodología es distinta, aunque se puede incluir con un interruptor. Son estimaciones de voto, no de escaños.

## Neutralidad y límites

- Todos los partidos tienen el mismo formato y se ordenan por un criterio objetivo (escaños del Congreso disuelto).
- Las posiciones del test se citan con su fuente; cuando no hay evidencia clara, se marcan «sin posición» y no cuentan.
- La ley electoral prohíbe publicar encuestas en los cinco días previos a la votación, así que el panel las retira del 24 de noviembre hasta la jornada de votación.
- Es un proyecto educativo y experimental: comprueba siempre los datos oficiales en la [Junta Electoral Central](https://www.juntaelectoralcentral.es) y el [Ministerio del Interior](https://www.infoelectoral.interior.gob.es).
