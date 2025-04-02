---
description: Además de nofollow ahora contamos con sponsored y ugc
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
date: 12/09/2019
author: Emirodgar
lang: es_ES
sitemap: 1
feed: 1
folder: seo
permalink: detectar-googlebot

--- 

# Cómo detectar a Googlebot

En ciertas ocasiones es necesario identificar si el visitante de nuestro sitio es el robot de búsqueda de Google (Googlebot) y tomar ciertas acciones.

> No debemos ofrecer contenido diferente al robot y a los usuarios ya que eso sería *cloaking* y podría ser penalizado.

## ¿Cómo identificar al robot de Google?

Actualmente tenemos dos posibilidades. Bien realizamos una DNS inversa o consultamos el `User-Agent`.

### DNS inversa

Es el proceso **más fiable** pero que **más recursos implica** ya que tendremos que llevar a cabo una operación de consulta sobre la IP.

El proceso sería el siguiente:  

1.  Debemos ejecutar una petición DNS inversa sobre la IP del visitante.
2.  Si la petición devuelve un host de `googlebot.com` entonces se trata de un robot de Google.
3.  Podríamos hacer una petición DNS de nuevo sobre el host para asegurarnos de que la IP es la misma y que no hay suplantación. Este tercer paso es opcional.

Veamos un ejemplo de cómo sería este proceso

    host 66.249.66.1
    1.66.249.66.in-addr.arpa domain name pointer crawl-66-249-66-1.googlebot.com.

### User Agent

La otra opción que tenemos disponible sería consultar el `User-Agent` para comprobar si se trata de un robot de búsqueda de Google. El proceso sería el siguiente:
  
Google ofrece un [listado completo](https://support.google.com/webmasters/answer/1061943?hl=es-419) de los `User-Agent` de todos sus robots, tanto de los de búsqueda como los asignados a otros servicios.

Por ejemplo, el `User-Agent` para el robot de búsqueda sería el siguiente:

    Googlebot/2.1 (+http://www.google.com/bot.html)

Tan sólo tendríamos que comparar para saber si es Googlebot o no. Rápido y sencillo. La única pega es que alguien podría suplantar a Googlebot usando el mismo valor por lo que la única opción fiable sería la primera.
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTkyMzUwNTg2XX0=
-->