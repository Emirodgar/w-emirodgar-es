---
title: Guía SEO pra Shopify 
description: Optimizar tu ecommerce con recomendaciones SEO específicas para Shopify 
image: https://emirodgar.com/cdn/images/og/auditoria.png
date: 31/10/2019
author: Emirodgar
sitemap: 1
feed: 1
folder: seo
lang: es_ES
permalink: shopify-seo

---

# Guía SEO pra Shopify

Actualmente cerca del 4,5% de los principales ecommerces del mundo hacen uso de Shopify como plataforma de comercio electrónico. 

En esta guía quiero trasladar las principales recomendaciones SEO que he trabajado en portales Shopify. Algunas serán comunes a otros portales, otras son específicas de esta plataforma.

## Puntos a trabajar dentro de Shopify

Por defecto -y sin una configuración adecuada- Shopify, los puntos que debemos trabajar y mejorar serán:

### Evitar contenido duplicado debido a la arquitectura y enlazado interno.

Por defecto podemos encontrarnos con duplicidades dentro de Shopify de la siguiente manera:

 - Duplicidad de productos: vigilemos las URLs de `/products/` y `collections/.*/products/` ya que a veces se generan duplicidades al no establecer bien la etiqueta canónica. 
 - **Paginación de productos**: debemos evitar que éstas sean indexables aunque sí debemos permitir que Google acceda a las mismas.
 - **Variantes de un mismo producto**: mucho cuidado cuando generamos múltiples variantes de un producto que apenas aportan valor diferencial. Por ejemplo, diferentes colores, tamaños o cambios nimios. Es preferible trabajarlo a nivel de contenido sobre una única página que crear múltiples. Recomiendo [leer esta guía](https://www.searchenginejournal.com/seo-best-practices-for-color-variations/265323/) para profundizar tanto en el problema como en la solución.
 
 En el caso de que no seamos capaces de limitar los accesos a nivel técnico, podemos hacer uso del [robots.txt para no permitir el rastreo](https://help.shopify.com/en/manual/promoting-marketing/seo/hide-a-page-from-search-engines) pero ojo, eso no evitará su indexación. Para ello necesitaremos aplicar la etiqueta noindex.

En el caso de Shopify, debemos programarlo directamente desde el template de la siguiente manera:

    {% if template contains 'search' %}
    <meta name="robots" content="noindex">
    {% endif %} 

Lógicamente necesitaremos especificar cada caso (condición) en la que queramos que aparezca el noindex y por lo tanto dichas URLs no sean indexadas.

El robots.txt debería ser usado únciamente para evitar el acceso a las siguientes secciones:

-   Área de administración
-   Checkout
-   Pedidos
-   Carro de la compra
-   Búsquedas internas

### Redireccionar páginas antiguas

Cuando dejamos atrás una página o queremos consolidar varias para evitar contenido duplicado, debemos hacerlo a través de una redirección 301. 

Por desgracia no hay una forma -a excepción del servidor web- para hacerlo de forma automática por lo que la única opción que nos queda es implementarlas de forma individual desde 

    Tienda Online > Navegación > Redirecciones


### Añadir datos estructurados, principalmente de breadcrumb y productos.

Los datos estructurados nos ayudarán a transmitir información relevante a los buscadores y facilitar por tanto la rápido acceso a datos clave asociados tanto al producto como a la navegación del sitio.

Los que recomiendo incluir son:

 - [Productos](https://developers.google.com/search/docs/data-types/product): clave para cualquier ecommerce. Ofrecemos información relevante acerca del precio y otras características.
 - [Artículo](https://developers.google.com/search/docs/data-types/article): para las publicaciones del blog con el objetivo de aparecer en Google Discover y aportar información acerca de fechas de publicación y modificación.
 - [Breadcrumb](https://developers.google.com/search/docs/data-types/breadcrumb): para todo el sitio de cara a facilitar la navegación por el sitio.


### Comprimir y optimizar las imágenes

En cualquier ecommerce las imágenes son un factor clave y muy relevante. El hecho de que estén completamente optimizadas nos ayudará a que la navegación sea más fluida y la experiencia de los usuarios lo más adecuada posible.

Existen múltiples plugins para integrarse con Shopify, por ejemplo [Crush](https://crush.pics/platforms/shopify). Cualquiera que facilite la compresión de las imágenes será válido.

### Ajustar las apps necesarias para que el tiempo de carga 

A mayor número de aplicaciones/plugins que tengamos instaladas, peor rendimiento ofrecerá nuestra tienda. Por ello recomiendo ajustar al mínimo y quedarnos únicamente con aquellas que consideremos cruciales.

En el caso de SEO, es recomendable hacer uso de aquellas que ofrecen múltiples funcionalidades (como es el caso de [Smart-SEO](https://apps.shopify.com/smart-seo)) que no instalar varias con una única funcionalidad.

Otras acciones que podemos llevar a cabo para garantizar un buen tiempo de carga y experiencia de los usuarios son:

- Hacer uso de un template rápido y ligero
- Usar imágenes pequeñas
- Evitar los carruseles

 
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTc5Mzc1MzcxMiw3MDMwMzU4MjYsLTIyNT
UxMjY4NCw0MTA1MDQ2MDksNTcyODk4NzU3XX0=
-->