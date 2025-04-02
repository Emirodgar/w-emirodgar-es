---
description: Podemos hacer uso de múltiples templates para colorear nuestro código
lang: es_ES
author: Emirodgar
sitemap: 1
feed: 1
folder: jekyll
date: 02/03/2020
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
permalink: colorear-codigo-jekyll

---

# Colorear el código con markdown en Jekyll

Cuando hacemos uso de `Jekyll` y `Markdown` suele ser frecuente que incluyamos pequeños fragmentos de código eventualmente.

Por norma general, para poder incluir código fuente lo hacemos de la siguiente manera.

````
```html
<meta http-equiv="X-UA-Compatible" content="chrome=1">
   <link rel="icon" href="https://emirodgar.com/cdn/images/hash.png">
```
````
Básicamente indicamos el lenguaje de programación que vamos a utilizar para que sea formatea de forma correcta. 

Por defecto, Jekyll hace uso de [Rouge](http://rouge.jneen.net/) para formatear y colorear hasta **más de 100 lenguajes de programación** facilitando por tanto la lectura y análisis por parte de los usuarios.

> [Listado de los lenguajes soportados por Rouge](https://github.com/rouge-ruby/rouge/wiki/List-of-supported-languages-and-lexers)

En el caso de no especificar uno por defecto, se coloreará con los colores base sin destacar ninguna parte específica.

## Templates para colorear el código fuente

Si queremos modificar los colores predeterminados lo podemos hacer creando un código `CSS` propio o haciendo uso de los [múltiples templates ya existentes](http://jwarby.github.io/jekyll-pygments-themes/languages/python.html).

En este último caso bastará con que seleccionemos el que más nos guste e incorporemos su código en nuestra página.
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTkzNDI3MjkxMF19
-->