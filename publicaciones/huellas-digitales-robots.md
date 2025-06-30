---
title: Huellas digitales de robots de rastreo
description: 
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
author: Emirodgar
lang: es_ES
sitemap: 1
feed: 1
date: 30-06-2025
folder: ia
permalink: huellas-digitales-robots
---


# Huellas digitales de robots de rastreo

Ojo con los "bots buenos" y la visibilidad online. Hoy en día, el mundo digital está lleno de bots; no solo de los que nos dan problemas, sino también de otros que son esenciales para que nuestra información llegue a más gente. Con el auge de plataformas de SEO, marketing y, sobre todo, la Inteligencia Artificial, la cantidad de estos "rastreadores" que recorren la web para recopilar y verificar datos no para de crecer.

![image](https://github.com/user-attachments/assets/ebfeb6fb-2f68-4035-a2d4-0c5115e52651){:class="img-responsive"}


## ¿Por qué son importantes estos bots?

Imagina que estos bots son como pequeños exploradores que buscan y organizan la información de tu web para que los buscadores como Google, o incluso los modelos de lenguaje de la IA (como ChatGPT), puedan encontrarla y mostrarla cuando alguien la busca. Si bloqueamos a estos exploradores por error, es como cerrar la puerta a nuestra propia visibilidad.

## El riesgo de un bloqueo incorrecto

El problema surge cuando, sin querer, nuestras herramientas de seguridad, como las CDNs (redes de entrega de contenido) o los sistemas de protección automatizados, confunden a estos bots "buenos" con los "malos" y les impiden el acceso. ¿El resultado? Una disminución notable de nuestra visibilidad en los motores de búsqueda y en las respuestas de los modelos de IA. Esto significa que a la gente le costará más encontrarnos, lo que se traduce en menos visitas y, para las empresas, en menos clientes potenciales.

Además, si tienes campañas de marketing de pago en marcha, un bloqueo erróneo puede causar problemas serios en su funcionamiento, haciendo que inviertas dinero sin obtener los resultados esperados.

## La solución: identificar a los bots "buenos"

Para evitar estos dolores de cabeza, es fundamental asegurarnos de que los bots que nos benefician puedan hacer su trabajo sin impedimentos. Esto implica tener una lista actualizada de lo que llamamos "bots buenos" y las firmas o "identificaciones" de cada uno de ellos. De esta forma, nuestros sistemas de seguridad automatizados podrán reconocerlos y permitirles el paso, saltándose las limitaciones de velocidad u otros bloqueos que tengamos activados. A raíz de esto surge [este proyecto](https://bots.searchtheory.io/) para mantener una base de datos comunitaria y actualizada. Comparto la tabla de huellas digitales de los bots conocidos hasta hoy:

| Bot Name             | User Agent Patterns                                                                 |
|----------------------|--------------------------------------------------------------------------------------|
| Googlebot Image      | `^.*Googlebot-Image.*$`                                                              |
| Googlebot Video      | `^.*Googlebot-Video.*$`                                                              |
| Googlebot            | `^.*(?!.*Mobile).*Googlebot.*$`<br>`^.*Mobile.*Googlebot.*$`                         |
| Google-InspectionTool| `^.*(?!.*Mobile).*Google-InspectionTool.*$`<br>`^.*Mobile.*Google-InspectionTool.*$` |
| GoogleOther-Image    | `^.*GoogleOther-Image.*$`                                                            |
| GoogleOther-Video    | `^.*GoogleOther-Video.*$`                                                            |
| GoogleOther          | `^.*(?!.*Mobile).*GoogleOther.*$`<br>`^.*Mobile.*GoogleOther.*$`                     |
| Google StoreBot      | `^.*Storebot-Google.*(?!.*Mobile).*$`<br>`^.*Storebot-Google.*Mobile.*$`            |
| Google AdsBot        | `^.*AdsBot-Google(?!-Mobile).*$`<br>`^.*AdsBot-Google-Mobile.*$`                    |
| Google AdSense       | `^.*Mediapartners-Google.*$`                                                         |
| Google-Safety        | `^.*Google-Safety.*$`                                                                |
| OAI-SearchBot        | `^.*OAI-SearchBot.*$`                                                                |
| ChatGPT-User         | `^.*ChatGPT-User.*$`                                                                 |
| DuckAssistBot        | `^.*DuckAssistBot.*$`                                                                |
| DuckDuckBot          | `^.*DuckDuckBot.*$`                                                                  |
| GPTBot               | `^.*GPTBot.*$`                                                                       |
| Perplexity-User      | `^.*Perplexity-User.*$`                                                              |
| MistralAI-User       | `^.*MistralAI-User.*$`                                                               |
| PerplexityBot        | `^.*PerplexityBot.*$`                                                                |
| AdIdxBot             | `^(?!.*Mobile).*adidxbot.*$`<br>`^.*Mobile.*adidxbot.*$`                             |
| Bingbot              | `^(?!.*(?:Mobile|adidxbot)).*bingbot.*$`<br>`^.*Mobile(?!.*adidxbot).*bingbot.*$`   |
| Applebot             | `^.*(?!.*Mobile).*Applebot.*$`<br>`^.*Mobile.*Applebot.*$`                           |
