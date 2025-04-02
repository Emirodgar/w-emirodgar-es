---
title: Aplicar Lazy Load para cargar imágenes bajo demanda
description: Esta técnica nos ayudará a mejorar el tiempo de carga
lang: es_ES
author: Emirodgar
sitemap: 1
feed: 1
folder: programacion
date: 10/09/2019
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
permalink: lazy-load-carga-bajo-demanda-imagenes

---

# Aplicar Lazy Load para cargar imágenes bajo demanda

La técnica **Lazy Load** consiste en **cargar elementos de una página web bajo demanda**, es decir, cuando se van a utilizar.

Cuando accedemos a una página, por defecto descargamos todos los elementos que la componen, lo usemos o no. Si disponemos de un portfolio de clientes a mitad de la página y un 60% de la gente nunca llega a dicha sección, habremos descargado siempre las imágenes para nada.

A través de la **carga bajo demanda** únicamente cargaremos dichas imágenes si el usuario llega hasta ellas mejorando sustancialmente el [tiempo de carga de la web](https://emirodgar.com/mejorar-tiempo-carga-web) y ofreciendo una experiencia gratificante a nuestros usuarios.

Para poder llevar a cabo esta técnica tendremos que incluir el fichero [lazysizes.min.js](https://raw.githubusercontent.com/aFarkas/lazysizes/gh-pages/lazysizes.min.js) en nuestra web. Primero lo descargamos del enlace anterior y después lo incluimos de la siguiente forma

```html
<script src="[ruta]/js/lazysizes.min.js" async></script>
```

Ahora tendremos que ir a las imágenes que queremos cargar bajo demando e incluir una serie de cambios. A continuación se muestra el código original de la imagen.

```html
<img 
src="cdn/images/clients/melia-hoteles.jpg"
alt="Estrategia SEO Meliá Hoteles">
```

En el siguiendo código podemos ver los cambios realizados.

```html
<img 
data-src="cdn/images/clients/melia-hoteles.jpg"
class="lazyload" 
alt="Estrategia SEO Meliá Hoteles">
```

Básicamente hemos cambiado ```src``` por ```data-src``` y hemos incluido la clase lazyload ```class="lazyload"```. A partir de ahora esas imágenes sólo se mostrarán cuando alguien haga scroll cerca de ellas optimizando el tiempo de carga de la web. Si hacemos uso del [formato WebP](https://emirodgar.com/webp-compatibilidad) el proceso será el mismo. 

Por último, si las imágenes forman parte de una galería y necesitan estar presentes durante la carga de la página para confeccionar el esqueleto de la misma, podemos hacer uso de ```src``` con una imagen base de poco peso y que se repita en todos los huecos.

```html
<img 
src="cdn/images/clients/base.jpg" 
data-src="cdn/images/clients/melia-hoteles.jpg" 
class="lazyload" 
alt="Estrategia SEO Meliá Hoteles">
```


<!--stackedit_data:
eyJoaXN0b3J5IjpbODM0MTQ4OTUzLC0zOTA4NzU4NTAsMjA1OT
Q2MjU3OCwtOTc3MTk2Nzg0XX0=
-->