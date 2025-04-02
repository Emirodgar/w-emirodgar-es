---
title: Comandos de Google para SEO
description: Aprende a utilizar todos los comandos de Google para potenciar el SEO de tu página
lang: es_ES
author: Emirodgar
sitemap: 1
feed: 1
folder: seo, google
date: 09/05/2019
date_modified: 09/05/2020
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
permalink: comandos-google

---

# Comandos de Google para SEO

Google es un gran buscador y como tal nos permite interactuar tanto con las búsquedas como con los resultados de una forma diferente.

Para ello dispone de una serie de comandos específicos que nos ayudarán a encontrar exactamente lo que estamos buscando. Los podemos utilizar directamente desde la barra de navegación de Google.

## 1 - Búsqueda entre comillas

El hecho de entrecomillar una palabra o frase nos ayudará a que ésta esté siempre presente en todos los resultados. Si no aparece tal como lo hemos seleccionado, Google no nos lo mostrará. Ideal para conseguir búsquedas exactas.

```
"auditoría seo" técnica
```

## 2- Buscar dentro de un dominio

Para buscar únicamente dentro de un dominio debemos utilizar el comando site de la siguiente forma:

```
site:emirodgar.com
```

## 3- Búsquedas combinadas

Podemos realizar varias búsquedas combinando elementos. Por ejemplo:

```
"consultor SEO" OR "posicionamiento web"
```

## 4- Buscar términos en la URL

No sólo podemos buscar a través del contenido de una página sino que también podemos limitar los resultados a aquellos que contienen los términos en su URL.

```
inurl:seo
```

## 5- Buscar por tipo de fichero

Si queremos centrar nuestra búsqueda únicamente en un formato específico -por ejemplo PDF o XML- podemos hacer uso del siguiente comando:
```
filetype:pdf
```

## 6- Buscar términos cercanos

Este comando nos ayudará a buscar dos términos relacionados especificando cuán de lejos deben estar. Por ejemplo, si queremos buscar emirodgar + 3 palabras cualquiera + consultor SEO, podríamos usar el siguiente comando:
 
```
"emirodgar" AROUND(3) "consultor seo"
```

Sólo se tendrían en cuenta frases con tres palabras o menos entre ambos términos.

## 7- Excluir términos

En el caso de que queramos buscar un término pero excluyendo todos los resultados que no nos interesen lo podemos hacer utilizando el guión alto "-" justo delante de lo que queremos excluir.
```
Google -analytics
```
En este caso buscaríamos información sobre Google pero excluyendo el producto de Analytics

## 8- Especificar rango de tiempo

Para concretar las búsquedas en un rango de tiempo concreto tan sólo tendremos que especificar las fechas de la siguiente forma:

```
Salamanca before:2018-06-01 after:2016-06-01
```

## Ejemplos para validar el SEO de una página

Aunque existen alternativas que nos ayudarán a [analizar el SEO](factores-seo) de una web de forma más eficiente, podemos hacer uso de estos comandos para llevar a cabo un análisis SEO rápido.

- site:emirodgar.com para ver las páginas que ha descubierto e indexado (desde GSC es más fiable)
- site:emirodgar.com intext:[] para descubrir si se ha indexado contenido que no debería
- site:emirodgar.com intitle:[] para descubrir posibles títulos duplicados
- site:emirodgar.com inurl:http para descubir posible contenido duplicado con la versión no segura
- site:emirodgar.com -www para identificar otros subdominios de los que no estemos al tanto
- site:emirodgar.com filetype:xml OR filetype:pdf OR filetype:txt para identificar posibles ficheros indexados que no sean páginas HTML
-site:emirodgar.com inurl:? para identificar posibles parámetros en las URLs
- site:emirodgar.* -emirodgar.com para encontrar otros dominios adicionales al que estamos optimizando
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTU3ODYzODI2NCw2NjI4MzQxMTFdfQ==
-->