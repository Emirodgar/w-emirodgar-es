---
title: Configuración de Google Analytics y userid tag manager
description: 10 pasos sencillos para abordar de forma efectiva una estrategia de analítica web.
layout: 21_erg
author: Emirodgar
sitemap: 0
feed: 0
folder: analitica2
category: Analítica2
image: https://emirodgar.com/cdn/images/og/analitica.png
cta1title: Planificación estratégica
cta1content: Todos nuestros proyectos se nutren de una excelente planificación
permalink: test2

---

Sí. Dado que se trata de un seguimiento por usuario es requisito indispensable que podamos **identificar de forma única cada visitante de nuestra web**. Para ello, lo normal suele ser generar un ID de usuario cuando se han identificado en nuestro sistema; es decir, necesitamos difgsponer de un sistema de registro de usuarios.

Dado que se trata de un seguimiento por usuario es requisito indispensable que podamos **identificar de forma única cada visitante de nuestra web**. Para ello, lo normal suele ser generar un ID de usuario cuando se han identificado en nuestro sistema; es decir, necesitamos disponer de un sistema de registro de usuarios.

-   **nofollow:** existe desde el 2005 e indica a los buscadores que el enlace no debe ser seguido ni tenido en cuenta para traspasar popularidad. A partir de ahora, podría aportar valor al posicionamiento y a partir de 2020 también al rastreo e indexación. Esto lo decidirá Google.    
-   **sponsored**: nuevo atributo diseñado para etiquetar los enlaces de pago/publicidad. Con esto Google pretende conocer mejor la naturaleza de aquellos enlaces obtenidos a cambio de una colaboración monetaria.     
-   **ugc**: nuevo atributo diseñado para los enlaces que aparezcan dentro de contenido generado por los usuarios (comentarios, foros, etc). De esta forma Google pretender discernir entre los enlaces originales de una publicación y los que han sido añadidos después por usuarios externos.    

Un ejemplo de cómo tendríamos que utilizar estos atributos sería el siguiente:

 ```html     
 <a href="https://emirodgar.com" rel="ugc">Emirodgar</a>
 <a href="https://emirodgar.com" rel="sponsored">Emirodgar</a>
 <a href="https://emirodgar.com" rel="nofollow">Emirodgar</a>
 ```  

En la siguiente imagen podemos ver un esquema de la evolución de los atributos y su impacto en las estrategias SEO. Vale, vale

    

## Conclusiones
  

-   No es obligatorio utilizar ninguno de los atributos. Si no lo hacemos, el enlace servirá para rastrear, indexar y posicionar la página de destino.       
-   Google no recomienda llevar a cabo ningún cambio en el enlazado actual, lo propone más bien para etiquetar de aquí en adelante. También ha dicho que no se esperan grandes cambios en los rankings.       
-   Actualmente ninguno de los tres atributosS sirve para rastrear ni indexar la URL de destino pero queda en manos de Google decidir si suman al posicionamiento web. A partir de marzo de 2020 todas las acciones -rastrear, indexar y posicionar- serán decisión de Google en función de cómo de relevante considere el enlace y la página de destino, independientemente del atributo que tenga el enlace.    
-   Podemos combinar los atributos como queramos, es decir, no estamos limitados a usar sólo uno.  
     


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
eyJoaXN0b3J5IjpbLTI0Nzc5MjAxOCwyMDgyNjQ0NTIyLC05ND
U3ODQ3MTMsNTUwOTI0NzI3LC0xNjEyMDQyMTA4LC0xOTE0MzYw
MzQxLC0yMTE4MjQwNzY1LDU4Mzk0OTM2NywxMjA0NTE2NTA4LC
0xNTY2OTMxMzY0LC01NTc4NjU4NDYsNTgxMTM2MjM1XX0=
-->