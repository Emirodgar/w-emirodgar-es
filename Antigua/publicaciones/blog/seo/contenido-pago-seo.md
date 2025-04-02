---
description: Podemos mostrar contenidos de pago a Google pero que no sean accesibles a los usuarios
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
date: 03/03/2020
author: Emirodgar
lang: es_ES
sitemap: 1
feed: 1
folder: seo
permalink: contenidos-pago-google

--- 

# Contenidos de pago en Google

Cada vez más periódicos digitales se están pasando al modelo de suscripción. Existen varias opciones:

 - **Muro de pago**: todas las publicaciones son de pago y es necesario una suscripción para su acceso.
 - **Muro de pago mixto**: algunas publicaciones son gratuitas y otras de pago. Para poder acceder a todo hay que tener una suscripción.
 - **Prueba gratuita**: las primeras publicaciones son gratuitas -para que puedas evaluar la calidad de las mismas- y a partir de un número determinado tienes que pagar para seguir leyendo.
 - **Contenido mixto**: el comienzo de la noticia es gratuito pero para leerla completa hay que tener suscripción.

Google Noticias ya tiene su [propio sistema de ingresos](https://support.google.com/news/publisher-center/answer/9606543?visit_id=637188253321907152-220207309&rd=1&hl=es) por lo que si está activo en nuestro país podemos solicitar participar en dicho programa. Si no, tendremos que preparar nuestra web a nivel técnico para que Google no tenga problemas con nuestros contenidos de pago. 

## Cómo evitar penalizaciones por cloacking

Las **técnicas de ocultación** o **cloaking** consisten en mostrar contenido diferente a usuarios y a robots de búsqueda. Están penalizadas por Google y suelen acarrean desposicionamientos bastante grandes.

Para evitar problemas [Google ha dispuesto una guía](https://developers.google.com/search/docs/data-types/paywalled-content) bastante completa en la que nos enseña los pasos a seguir para poder hacer accesible a sus robots de búsqueda contenidos de pago **sin generar cloacking**.

### Usar etiquetas para el contenido de pago

Si ofrecemos una parte gratuita y otra de pago, la recomendación que nos da Google es etiquetar a través de los [datos estructurados de `NewsArticle`](https://developers.google.com/search/docs/data-types/article) que se trata de un artículo de pago y establecer el selector `CSS` que determinará qué partes son de pago y cuáles gratuitas.

En el siguiente ejemplo utilizaremos la clase `paywall`  para determinar párrafos de contenido de pago.

```html
<body>  
<p>Contenido gratuito</p>  
<div class="paywall">Contenido de pago.</div>  
</body>
```
Y en los datos estructurados indicaremos que existen zonas de pago a través de la opción `isAccessibleForFree` a `False` e indicando que serán las que incluyan el `cssSelector` con valor `paywall`.

```json
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://example.org/article"
  },
  "isAccessibleForFree": "False",
  "hasPart": {
    "@type": "WebPageElement",
    "isAccessibleForFree": "False",
    "cssSelector": ".paywall"
  }
}
```

### No bloquear a Googlebot

Para que [Google pueda rastrear e indexar nuestras páginas](https://emirodgar.com/google-rastreo) es necesario que no bloqueemos el rastreo a través del `robots.txt` ni la indexación con la etiqueta `noindex`. 

> Cuidado con [bloquear ficheros como Javascript o CSS](https://emirodgar.com/bloquear-indexacion-js-css) ya que podría causar problemas en el proceso de indexación.

Para garantizar un mayor control en los accesos a los contenidos de pago también podemos [detectar los accesos de Googlebot](https://emirodgar.com/detectar-googlebot) a nuestra página aunque no es recomendable ofrecer al robot un contenido distinto que a los usuarios ya que eso sería cloaking. Lo podemos usar a modo de verificación de que el proceso funciona correctamente. 
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTQ5OTM0NzA5NCw3MDcwNzgyODUsLTE3Mz
cxMzAxMjVdfQ==
-->