---
title: Configurar el User ID de Analytics a través de Google Tag Manager
description: Obtén información de tus usuarios de forma más eficiente con la función User ID de Analytics
lang: es_ES
author: Emirodgar
sitemap: 1
feed: 1
folder: analitica
date: 10/10/2019
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
permalink: userid-analytics-tag-manager

---

# Configurar el User ID de Google Analytics a través de Google Tag Manager

Google Analytics utiliza el [ID de cliente](https://developers.google.com/analytics/devguides/collection/analyticsjs/cookies-user-id?hl=es#getting_the_client_id_from_the_cookie) (Client ID) para identificar a los usuarios que acceden a nuestra página web.

> Este valor se almacena a nivel de cookie por lo que si un usuario utiliza varios dispositivos para acceder a nuestro sitio web (móvil, tablet y ordenador) tendremos tres cookies diferentes aún siendo la misma persona.

Para solucionar esta configuración por defecto y poder unificar todas las sesiones de un mismo usuario bajo un mismo identificador, Analytics nos ofrece la opción de utilizar el [ID de usuario](https://support.google.com/tagmanager/answer/4565987) (User ID).  Así define Google el objetivo de esta funcionalidad de Analytics:

> Asociar varias sesiones de usuario y actividades a un ID único, lo que permite obtener un recuento de usuarios más preciso, analizar la experiencia de los usuarios que han iniciado sesión y comprender el comportamiento de estos en todos los dispositivos.

## Paso 1 - Identificar a nuestros usuarios

Dado que se trata de un seguimiento por usuario es requisito indispensable que podamos **identificar de forma única cada visitante de nuestra web**. Para ello, lo normal suele ser generar un ID de usuario cuando se han identificado en nuestro sistema; es decir, necesitamos disponer de un sistema de registro de usuarios.

## Paso 2 - Enviar el ID a la capa de datos

Cuando tengamos un identificador único para cada usuario que ha accedido a nuestro sistema, debemos enviarlo a la capa de datos de la siguiente forma:

```js
<script type="text/JavaScript"> 
  window.dataLayer = window.dataLayer || [];
  dataLayer.push {( 'erg_userID': 'XXXXXX' )} 
</script>

```

Es importante que enviemos la información del identificador del usuario antes del código base de Google Tag Manager.

## Paso 3 - Recuperar el ID en Tag Manager

Ahora debemos recuperar el ID de usuario en GTM para lo cual necesitaremos crear una variable con las siguientes características:

 - **Nombre**: el mismo que hemos utilizado en el envío a la capa de datos. En el ejemplo anterior sería: erg_userID.
 - **Tipo**: variable de capa de datos.

## Paso 4 - Enviar el ID de usuario a Analytics

En la etiqueta de Universal Analytics debemos abrir el panel de "Más opciones > Campos para configurar".

Aquí debemos añadir un nuevo "nombre del campo" que sea userId y cuyo valor referencia a la variable que hemos creado "erg_userID".
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTEzMDg5NTExMDAsLTIzMTQ1NTc1MiwzOD
M4MDMxODQsMjA1MDMxMzY5NCwxNjY5NjcwOTY4LDI0NDA5MzY4
OCwtMTMwMzk5NTU3M119
-->