---
description: Optimiza tu tiempo y automatiza el rendimiento de múltiples URLs dentro de tu sitio web
lang: es_ES
author: Emirodgar
sitemap: 1
feed: 1
folder: programacion
date: 12/11/2019
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
permalink: consola-devtools-chrome

---


# Interactuar con la consola de Google Chrome

En cualquier navegador Google Chrome podemos pulsar la tecla `F12` y automáticamente se nos abrirá un panel a través del cuál podremos analizar lo que ha ocurrido en la web que estamos viendo o incluso podremos interactuar con la misma.

Veamos algunas de las funcionalidades de las que podemos hacer uso. 

## Obtener listado de variables y objetos creados

Si queremos conocer qué variables están disponibles tanto en el entorno del navegador como los asociados a la página o aplicación web, podemos usar los siguientes comandos:

-   `keys(window)`  para ver las variables
-   `dir(window)`  para ver los objetos

Otra posibilidad sería hacer uso directamente del objeto `window.` y navegar por las diferentes opciones que nos ofrece. Desde aquí podremos acceder a todas las variables públicas, tanto del navegador como de la página.

Otra opción sería invocar directamente el objeto `this` para recibir un listado completo de todas las opciones que tenemos disponibles.


## Limpiar la consola

Cuando hay un exceso de mensajes, podemos limpiar la consola de nuestro navegador simplemente haciendo clic con el botón derecho y seleccionando clear console.

También lo podemos hacer a través de código tecleando `clear()`.

> Si en opciones tenemos habilitada la opción de **Preserve log**, el comando `clear()` no funcionará por lo que tendremos que hacerlo a través del menú contextual.

## Usar los logs

A la hora de desarrollar podemos enviar avisos a la consola directamente desde nuestra aplicación. Para ello usaremos los siguientes comandos:

- `console.log("texto")`: para un mensaje normal
- `console.warn("texto")`: para un mensaje de aviso
- `console.error("texto")`: para un mensaje de error


Esto nos va a permitir identificar de forma rápida lo que está ocurriendo en la página.

## Hacer debug

Si hacemos uso de `debugger` podremos probar directamente el código javascript dentro de la consola. También podemos ir directamente a la pestaña Sources y analizar cualquier fichero Javascript para depurar su ejecución.

Google dispone de un [tutorial básico](https://developers.google.com/web/tools/chrome-devtools/javascript?hl=es) pero completo.

## Analizar Google Analytics

Google Analytics tiene una extensión para Chrome llamada [Google Analytics Debugger](https://chrome.google.com/webstore/detail/google-analytics-debugger/jnkmfdileelhofjcijamephohjechhna) a través de la cuál podremos analizar desde la consola de DevTools todo lo que se envía a Google Analytics.

Es ideal para identificar problemas y validar implementaciones de analítica web bajo esta plataforma.

También podemos interactuar directamente con el objeto de Google Analytics para, por ejemplo, obtener el ID de la cuenta:

    ga.getAll()[0].get('trackingId')

En la [documentación oficial de Google Analytics](https://developers.google.com/analytics/devguides/collection/analyticsjs/ga-object-methods-reference) nos explican con mayor detalle cómo interactuar con este objeto.

## Trabajar con la capa de datos

También podemos interactuar de forma directa con la capa de datos. Por ejemplo, el siguiente código lanzará un evento directamente en la página. Si tenemos un listener asociado al mismo podría ver en tiempo real si éste funciona.

    window.dataLayer = window.dataLayer || [];  
    dataLayer.push ({  
    'event': 'erg_contacto'  
    })

## Validar páginas AMP

También podemos usar la consola de Chrome para validar páginas AMP. Para ello bastará con que a la URL le añadamos `#development=1` y recarguemos de nuevo la página.

Por defecto, el mensaje que recibiremos será:

    Powered by AMP ⚡ HTML – Version 1911062056110 https://emirodgar.com/consola-devtools-chrome

Una vez incluido la variable development=1 en la URL recibiremos un valor adicional informándonos de si la versión AMP es válida o si por el contrario ha habido algún error.

    AMP validation successful.

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTIwMTQxNjQyNDgsLTEwNjg5NTcyNCwzMT
YzNDg0MDAsNDI3ODAzOTQ4LC0xMDEwNjYyMTMsLTUxMTY0MTMz
Niw1Njc0NDQzMTMsMTgyMTU4OTMxOCwtNjkxOTk0MjgzLC04Nj
YwMzMxMjFdfQ==
-->