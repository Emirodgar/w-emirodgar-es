---
description: ¿Qué validador Javascript es mejor para mis proyectos?
lang: es_ES
author: Emirodgar
sitemap: 1
feed: 1
folder: programacion
date: 10/01/2020
image: https://emirodgar.com/cdn/images/og/marketing-digital.png
permalink: validadores-javascript

---

# Validadores de JavaScript

Un validador nos ayudará a evitar errores a la hora de programar. JavaScript no trae ninguno por defecto pero existen varios que podemos instalar para asegurar que generamos código **claro**, **funcional**, **estándar** y **escalable**.

> El objetivo de un validador es optimizar nuestro tiempo, evitar errores en el código y asegurar una programación estandarizada.

Aunque tengamos experiencia programando podemos pecar de malas prácticas o de generar lenguaje poco funcional lo cuál se traduce en un peor rendimiento. 

## ¿Qué validador puedo usar?

Los más conocidos son [JSLint](http://www.jslint.com/), [JSHint](http://jshint.com/), [JSCS](http://jscs.info/) y [ESLint](http://eslint.org/). Todos ellos funcionan de la misma forma: disponen de un conjunto de reglas con las que validan y garantizan que nuestro código es correcto.

- **JSLint**: es el más antiguo de todos. Personalmente no me gusta debido a que genera demasiados avisos y que la configuración, así como la página de ayuda, no son nada intuitivas. Es demasiado estricto.
- **JSHint**: surge a partir del anterior para solventar, en parte, algunos de los problemas de base. Tiene un buen sistema de configuración y se integra fácilmente con muchos entornos de programación. Podemos especificar y adaptar el validador a nuestras necesidades. Es fácil de usar.
- **JSCS**: en este validador debemos configurarlo desde cero para que se adapte por completo a lo que queremos que nos valide. Es útil para proyectos con un tipo de programación muy específica. Sólo detecta errores en el código pero no variables sin usar u otros aspectos que optimicen nuestra programación.
- **ESLint**: es el más moderno y, aunque viene con una gran documentación, requiere de una configuración inicial. Es muy completo y dispone de muchas integraciones. Posiblemente sea la opción más avanzada, aunque su ejecución puede ser algo más lenta. Yo es el que suelo usar.

## Instalar ESLint

Para poder instalar ESLint recomiendo usar `npm` por lo que antes tendremos que [Node.js](https://nodejs.org/en/) funcionando en el ordenador. Una vez que tengamos disponible `npm` bastará con abrir una consola en Windows y teclear lo siguiente:

```cmd
npm install -g eslint
```

Una vez terminado, iniciamos el validador y después ya podremos optimizar cualquier fichero JavaScript.

```cmd
eslint --init
eslint fichero.js
```

## Integrar ESLint en SublimeText

Por comodidad es preferible integrar el validador con el IDE de programación que utilicemos. En mi caso es SublimeText, aunque prácticamente todos permiten estas integraciones. 

El siguiente paso será instalar el plugin de ESLint en Sublime. Podemos hacerlo desde su [repositorio oficial](https://packagecontrol.io/packages/ESLint) o de forma más rápida directamente desde el editor pulsando `cmd+shift+p`, seleccionando `instalar paquete` y luego `ESLint`.

Una vez instalado, debemos ir al archivo de configuración `Settings-Default` y rellenar los tres campos que aparecen.

```json
{
  "node_path": "C:/Program Files/nodejs",
  "node_modules_path": "C:/Users/Emilio/AppData/Roaming/npm/node_modules",
  "config_file": "C:/Users/Emilio/.eslintrc.json"
}
```

Las dos primeras rutas corresponden a dónde está instalado Node.js en nuestro ordenador. En mi caso es una ruta de Windows. Si usas Linux, tendrás que buscar la adecuada.

ESLint necesita un **archivo de configuración** para comenzar por lo que tendremos que crearlo y asignarlo en `config_file`. Yo suelo usar JSON, en este caso el fichero se llama `.eslintrc.json` pero se pueden usar [otros formatos](https://eslint.org/docs/user-guide/configuring#configuration-file-formats).

Podemos utilizar la configuración básica o personalizarla gracias a su [completa guía](https://eslint.org/docs/user-guide/configuring). En mi caso, el fichero base es el siguiente:
```json
{
    "parserOptions": {
        "ecmaVersion": 6,
        "sourceType": "module",
        "ecmaFeatures": {
            "jsx": true
        }
    },
    "rules": {
        "semi": "error"
    }
}
```

Ahora ya podemos volver a Sublime, navegamos hacia un fichero JavaScript, pulsamos `botón derecho` y seleccionamos `ESLint`. En la consola inferior nos aparecerá el resultado de la validación.
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTUxNjQzNzk3MF19
-->