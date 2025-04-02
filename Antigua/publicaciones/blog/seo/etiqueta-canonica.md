---
title: Etiqueta canónica
description: 
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
author: Emirodgar
sitemap: 1
feed: 1
folder: seo
lang: es_ES
permalink: etiqueta-canonica

--- 

# Etiqueta canónica

El **contenido duplicado** siempre ha sido un problema para el SEO. Disponer de múltiples URLs para ofrecer el mismo acceso provoca que nuestra estrategia orgánica no esté consolidada y no seamos competitivos.

Si Google encuentra varias URLs duplicadas, **establecerá una de ellas como canónica** (predeterminada) y será ésta la que rastree con mayor frecuencia. Las demás quedarán en un segundo plano y, aunque es posible que sí las rastree, lo más seguro es que no posicionen.

## ¿Qué es contenido duplicado?

A menudo se tiende a pensar que **el contendido duplicado lo generan dos páginas idénticas** pero esto no tiene porqué ser así. Aunque exista diferencia entre el contenido, si no es relevante o es pequeña, Google las considerará como duplicadas y por lo tanto **definirá una como canónica** frente al resto.

## ¿Qué es la etiqueta canónica?

Es la forma que tenemos de indicarle a Google cuál será la página canónica que debe rastrear e indexar con mayor frecuencia delegando a un segundo lugar el resto de posibles duplicadas.

**¿Es necesario que cada página tenga establecida una canónica?** no es necesario pero en ciertos casos sí es conveniente que lo establezcamos para asegurar un rastreo e indexación óptimo de las URLs de valor.

## Beneficios de usar la etiqueta canónica

- Definimos qué URL queremos que sea rastreada e indexada.
- Unificamos enlaces y popularidad en una única URL que mejorará por tanto su posicionamiento web.
- Para facilitar los análisis en plataformas como Google Search Console
- Para ahorrar tiempo de rastreo del robot de búsqueda en páginas duplicadas o con poco valor.

## Cómo implementar la etiqueta canonical

Aunque hay varias formas de indicar a Google que una URL es canónica, la más común suele ser añadir una etiqueta dentro de la cabecera de la página.
 
```html
<link rel="canonical" href="https://emirodgar.com" />
```

También se puede implementar como encabezado HTTP. Si quisiéramos establecer el atributo canonical para algo que no fuera una página web, por ejemplo un PDF, tendríamos que hacer uso de los encabezados HTTP.

```
Link: <http://emirodgar.com/informe.pdf>; rel="canonical"
```

Hay otras opciones como aplicar una redirección 301 (para dejar únicamente una versión o establecerlo a nivel del Sitemap XML.

## Necesitamos más factores

Pero cuidado, la etiqueta canónica puede ser ignorada por Google por lo que, además de usarla, sería neceario apoyarla con otros factores. En [este vídeo de Google Webmasters](https://www.youtube.com/watch?v=8j_hxBw5B4E) explican en qué casos Google podría ignorar la que nosotros hemos enviado y seleccionar otra URL como canónica.

<amp-twitter 
  width="375"
  height="472"
  layout="responsive"
  data-tweetid="1204760229906399232">
</amp-twitter>

Los factores SEO que nos ayudarán a canonicalizar una URL serán:

- Redirecciones
- Enlazado interno y externo
- Sitemaps y hreflang
- URLs amigables y limpias
- HTTPs
- Dominio seleccionado como preferido

Básicamente se trata de ser consistente y ofrecer una visión global que esté alineada con la URL canónica que estamos presentando, si no, Google podría ignorarla completamente.
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTMyNTE2Nzg2NSwtMTA5ODc3MTQ1NywtMT
gzODU0MTA1MywtMjAwMDI5MDQ1OCwtNTE3MDI0NTg3LDY2NDg4
MDQ3M119
-->