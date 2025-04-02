---
title: Bloquear indexación de Javascript y CSS en estrategia SEO
description: Bloquear estos archivos podría afectar a la estrategia SEO. Aprende cómo hacerlo de forma correcta
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
date: 20/08/2019
author: Emirodgar
lang: es_ES
sitemap: 1
feed: 1
folder: seo
permalink: bloquear-indexacion-js-css

---

# Bloquear indexación de Javascript y CSS en estrategia SEO

Dentro del proceso de **indexación de una página web**, podemos hacer uso de diversas instrucciones para determinar qué URLs queremos que se indexen e incluso qué formatos.

Lo lógico sería permitir que se indexe siempre **cualquier URL que aporte valor a nuestra estrategia**, incluyendo también todos los recursos - Javascript, CSS e imágenes- de los que hace uso.

<amp-twitter 
  width="375"
  height="472"
  layout="responsive"
  data-tweetid="1163769116571947009">
</amp-twitter>

En ciertas ocasiones -casi siempre por temas de recursos- limitamos los tipos de documentos a los que tienen acceso para evitar alcanzar el [límite del hosting](https://emirodgar.com/hosting-seo) donde estamos alojados.

## Cómo afecta al SEO bloquear Javascript 

El Javascript es utilizado para **dotar a una página web de funcionalidad** puesto que el HTML en el que se basa es estático.

Googlebot hace uso de Chromium para rastrear, navegar e indexar las páginas web. Con [cada cambio de algoritmo](https://emirodgar.com/cambio-algoritmo-google) va mejorando su capacidad para renderizar Javascript. Si en nuestra web utilizamos esta tecnología para mostrar contenido, el hecho de bloquear el acceso a este tipo de ficheros provocará que no pueda ejecutarlo y por tanto acceder al mismo.

> Si bloqueamos Javascript nos exponemos a que Googlebot no pueda acceder a parte de nuestro contenido

Para saber si estamos en este caso podemos hacer uso de [Google Search Console](https://search.google.com/search-console) (Inspeccionar URL) o la [prueba de optimización para móviles](https://search.google.com/test/mobile-friendly).  En el caso de que estemos bloqueando algún fichero, nos lo dirá y podremos **comprobar cómo ve Googlebot nuestra web**. 

## Cómo afecta al SEO bloquear CSS

El CSS es utilizado para la parte visual de la página web.  Esto implica que no afectará de ninguna forma a la estrategia SEO puesto que los robots de búsqueda únicamente se fijan en el código fuente de la misma y no en su parte visual. 

## ¿Qué bloqueamos sin afectar a la indexación?

Comenzaremos por [bloquear el acceso a robots SPAM](https://emirodgar.com/listado-robots-bloquear) o que no nos interesa que rastreen e indexen nuestro sitio web.  Con eso veremos una reducción bastante importante de nuestros recursos.

Por otro lado recomiendo hacer uso de servicios CDN (Content Delivery Network) como Cloudflare que nos ayudarán a cachear y optimizar la entrega de recursos estáticos.

Por último, podemos bloquear los archivos CSS ya que esta medida no afectará a la indexación ni futuro posicionamiento de la página web.


<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE1MjY0ODExODgsLTczODA4ODcyLC03OT
g0NTc0LDc2ODQ4NDQ4XX0=
-->