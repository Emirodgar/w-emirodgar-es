---
title: Eliminar página o URL indexada en Google
description: Aprende a eliminar una URL de forma correcta y eficiente para que no vuelva a aparecer en Google
lang: es_ES
author: Emirodgar
sitemap: 1
feed: 1
folder: seo
date: 26/09/2019
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
permalink: eliminar-url-google

---

# Eliminar página o URL indexada en Google

Existe un gran desconocimiento sobre cómo podemos hacer que nuestra página web o una URL de la misma sea desindexada correctamente de Google.

> Disponer únicamente de páginas de calidad es un [Factor SEO](factores-seo) crítico para cualquier estrategia. Por ello debemos evitar que los buscadores indexen aquellas que no aportan valor.

 **Prevenir que se indexe**

 - [Directiva noindex](#noindex)
 - [Bloqueo con disallow en robots.txt](#disallow) (no garantiza la no indexación)

**Eliminar URL indexada**

 - Error 404 o 410
 - Redirección 301
 - Herramienta de eliminación de Google (temporal) + noindex

 

## 1. Prevenir la indexación de una URL

Si aún estamos a tiempo, es mejor prevenir la indexación de nuestra página o sección por parte de los buscadores.

### 1.1. <a name="noindex"></a> Directiva noindex

> Para poder utilizar noindex dentro de una URL, ésta debe ser accesible por los buscadores por lo que **no podemos bloquear su acceso a través del robots.txt**

La [directiva **noindex**](https://developers.google.com/search/reference/robots_meta_tag) puede ser implementada a través del header de la página. Bastará con incluir la meta robots con el valor **noindex**

```
<!DOCTYPE html>
<html><head>
<meta name="robots" content="noindex" />
_(…)_
</head>
<body>_(…)_</body>
</html>
```
También podríamos configurarlo a nivel de servidor como una cabecera HTTP:

```
X-Robots-Tag: noindex
```
Siempre que un robot de búsqueda reciba la etiqueta robots con valor **noindex** la URL no será indexada..

>  La [directiva noindex bajo robots.txt ya no funciona](https://searchengineland.com/google-to-stop-supporting-noindex-directive-in-robots-txt-319003) por lo que no debemos usarla.

### 1.2. <a name="disallow"></a>Disallow en robots.txt

> El fichero robots.txt podría ser ignorado por los buscadores por lo que no es una opción que garantice al 100% la no indexación de la URL.

En el caso de que se trate de una sección amplia del sitio o que no tengamos acceso a dichas páginas para poder implementar la directiva noindex, podemos hacer uso del comando disallow del robots.txt. Para ello debemos seguir el [estándar de exclusión de robots](https://es.wikipedia.org/wiki/Est%C3%A1ndar_de_exclusi%C3%B3n_de_robots).

```
User-agent: *
Disallow: /cgi-bin/
Disallow: /tmp/
Disallow: /privado/
```

No obstante, como ya hemos comentado, el disallow **no garantiza la no indexación**.

## 2. Eliminar una URL ya indexada

En el caso de que la URL esté indexada por los buscadores, además de seguir los pasos del punto anterior, podemos hacer lo siguiente para acelerar y agilizar el proceso:

 1. Forzar un error 404 o error 410 (éste último suele ser más rápido)
 2. Aplicar una redirección 301 (suele generar un error *[404 soft](https://support.google.com/webmasters/answer/181708?hl=es)* en Google Search Console)

Como curiosidad, John Mueller confirmó a través de Twitter que siempre que exista un enlace externo hacia una de nuestras URLs, aunque ésta muestre un error 404, Google seguirá intentando indexarla de vez en cuando.

<amp-twitter 
  width="375"
  height="472"
  layout="responsive"
  data-tweetid="1107298611128352769">
</amp-twitter>


## Herramientas de Google

Google pone a nuestra disposición dos herramientas, la primera para poder [eliminar contenido puntual desde Google Search Console](https://www.google.com/webmasters/tools/url-removal) y la segunda para [eliminar contenido obsoleto](https://www.google.com/webmasters/tools/removals). Ambas no garantizan su eliminación y, de hacerlo, se trata de una **acción temporal** por lo que tendrá validez únicamente durante 90 días. A partir de entonces, podría volver a ser indexado.

## Consejos adicionales

En el caso de muchas URLs que, tras un tiempo publicadas, no queremos que sigan indexadas, podemos hacer uso de la etiqueta  [unavailable_after](https://googleblog.blogspot.com/2007/07/robots-exclusion-protocol-now-with-even.html)  de tal forma que ya vamos preparando el terreno para que, a corto plazo, Google las desindexe. Yo la suelo utilizar para páginas de eventos.

En el caso de que queramos que desaparezca información alojada en otras páginas y que están incumpliendo las normas, podemos  [seguir estos pasos](https://support.google.com/webmasters/answer/6332384?hl=es#more_information)  ya que debemos hacerlo a través del  [portal legal de Google](https://support.google.com/legal/answer/3110420?visit_id=1-636652569480291557-3013440154&rd=1).

Tags: {{page.tags}}
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTk0MTQ4NzEwLC03MzkyNDg2MTksMTA0Nz
c4MTc1MiwyNjkyNjYzMzldfQ==
-->