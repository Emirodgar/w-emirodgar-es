---
description: Guía para enteder el funcionamiento de las cookies y el atributo SameSite
lang: es_ES
author: Emirodgar
sitemap: 1
feed: 1
folder: programacion
date: 07/01/2020
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
permalink: cookies-samesite

---


# Cookies SameSite: guía para entender cómo funcionan

Las cookies son, a día de hoy, la forma más utilizada para guardar y mantener información entre un usuario y una o varias páginas web. Éstas se guardan en el navegador (Chrome, Firefox, Edge, etc.) y normalmente se usan para guardar sesiones, preferencias en aplicaciones o seguimiento de analítica web.

Se componen de una clave y de un valor y de unas condiciones que le indican cuándo y cómo se debe utilizar dicha información.

    clave=valor
    nombre=emilio

Con el objetivo de preservar la privacidad de los usuarios, los navegadores han ido evolucionando y siendo más restrictivos a la hora de aceptar cookies.

## Tipos de cookies

Existen dos tipos de cookies: **first**-party y **third**-party.

Aquellas cookies generadas por la página web en la que estamos navegando serán consideradas como *first-party* (ya que son propias de dicha página) y las que correspondan a otra página sobre la que no estamos navegando, serán *third-party*.

## Atributo SameSite

El atributo `SameSite` nace como respuesta a la necesidad de especificar aquellas zonas grises que existen entre los dos tipos actuales de Cookies.

Este atributo puede tener valor `Strict` `Lax` o `None`. También puede no ser especificado ya que no es -a día de hoy- obligatorio.

### Valor SameSite None

Si especificamos el valor como `None` no estamos restringiendo la creación de la cookie  por lo que ésta se generará y almacenará en el navegador en todos los casos. Equivaldría a una **third-cookie**.
En este caso, adicional a `SameSite` tendremos que incluir también el valor `Secure`.

```text
Set-Cookie: nombre=emilio; SameSite=None; Secure
```

### Valor SameSite Strict

Si configuramos la cookie con SameSite `Strict` implicará que la cookie sólo se creará cuando el usuario esté en nuestra página navegando y la URL sea exactamente la misma para la que la cookie ha sido definida, es decir, funcionará como una *first-party* siempre y cuando ya estemos dentro de la web.

Si el usuario accede a nuestra web desde un enlace externo, por ejemplo a través del email o de otra web, la cookie no saltará por no tratarse de una petición inicial lanzada desde nuestro dominio.

Este atributo es ideal para almacenar información de usuarios que estén interactuando de forma consciente con nuestra web (usuarios registrados, aplicaciones interactivas, etc.).

```text
Set-Cookie: nombre=emilio; SameSite=Strict;
```

### Valor SameSite Lax

Si lo que queremos es generar una cookie *first-party* en cualquier escenario (sin limitar el que el usuario ya tenga que estar presente en nuestra web), entonces deberemos usar el valor `Lax`.

Este valor es recomendable para aquellas cookies que afectan a la visualización de la página.

```text
Set-Cookie: nombre=emilio; SameSite=Lax;
```

A modo de resumen, la siguiente imagen refleja de forma sencilla la diferencia entre los diferentes valores de `SameSite`.

<amp-twitter 
  width="375"
  height="472"
  layout="responsive"
  data-tweetid="1214554679620833281">
</amp-twitter>


### Comportamiento por defecto

Las reglas establecidas a día de hoy indican que:

 - Cookies sin atributo `SameSite` equivaldrán a `SameSite=Lax`
 - Cookies con `SameSite=None` tendrán que especificar el atributo `Secure` 

En la página de [SameSite cookie recipes](https://web.dev/samesite-cookie-recipes/) nos dan una serie de consejos adicionales sobre qué tipo de configuración debemos crear para nuestras cookies en función de la situación que tengamos delante.
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTMxMjQ2NDk5NCw2ODY4NzQzMjYsNjE4MD
k0NDMsMjAwMjY3NjQ0OCw2ODc4NDI2LC0xNTgxODIwOTUxLDcz
MDk5ODExNl19
-->