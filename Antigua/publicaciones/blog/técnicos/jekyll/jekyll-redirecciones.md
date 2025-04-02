---
title: Aplicar redirecciones en Jekyll
description: Aprende a redireccionar tus páginas usando el framework Jekyll
lang: es_ES
author: Emirodgar
sitemap: 1
feed: 1
folder: jekyll
date: 28/06/2019
date_modified: 28/06/2019
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
permalink: redirecciones-seo-jekyll

---

# Aplicar redirecciones en Jekyll

Ya he hablado en alguna ocasión del generador de páginas webs **Jekyll** y [cómo optimizarlo para una estrategia SEO](optimizacion-seo-jekyll).

Ahora vamos a ver cómo se pueden implementar redirecciones de forma sencilla.

## Habilitar el módulo de redirecciones

El primer paso será habilitar en el fichero ```_config.yml``` el plugin asociado a las redirecciones -*jekyll-redirect-from*. Éste nos permitirá utilizarlas dentro del framework; para ello si no tenemos ya creada una sección de plugins, añadimos lo siguiente:

```yml
plugins:  
    - jekyll-redirect-from
```

Si ya teníamos algún plugin cargado, únicamente añadiremos la segunda línea a continuación de los que ya existan en el fichero.

## Aplicar redirecciones 301

Una vez habilitado el plugin, aplicar redirecciones será tan sencillo como incluir los siguientes comandos dentro de las cabeceras de nuestras páginas.

Para redireccionar una URL a otra (tanto interna como externa) debemos utilizar el comando **redirect_to** de la siguiente forma:

```yml
---
title: Redirección 301
redirect_to:
  - http://otra-pagina.com
permalink: /actual/
---
```

Si quisiéramos que otas páginas antiguas redireccionen a la página actual que estamos definiendo, debemos hacer uso de **redirect_from** especificando cada una de las URLs que serán redireccionadas.

```yml
---
title: Redirección 301 de otras URLs a esta página 
redirect_from:
    - /antigua/
    - /otra/antigua/
permalink: /actual/
---
``` 


También podríamos crear un **fichero .htaccess** bajo Jekyll y gestionar las redirecciones a través del mismo, pero creo que esta forma es más rápida y sencilla.
<!--stackedit_data:
eyJoaXN0b3J5IjpbNjYyMjcyMzQ1LC0xOTY0ODM2NzY0XX0=
-->