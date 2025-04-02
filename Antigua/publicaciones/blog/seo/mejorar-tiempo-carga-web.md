---
title: SEO - Mejorar el tiempo de carga de una web
description: El tiempo de carga es un factor clave para las estrategias de posicionamiento web
image: https://emirodgar.com/cdn/images/og/marketing-digital.png
date: 27/08/2019
author: Emirodgar
lang: es_ES
sitemap: 1
feed: 1
folder: seo
permalink: mejorar-tiempo-carga-web

---

# SEO: Mejorar el tiempo de carga de una web

Desde el [cambio de algoritmo Mobile First Index](https://emirodgar.com/cambio-algoritmo-google), el tiempo de carga de una página web pasó a ser un [factor SEO](https://emirodgar.com/factores-seo) importante en cualquier estrategia de posicionamiento.

Si queremos disponer de una página cuyo tiempo de carga sea rápido y que nos permita mejorar posicionamiento, captación y conversión, estos son los puntos que deberíamos de trabajar.

<amp-twitter 
  width="375"
  height="472"
  layout="responsive"
  data-tweetid="1194883372432134144">
</amp-twitter>

## 1. Hosting

El [hosting afecta al SEO](https://emirodgar.com/hosting-seo) por lo que el servidor donde tengamos alojada nuestra página web es el primer aspecto que debemos trabajar. Un servidor profesional nos ofrecerá buenos tiempos de conexión por lo que antes de contratarlo conviene conocer qué valor de **Time to First Byte** (TTFB) ofrece.

>[Web server perfomance test](https://www.dotcom-tools.com/web-server-performance-test.aspx) nos ayudará a validar el tiempo de carga asociado a un hosting.
>
Si tarda mucho en servir nuestra página web, el resto de carga se verá afectado por lo que garantizar un rápido envío del primer byte es crucial para un correcto tiempo de carga.

Si nuestro servidor web no los permite, podemos instalar el [módulo PageSpeed de Google](https://developers.google.com/speed/pagespeed/module/?hl=es-419) que automáticamente configurará una serie de parámetros para optimizar el sitio web.

## 2. Elementos multimedia

Tanto imágenes como vídeos pueden provocar que nuestra página sea más lenta de lo necesario. A este respecto hay varias cosas que podemos hacer:

 1. [Carga selectiva (lazy load)](https://developers.google.com/web/fundamentals/performance/lazy-loading-guidance/images-and-video/?hl=es) en base a lo que se va mostrando en pantalla. En lugar de cargar todas las imágenes o vídeos de golpe, únicamente cargamos aquellas que entran en el campo de visión del usuario. A medida que hace scroll, vamos cargando las siguientes.
 2. Hacer uso de los nuevos formatos de imágenes como [webp](https://developers.google.com/speed/webp/) para mejorar la velocidad.
 3. [Comprimir las imágenes](https://web.dev/use-imagemin-to-compress-images) para que ocupen menos espacio. Podemos hacer uso de [ImageOptim](https://imageoptim.com/mac), [Squossh](https://squoosh.app/) o [Compressor.io](https://compressor.io/)
 4. Usar [imágenes con las dimensiones adecuadas](https://web.dev/serve-images-with-correct-dimensions). No tiene sentido poner una imagen grande si la vamos a mostrar en pequeño. Para páginas multidispositivo es importante aprender a utilizar las [imágenes adaptativas](https://web.dev/uses-responsive-images/).

> También es importante [optimizar las imágenes ](https://emirodgar.com/optimizacion-imagenes-seo) para que aporten valor a la estrategia SEO.

Por último, podemos hacer uso de una r**ed de distribución de contenidos** (CDN) como Cloudflare que nos permitirá cachear y servir los ficheros estáticos de forma más rápida y eficiente, mejorando sustancialmente la carga de nuestro web

## 3. Comprimir los recursos

Hay ciertos recursos que creamos una vez y no volvemos a utilizar. Por ello se recomiendo comprimirlos al máximo (quitando espacios, comentarios o saltos de línea) para que ocupen el menor tamaño posible.

 - [Comprimir el código CSS](https://web.dev/unminified-css/). Recomiendo [CSSnano](https://github.com/ben-eb/cssnano) o [CSSO](https://github.com/css/csso). 
 - [Comprimir el código Javascript](https://web.dev/unminified-javascript/). Podemos usar [UglifyJS](https://github.com/mishoo/UglifyJS2).
 - [Comprimir el código HTML](http://minifycode.com/html-minifier/)

> Mucho ojo con [bloquear el acceso de los buscadores a los ficheros CSS y JS](https://emirodgar.com/bloquear-indexacion-js-css) puesto que podría afectar a nuestra estrategia SEO.

## 4. Eliminar aquello que no utilizamos

La forma más efectiva de aligerar nuestra web es eliminando aquello que no utilizamos. Es práctica habitual hacer un desarrollo y replicarlo a lo largo de todo el sitio web pero muchas veces, ciertas partes del mismo, son usadas de forma puntual; aún asi, las cargamos de forma transversal.

Por ejemplo, si en la home tenemos un banner y en el resto del sitio no, deberíamos tener un CSS/JS común a toda la página que no incluyera nada relacionado con el banner y, únicamente en la home, añadir ese código extra.

Podemos hacer uso de [Chrome Dev Tools](https://developers.google.com/web/updates/2017/04/devtools-release-notes#coverage) para identificar [el código CSS que no utilizamos en una página](https://web.dev/unused-css-rules/), de esa forma con retirarlo ajustaremos al máximo el tamaño de este fichero. Una aplicación online muy cómoda es [PurifyCSS](https://purifycss.online/).

También disponemos de extensiones para el navegador como [UnusedCSS](https://unused-css.com/) o [PurgeCSS](https://www.purgecss.com/) que nos facilitarán la tarea. 

Adicional a todo esto, existe un punto avanzado que también podemos trabajar. Se trata del [camino crítico para generar nuestra web](https://www.portent.com/blog/design-dev/the-critical-rendering-path-explained.htm). Si conseguimos identificar y separar la estructura crítica de lo demás -para que sea lo primero que cargue- conseguiremos una página realmente rápida.

## Herramientas para validar el tiempo de carga

Podemos hacer uso de aplicaciones como [Web.dev](https://web.dev) (basada en [Google Lighthouse](https://emirodgar.com/automatizar-analisis-lighthouse)) o [GTMetrix](https://gtmetrix.com/) para conocer qué puntos debemos otimizar en nuestra web.

<!--stackedit_data:
eyJoaXN0b3J5IjpbMTc0OTA4MzU0NCwtMTkwMTkyMTEwMSwxNT
c0OTg0NDk1LDE0MTgzODY1NDQsMTE3MDI4MzExMiwtNTUwNzM0
MDc4XX0=
-->