---
title: 10 trucos para mejorar las hojas de cálculo de Google (Google Sheet)
description: Saca más provecho a tus hojas de cálculo de Google con estos 10 trucos
lang: es_ES
author: Emirodgar
sitemap: 1
feed: 1
folder: marketing
tags: SEO, Google, excel
date: 26/03/2020
image: https://emirodgar.com/cdn/images/og/herramientas.png
permalink: trucos-hojas-calculo-google

---

# 10 trucos para las hojas de cálculo de Google

Desde que descubrí **Google Apps** soy un fan incondicional de todos sus servicios, en especial de Google Sheets. 

Os explico una serie de trucos para exprimir al máximo y sacar un mayor provecho a las hojas de cálculo de Google.

### Índice de contenidos

 1. [Crea una hoja desde el navegador](#crear-hoja)
 2. [Usa combinaciones de teclas](#combinacion-teclas)
 3. [Traduce a otros idiomas](#traducir-idiomas)
 4. [Importa datos de otras hojas de cálculo](#importar-datos)
 5. [Importa datos desde la web](#importar-datos-web)
 6. [Extiende una fórmula a todo un rango](#formula-rango)
 7. [Normaliza y valida el contenido](#normalizar-validar)
 8. [Haz uso de gráficas de control (sparkline)](#grafica-sparkline)
 9. [Automatiza tareas](#automatizar-tareas)
 10. [Exporta los datos a PDF o JSON](#exportar-datos) 

## <a name="crear-hoja"></a> 1- Crea una hoja desde el navegador

Si estás haciendo uso de Google Chrome (con tu sesión de Google iniciada) batará con que teclées en la barra de direcciones ```sheets.new``` para crear y abrir una nueva hoja de cálculo. Rápido y efectivo.

## <a name="combinacion-teclas"></a> 2- Usa combinaciones de teclas

Si trabajas frecuentemente en hojas de cálculo, el conocer las combinaciones de teclas te ayudará a avanzar mucho más rápido. El [listado de combinaciones de teclas para Google Sheets](https://support.google.com/docs/answer/181110?p=spreadsheets_shortcuts&visit_id=636916984300300429-799695081&rd=1) es bastante amplio así que os dejo las que considero más relevantes:

 1. Insertar enlace (`ctrl` + `k`k)
 2. Quitar formato (`ctrl` + `\`\)
 3. Pegar sólo valores (`ctrl` + `may` + `v`v)
 4. Dar formato de fecha (`ctrl` + `may` + `3`3)
 5. Dar formato de moneda (`ctrl` + `may` + `4`4)
 6. Insertar una nota (`may` + `f2`)
 7. Insertar un comentario (`ctrl` + `alt` + `m`)
 8. Seleccionar todos los datos (`ctrl` + `a`)
 9. Buscar y sustituir (`ctrl` + `h`)
 10. Acceder a una fórmula (`F2`)
 11. Hacer fórmulas multilínea (`ctrl` + `enter`m)

Dependiendo de tu forma de trabajar tendrá sentido usar unas u otras.

## <a name="traducir-idiomas"></a> 3- Traduce a otros idiomas

Si trabajas en varios idiomas bastará con que utilices la función [GoogleTranslate](https://support.google.com/docs/answer/3093331?hl=es) para traducir de forma rápida a múltiples idiomas. Especificamos el contenido a traducir, el idioma de origen y el idioma que queremos obtener de la siguiente forma:

```
=GOOGLETRANSLATE("hola";"es";"en")
```

Si en algún momento tienes dudas acerca del idioma de algún campo puedes hacer uso de la función [DetecLanguage](https://support.google.com/docs/answer/3093278?hl=en) para salir de dudas.

## <a name="importar-datos"></a> 4- Importar datos de otras hojas de cálculo

Es de sobra conocido que podemos integrar información de una pestaña a otra pero Google también nos permite interactuar con información de otras hojas de cálculo a través de la función [ImportRange](https://support.google.com/docs/answer/3093340?hl=es).

```
=IMPORTRANGE("https://docs.google.com/spreadsheets/d/19F`dfgV14";  "Pestaña!A1:A15")
```

Para que esto funcione hay que conectar las hojas una única vez. Cuando utilicemos la función nos solicitará dicho permiso para conectarlas; a partir de ahí podremos importar tanta información como queramos sin ningún impedimento.

## <a name="importar-datos-web"></a>5- Importar datos de otras páginas web

¿Te imaginas poder importar listas de información de otras páginas? es tan sencillo como hacer uso de la función [ImportHTML](https://support.google.com/docs/answer/3093339?hl=es) de la siguiente manera:

```
=IMPORTHTML("https://es.wikipedia.org/wiki/Anexo:Capitales_de_provincia_de_Espa%C3%B1a_por_poblaci%C3%B3n";"table";1)
```

También podríamos importar información desde un [fichero XML](https://support.google.com/docs/answer/3093342) o un [feed RSS](https://support.google.com/docs/answer/3093337).

## <a name="formula-rango"></a>6- Extiende una fórmula a todo un rango

La mayoría de gente suele arrastrar una fórmula por todo el rango donde quiere que funcione. Si hacemos un cambio en la misma tendremos que volver a arrastrar la fórmula una y otra vez. Una opción más eficiente sería utilizar [ArrayFormula](https://support.google.com/docs/answer/3093275?hl=es) para definir -en una única celda- el comportamiento que queramos en dicho rango

```
=ArrayFormula(TRIM(C1:C50))
```

Si decidimos arrastrar una fómula podemos fijar celdas y columnas añadiendo `$` delante del valor. Para hacerlo más sencillo podemos pulsar `F4` cuando estemos en la fórmula y lo añadirá por defecto.

También podrás añadir comentarios a las fórmulas usando `N("comentario")`. Por ejemplo:

    =SUMA(A1:A100) + N("Suma de presupuestos")

## <a name="normalizar-validar"></a> 7- Normaliza y valida el contenido

Para mí hay cuatro funciones básicas que nos ayudarán a que el texto de nuestras hojas de cálculo esté normalizado:

 1. ```Upper```: todo a maýusculas
 2. ```Lower:``` todo a minúsculas
 3. ```Proper```: mayúscula la primera letra de cada palabra
 4. ```Trim```: eliminar espacios en blanco al principio y al final de una cadena

Podemos hacer uso de la función ```trim``` de forma rápida sobre un conjunto de filas y columnas desde el menú "Datos > Recortar datos en blanco".

<amp-img alt="Google sheets trim para eliminar espacios en blanco"
  src="https://3.bp.blogspot.com/-EqUSP926q34/XNLiGUDgLmI/AAAAAAAAH70/2afdGeHJHJ4RbnmL7sONpnN5jse_6FYIACLcBGAs/s640/2.gif"
  width="640"
  height="360"
  layout="responsive">
</amp-img>

Por otro lado, si queremos validar ciertos campos, podemos hacer uso de las funciones por defecto. Las que más utilizo son:

 -  ```ISEMAIL```: para determinar si un campo es un email válido o no.
 - ```ISURL```: para determinar si un campo es una dirección web válida.
 -  ```ESTEXTO```: para determinar si un campo contiene sólo texto.

También podemos eliminar de forma rápida cualquier valor duplicado de la siguiente forma:

<amp-img alt="Google sheets eliminar contenidos duplicados"
  src="https://1.bp.blogspot.com/-rfa43G2hKMM/XNLh5IKw0wI/AAAAAAAAH7w/4LEbkCaIP8MCP21TS6eqYIS1M0q3F_NEwCLcBGAs/s640/1.gif"
  width="640"
  height="360"
  layout="responsive">
</amp-img>


## <a name="grafica-sparkline"></a>8- Haz uso de gráficas de control (sparkline)

El apoyo visual siempre es importante aunque generar gráficos sin un objetivo concreto puede que no aporte nada. Google sheets nos permite crear mini gráficos que se representan en una celda gracias a la función [Sparkline](https://support.google.com/docs/answer/3093289).

Una forma simple y fácil de integrar la parte visual sin perder control analítico.

También podemos añadir **caracteres unicode** haciendo uso de la función `CHAR`. Por ejemplo

- `=CHAR(8594)` sería una flecha hacia la derecha
- `=CHAR(10)` sería una flecha de enter
- `=CHAR(8595)` sería una flecha hacia abajo

> Podemos usar cualquier carácter unicode que aparece en [esta tabla](https://en.wikipedia.org/wiki/List_of_Unicode_characters).

## <a name="automatizar-tareas"></a> 9- Automatiza tareas

A través de [macros](https://support.google.com/docs/answer/7665004?hl=es) podemos crear tareas automatizadas dentro de nuestras hojas sin necesidad de hacerlo nosotros de forma manual. 

> Podemos entender una macro como un conjunto instrucciones listas para ser ejecutadas

Por ejemplo, podemos programar una macro para que todos los días a las 10 importe las últimas noticias del feed de nuestra página favorita. Cuando nos vayamos de vacaciones, seguirá funcionando y a nuestra regreso, la hoja de cálculo estará actualizada con todas las noticias publicadas hasta ese momento.

## <a name="exportar-datos"></a>10- Exporta los datos a PDF o JSON

Tus hojas de datos pueden ser [accedidas desde fuera](https://support.google.com/docs/answer/183965?co=GENIE.Platform%3DDesktop&hl=es) pero tambien podemos exportar su contenido en dos formatos: PDF o JSON.

> En el artículo de [automatizar los análisis de Lighthouse](https://emirodgar.com/automatizar-analisis-lighthouse) expliqué en detalle [cómo hacer pública una hoja para exportar sus datos](https://emirodgar.com/automatizar-analisis-lighthouse#exportar)

Para ello bastará con acceder al siguiente enlace para exportar a PDF:

```
https://docs.google.com/spreadsheets/d/[ID]/export?format=pdf
```

Y al siguiente para hacerlo en formato JSON:

``````
https://spreadsheets.google.com/feeds/list/[ID]/1/public/values?alt=json
``````
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTA2NDE3NTE4LDcyNDcwOTI3NiwtOTI4Mz
czNTI4LDE2NDkwMDUzMjJdfQ==
-->