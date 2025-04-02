---
title: ¿Cómo afecta un CDN al SEO?
description: 
lang: es_ES
author: emirodgar
sitemap: 1
feed: 1
folder: seo
date: 27/01/2022
layout: default
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
permalink: cdn-seo

---

CDN corresponde a las siglas en inglés de *Content Delivery Network* que podríamos traducir a castellano como **Red de Distribución de Contenidos**.  Se trata por tanto de una red de ordenadores que facilitan la distribución de los contenidos de una página o aplicación web utilizando servidores geolocalizados en diversos puntos del planeta. 

![Emirodgar](https://i.imgur.com/lzH6nBd.png){:class="img-responsive"}

El objetivo de estos sistemas es por tanto **mejorar el rendimiento y la experiencia de los usuarios** al interactuar con una aplicación o página web evitando que esta tenga que atender y servir todas las peticiones.

## ¿Cómo afecta al SEO?

### Mejor tiempo de carga

Los [tiempos de carga](https://emirodgar.com/mejorar-tiempo-carga-web)  deberían disminuir ya que los servidores están más cerca geográficamente de nuestros visitantes y además emplean el almacenamiento en caché (guardan y sirven una copia de la página), por lo que los usuarios serán menos propensos a rebotar debido a la lentitud de carga de las páginas, especialmente en dispositivos móviles.

**Mejorar la experiencia de los usuarios** reduciendo el tiempo de acceso a una web es un [factor SEO](https://emirodgar.com/factores-seo) por lo que beneficiará la estrategia de posicionamiento.

Esta cuestión a veces entra en conflicto con la geolocalización de una página. Es decir, si uso un CDN y las peticiones se sirven de forma descentralizada desde múltiples nodos geográficos, pierdo el valor SEO de que mi página esté ubicada en el país donde me quiero posicionar. Eso es así, pero [como comentó Matt Cutts hace ya unos años en este vídeo](https://www.youtube.com/watch?v=hXt23AXlJJU), la geolocalización de una página ya dejó de ser un factor relevante o al menos no lo es tanto como la experiencia de los usuarios o el tiempo de carga.

### Mejor estabilidad

A mayores, los CDN nos ayudan a **mantener nuestra página siempre operativa** ya que aunque el servidor de origen falle, estos ofrecerán a los usuarios una copia de nuestra web (almacenada en caché) dándonos tiempo para que volvamos a tener el servidor en pie. El hecho de evitar caídas ofrece estabilidad, lo cuál también es apreciado por Google.

### Página más segura

Una última ventaja asociada a utilizar un CDN en nuestro proyecto web será la seguridad. Podemos entender el uso de esta red como un **cortafuegos** que nos ayuda, no sólo frente a los Ataque de denegación de servicio (DdosS), sino también para **detectar potenciales vulnerabilidades** que pongan en riesgo nuestra página.

## ¿Qué pasa si uso un DNS sólo para las imágenes?

Los CDN sólo cambian la dirección IP de nuestro sitio a través del DNS para que apunte a los servidores del nodo regional, no cambian los nombres de dominio ni las URL, por lo que ni los usuarios ni los motores de búsqueda verán ninguna diferencia. Por ejemplo, nuestro dominio `www.emirodgar.com` puede estar alojado y funcionando en un servidor local y a mayores podríamos usar el subdominio `img.emirodgar.com` como CDN para las imágenes de nuestro sitio.

A efectos de Google, todo estará bajo el dominio `emirodgar.com` y las imágenes del CDN aportarán valor a la estrategia SEO. 


## ¿Qué CDN debo usar?

Existen muchas alternativas en el mercado. Mi experiencia mayoritaria se ha centrado en Akamai y Cloudflare. No obstante, cualquier CDN que aporte mejora en el tiempo de carga, estabilidad a una web y seguridad, será beneficioso para una estrategia SEO.
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTczMjU5MTk4NiwtMTY4MjkwMzc4LDE1Mj
czODMxMjhdfQ==
-->