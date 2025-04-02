---
title: Optimización SEO en Jekyll
description: Guía completa para optimizar el SEO en Jekyll
lang: es_ES
author: Emirodgar
sitemap: 1
feed: 1
folder: jekyll
date: 07/04/2019
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
permalink: optimizacion-seo-jekyll

---

# Optimización SEO en Jekyll

Jekyll es uno de los generadores de sitios web estáticos más populares en la actualidad. Utiliza **HTML** y **Markdown** para crear un sitio web listo para ser alojado en cualquier servidor web. 

La rapidez y sencillez con la que podemos crear una web debe siempre acompañar a una correcta [optimización SEO](factores-seo) ya que si no, estaremos perdiendo la oportunidad de captar tráfico de calidad.

## Estructura inicial

Lo primero será crear el fichero de configuración [_config.yml](https://github.com/mmistakes/jekyll-theme-basically-basic/blob/master/_config.yml) y la carpeta "_layouts". Dentro de la misma deberá existir un "default.html".

Para poder hacer uso de las [funcionalidades SEO que tiene Jekyll](http://jekyll.github.io/jekyll-seo-tag/usage/) debemos incluir el siguiente código dentro de nuestro HTML (sin espacios entre las llaves y los %):

```
<html>
 <head>
   { % seo % }
...
```

Jekyll sustituirá la variable ```{ % seo % }``` por una serie de código HTML relacionados con el SEO y que nos facilitarán el posicionamiento web de nuestra página.

Dentro de nuestro template podemos hacer uso de tantas variables de Jekyll como queramos. Aquí os dejo un [listado bastante completo](https://jekyllrb.com/docs/variables/).

## Variables y configuración inicial

Las variables SEO principales que podemos configurar son las siguientes:

-   Título
-   Description
-   URL canónica
-  Etiqueta idiomática
-   Datos estructurados JSON-LD
-   URLs siguiente y anterior
-   Open Graph (título, descripción, URL e imagen)
-   Metadatos para la tarjeta de Twitter

Si no especificamos nada, por defecto Jekyll ya incluye los valores estándar utilizando el título y la desccripción que tenga cada documento. Aún así, recomiendo siempre utilizar el mismo bloque de configuración para asegurarnos de que hacemos uso de todos los elementos SEO disponibles.

Para ello, al principio de cada bloque, yo utilizo el siguiente esquema:

```
---
title: Optimización SEO en Jekyll
description: Guía completa para optimizar el SEO en Jekyll
lang: es_ES
author: Emirodgar
tags: SEO, Jekyll
date: 08/04/2019
image: https://emirodgar.com/cdn/images/og/og-seo-tools.jpg
permalink: optimizacion-seo-jekyll

---
```

Para no repetir una y otra vez la información que es común a todas las páginas, podemos [crear colecciones](http://jekyll.github.io/jekyll-seo-tag/advanced-usage/#author-information). Por ejemplo, para el autor, bastará con crear un archivo específico con toda la información (nombre, perfiles sociales, imágen, etc.) e invocarlo tal como lo he especificado en el ejemplo anterior: ```author:Emirodgar```

De esta forma nos aseguramos que cualquier URL cuenta con la información mínima necesaria para que Google indexe y posicione de forma correcta.

> Los datos estructurados de Jekyll están bastante limitados por lo que recomiendo [este artículo](http://aramzs.github.io/jekyll/schema-dot-org/2018/04/27/how-to-make-your-jekyll-site-structured.html)  para poder profundizar en esta línea y conseguir un marcado semántico mucho más consolidado.
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE1MzgyMDg3NTIsMjAyNTg3NjU2Nl19
-->