---
title: Usar formato Webp cuando un navegador no es compatible
description: De esta forma podremos hacer uso del formato webp de Google en cualquier navegador web
lang: es_ES
author: Emirodgar
sitemap: 1
feed: 1
folder: programacion
date: 04/02/2020
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
permalink: webp-compatibilidad

---

# Usar formato WebP cuando un navegador no es compatible

WebP es un [nuevo formato de imagen](https://developers.google.com/speed/webp/) desarrollado por Google que ofrece un ratio de compresión un 25% mayor que un PNG y entre 25%-34% que el JPEG.

Utilizar WebP es nuestras páginas web nos ayudará a [mejorar el tiempo de carga](https://emirodgar.com/mejorar-tiempo-carga-web) y ofrecer una mejor experiencia a nuestros usuarios.

Por desgracia [no todos los navegadores ofrecen aún soporte](https://caniuse.com/#search=webp) a este nuevo formato por lo que en muchos casos tendremos que utilizar ambos formatos.

La forma correcta de hacerlo será la siguiente:

```html
<picture>
   <source srcset="cdn/images/2.webp" type="image/webp">
   <img src="cdn/images/2.jpg" alt="Telefónica">
</picture>
```

De esta forma, si el navegador sí permite los WebP, cargará primero dicho formato. En el caso de no saber interpretarlo cargará las imágenes en jpg.

En el caso de que necesitemos aplicarlo a imágenes dentro del CSS podemos hacer uso de la librería [Modernizr](https://modernizr.com/download?setclasses).

Esta librería trae por defecto un autodetector de soporte para WebP que podremos utilizar de la siguiente manera:

```css
.no-webp .client1 { 
   background-image:  url("image.jpg"); 
}
.webp .client1{ 
   background-image:  url("image.webp"); 
}
```

Automáticamente Modernizr sabrá qué clase aplicar y por lo tanto se cargará el formato de imagen soportado por el buscador.

Google tiene una [guía muy interesante](https://developers.google.com/speed/webp/faq#how_can_i_detect_browser_support_for_webp) que ofrece diversas formas de detectar soporte para WebP.

## Usar WebP en Wordpress

Si hacemos uso de Wordpress lo tendremos relativamente más fácil puesto que podemos instalar la extensión [WebP Express](https://es.wordpress.org/plugins/webp-express/) para, automáticamente, convertir todas las imágenes a este formato y mostrarlas siempre que el navegador sea compatible.
<!--stackedit_data:
eyJoaXN0b3J5IjpbNjI0NDE2NzIzLDQ0NDMyMTcsLTg0NTY5NT
Y0MSwtMjk2NTQ0MDg2XX0=
-->