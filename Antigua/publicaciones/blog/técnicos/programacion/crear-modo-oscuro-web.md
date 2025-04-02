---
description: A través de JavaScript y CSS podremos crear un modo oscuro sencillo para nuestra página web
lang: es_ES
sitemap: 1
feed: 1
folder: programacion
permalink: crear-modo-oscuro-web
  
---


# Cómo crear un modo oscuro en una web

Muchas páginas ofrecen la opción a sus visitantes de cambiar la plantilla web y pasar de una versión clara (generalmente blanca) a una oscura. 

¿Cómo podemos crear un modo oscuro para una página web? aunque iba a crear mis propios códigos, he partido de [este tutorial](https://flaviocopes.com/dark-mode/).

## Crear el enlace para cambiar

El primer paso será ofrecer el enlace que permita -a través de JavaScript y el almacenamiento interno del navegador- seleccionar la versión clara o la oscura.

```html
<a href="#" onclick="localStorage.setItem('mode', (localStorage.getItem('mode') || 'dark') === 'dark' ? 'light' : 'dark'); localStorage.getItem('mode') === 'dark' ? document.querySelector('body').classList.add('dark') : document.querySelector('body').classList.remove('dark')" title="Dark/light">Modo oscuro</a>
```

Con este enlace lo que estamos haciendo es seleccionar una versión u otra. 

## Crear el listener para cambiar la clase

Cada vez que hacemos clic en el enlace lo que tenemos que hacer es asignar una clase "clara" u "oscura" a la página web para que de esa forma se cambie el color. Esto lo hacemos estableciendo un `listener` para que obtenga el valor de `localStorage`.

```js
document.addEventListener('DOMContentLoaded', (event) => {
  ((localStorage.getItem('mode') || 'dark') === 'dark') ? document.querySelector('body').classList.add('dark') : document.querySelector('body').classList.remove('dark')
})
```

## Crear los estilos para el modo noche

Ya sólo nos queda establecer qué estilos `CSS` tendrá el modo noche. Dado que lo que hace el `listener` es asignar la clase `dark` al elemento `body` de nuestra página, debemos crear los estilos de la siguiente manera:

```css
body.dark code[class*=language-],
body.dark table tbody>tr:nth-child(odd)>td,
body.dark table tbody>tr:nth-child(odd)>th {
  background: #282c34;
  color:white;
}
body.dark h1,h2,h3,h4 { color:white;}
body.dark .post .post-content p {color :white;} 
```

Los estilos CSS dependerán de cada página web. Los que he puesto antes son los que corresponde a mi blog.

## Resultado final

El modo oscuro que he desarrollado para mi web quedaría de la siguiente manera:

<amp-twitter 
  width="375"
  height="472"
  layout="responsive"
  data-tweetid="1217030590106677253">
</amp-twitter>


<!--stackedit_data:
eyJoaXN0b3J5IjpbMTAxNDI4Mzc4OCwtMTY4NDA5OTAzOCwtMT
c2MDA5Nzg1MF19
-->