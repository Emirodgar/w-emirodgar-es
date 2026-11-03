---
title: Cómo preparar tu web para agentes de IA, dónde fallan hoy y qué corregir
description: Los agentes de IA ya usan las webs como las usan las personas y fallan donde la interfaz es ambigua. Repasamos los seis puntos de fallo y un plan de cuatro fases para corregirlos.
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
author: Emirodgar
lang: es_ES
sitemap: 1
feed: 1
date: 2026-11-03
folder: ia
permalink: web-para-agentes-ia
---

# Cómo preparar tu web para agentes de IA, dónde fallan hoy y qué corregir

Durante años, una web se diseñó para personas y se hizo descubrible para los rastreadores. Ahora hay un tercer visitante: el [agente de IA](https://emirodgar.es/agentes-de-ia) que no solo lee la página, sino que la **usa**: hace clic, rellena formularios y trata de completar una tarea. Y falla en sitios que a una persona le parecerían evidentes. La consultora MERJ ha pasado desde noviembre de 2025 probando cómo se comportan estos agentes y ha publicado [su investigación](https://merj.com/blog/agent-interaction-research) (29 de septiembre de 2026). Estas son las conclusiones que más importan a quien tiene una web.

## Un visitante que no es persona ni bot clásico

Un agente de navegador entra con un navegador real, ejecuta tu JavaScript, acepta cookies y se mueve como un usuario. No rastrea para un índice, intenta completar un objetivo concreto. Eso rompe dos supuestos habituales:

- **Es difícil de identificar.** Puede llegar desde un chat sin referrer, desde un navegador que una persona controlaba minutos antes o desde una IP de centro de datos. Si ejecuta la analítica, puede colarse en embudos y experimentos y distorsionarlos.
- **Cuando falla, nadie avisa.** Una persona abandona el carrito y, con suerte, te escribe. Un agente que falla no abre un ticket ni deja una línea en el log.

Esto es distinto de preguntarse si te pueden rastrear (robots.txt, cortafuegos, como vimos en las [huellas digitales de los robots](https://emirodgar.es/huellas-digitales-robots)) o si tu página se renderiza. La cuestión nueva viene después: el agente ha llegado y la página está cargada, pero ¿puede usarla?

## Cómo "ve" tu página un agente

MERJ distingue tres tipos de agente, categorías analíticas más que fronteras limpias entre productos:

- **Los que leen la estructura**: consumen el HTML y el árbol de accesibilidad, el mismo que usan los lectores de pantalla. Si tu sistema de diseño pinta un botón con un `div`, para ellos no hay nada que pulsar.
- **Los que miran la pantalla**: razonan sobre una captura y actúan por coordenadas, como el Computer Use de Anthropic. Se adaptan mejor a interfaces con poco marcado, pero son más lentos y caros.
- **Los híbridos**: combinan ambos y heredan los fallos de los dos.

La consecuencia es que el tipo de fallo depende de cómo percibe el agente. Un `aria-hidden="true"` sobre un botón visible lo esconde a los primeros y no molesta a los segundos. Un resultado de una prueba, además, vale para una combinación concreta de web, tarea, agente, modelo e idioma, no para "los agentes" en general.

## Los seis puntos donde fallan

El equipo describe el fallo como una tubería con seis etapas:

1. **Percepción**: el agente no ve algo que está ahí. Ejemplos: un lienzo (canvas) sin estructura, mensajes de estado que desaparecen antes de que los lea, o pantallas de carga con esqueletos que confunde con contenido real.
2. **Selección del objetivo**: ve el botón, pero pulsa otro. Pasa con controles muy pequeños y pegados, iconos sin nombre accesible, dos botones que dicen "Aplicar" o capas transparentes que se comen los clics.
3. **Planificación**: elige una secuencia equivocada. Insiste en un botón desactivado, se inventa un correo para cumplir un campo obligatorio o da por terminada la compra en el carrito sin llegar a la confirmación.
4. **Ejecución**: la acción básica no sale. Arrastrar y soltar es de lo menos fiable, igual que los selectores de fecha complejos o las listas con scroll virtual, donde la fila 5.000 ni existe en el DOM.
5. **Recuperación**: no sabe reaccionar a interrupciones. Los banners de cookies a pantalla completa, los pop-ups de newsletter o los saltos de maquetación a mitad de acción bloquearon a los agentes en las pruebas con páginas reales.
6. **Confianza y manipulación**: el texto de la página se convierte en una vía para dar órdenes al agente. Es la inyección de instrucciones (prompt injection) que ya vimos en [los riesgos de los agentes](https://emirodgar.es/agentes-de-ia), y a diferencia de los demás fallos no se arregla solo con mejor accesibilidad: hacen falta permisos mínimos, confirmación en acciones irreversibles y validación en el servidor.

MERJ midió además cómo mejoraban los agentes: el éxito medio en sus pruebas pasó de en torno al 30% en noviembre de 2025 a cerca del 60% en marzo de 2026. Son cifras de un conjunto de pruebas propio y envejecen rápido, así que sirven para ver la tendencia, no para fijar el estado actual.

## El caso del botón Cancelar: una etiqueta falsa pesa más que el diseño

El experimento más ilustrativo es sencillo. Un panel con un botón verde "Guardar" y otro gris "Cancelar", pero con las etiquetas ARIA intercambiadas a propósito. La tarea era guardar el documento. En marzo de 2026, ChatGPT Agent dentro de Atlas pulsó Cancelar primero en 25 de 25 ejecuciones. Claude Computer Use y el agente de Perplexity en Comet fueron directos a Guardar las 25 veces. Computer Use trabaja solo con capturas y no lee ARIA, así que el resultado es el esperable en un agente visual: la diferencia habla más de la forma de percibir que de qué proveedor es mejor.

La lectura de MERJ es que, para los agentes que leen la estructura, una etiqueta incorrecta puede ser peor que no tener etiqueta, sobre todo en controles destructivos. Hay que ser prudente: es una prueba concreta, de hace meses, y de ella no se pueden sacar jerarquías entre modelos. Pero deja una idea útil. Las etiquetas accesibles forman parte de la interfaz ejecutable y hay que comprobar que **dicen la verdad**, no solo que existen. Atlas, por cierto, ya no existe como navegador, como repasamos en [navegadores con IA](https://emirodgar.es/navegadores-ia).

Esto conecta con otra advertencia: las herramientas que dan una nota de "preparación para agentes" comprueban requisitos previos (árbol de accesibilidad bien formado, WebMCP, `llms.txt`), no que un agente complete tu compra o tu reserva. La página del experimento habría obtenido una nota casi perfecta en cualquiera de ellas.

## WebMCP: un carril rápido junto al navegador

Una alternativa a que el agente adivine la interfaz es que la web le diga qué acciones ofrece. Eso propone **WebMCP**, un estándar de navegador aún en construcción, pariente del [protocolo MCP](https://emirodgar.es/mcp):

- Febrero de 2026: Chrome abre una vista previa temprana. Junio: prueba de origen en Chrome 149.
- 25 de agosto de 2026: OpenAI añade soporte en el navegador integrado de la aplicación de escritorio de ChatGPT.
- Septiembre: Vercel suma soporte experimental y Microsoft anuncia que la implementación de Edge está lista para probar.
- El soporte sigue centrado en Chromium: Mozilla mantiene una posición neutral y WebKit se opone formalmente.

Tiene dos APIs, una declarativa que convierte formularios HTML en herramientas que el agente puede llamar y otra imperativa para flujos complejos, y permite marcar cada acción como de solo lectura, de consecuencias importantes o con contenido no fiable. Esas marcas son orientativas: el navegador no las impone. En un benchmark de nekuda, WebMCP completó las 49 tareas entre 2,5 y 7,5 veces más rápido y con un coste por tarea de 3 a 47 veces menor que los agentes que usan capturas o DOM. Es una prueba única en un entorno controlado, no la web abierta, pero apunta en la misma dirección. Y no resuelve la seguridad: un conjunto de herramientas estructurado es también una superficie de inyección.

Esta idea ya aparece en el comercio. Walmart, por ejemplo, ha presentado una pasarela basada en MCP para que los agentes compren sin recorrer su web, como contamos en [navegadores con IA](https://emirodgar.es/navegadores-ia).

## Hoja de ruta en cuatro fases

MERJ ordena el trabajo de lo más duradero a lo más especulativo:

1. **Arreglar la base.** Cambiar `div` y `span` por `button` y `a` reales, dar nombre accesible a cada icono, revisar que ARIA sea veraz (empezando por los controles destructivos y de pago), quitar capas transparentes (revisando el banner de cookies) y tratar los saltos de maquetación en elementos interactivos como un error. Los estados de éxito y error deben ser persistentes, no un aviso de cuatro segundos.
2. **Medir.** Definir tareas concretas ("añadir el producto X al carrito", no "usar la tienda"), registrar agente, modelo, idioma y versión de la web, y mantener las sesiones de pruebas fuera de la analítica.
3. **Subirlo al sistema de diseño.** Si el botón, el modal o el selector de fecha tienen la semántica correcta, la heredan todas las páginas. Y añadir pruebas con agentes a la integración continua para detectar regresiones.
4. **Añadir un carril estructurado donde compense.** Probar WebMCP en acciones claras o de mucho volumen, sin que sea la única vía, protegiendo toda acción destructiva con una confirmación aparte y tratando el contenido de usuarios (reseñas, foros) como un posible canal de inyección.

Los pasos 1 a 3 ayudan a las personas hoy y siguen valiendo aunque WebMCP no cuaje. MERJ insiste además en un matiz: la accesibilidad se hace para las personas, y optimizar etiquetas solo para que un agente rinda más puede acabar empeorando la experiencia de quien usa un lector de pantalla.

## El idioma también cuenta

Un estudio académico citado en la investigación (OmnilingualGAIA2, de 2026) evaluó agentes en diez idiomas y todos rindieron peor fuera del inglés. Hay un caso útil: ante "borra mi contacto de EE. UU." con dos contactos coincidentes, en inglés y en español, donde el artículo y el singular dejan clara la diferencia, el agente pide aclaración. En chino, japonés e indonesio, que no marcan igual el singular, Claude borró ambos en las tres pruebas. Es un caso de un benchmark, no una propiedad general de esos idiomas, pero la recomendación vale para cualquier web con varios mercados: probar cada idioma importante y exigir confirmación cuando la orden sea ambigua.

## Preguntas frecuentes

**¿Entienden los agentes de IA mi web?** Depende del agente y de cómo esté hecha la página. En las pruebas de MERJ los fallos más claros aparecen con controles sin nombre, interfaces que cambian a mitad de acción y banners que tapan la página.

**¿Basta con hacer la web accesible?** Es la mejor base y beneficia a las personas, pero no cubre todo: la planificación, la recuperación de errores y la seguridad frente a instrucciones maliciosas requieren trabajo adicional.

**¿Qué es WebMCP?** Una propuesta de estándar para que una web describa a un agente las acciones que ofrece, en lugar de obligarle a deducirlas de la interfaz. Aún es experimental y con soporte centrado en Chromium.

**¿Cómo sé si un agente puede completar mi compra o reserva?** No lo dice una puntuación de preparación: hay que probar ese recorrido concreto, con el agente, en la versión publicada y en cada idioma en el que vendas.

## Primero lo que ya hacía falta

La mayoría de lo que piden los agentes es lo que ya se debía a los usuarios: HTML con sentido, etiquetas honestas, páginas estables y controles que se puedan manejar con teclado. Si además quieres que te citen y recomienden, el trabajo de contenido está en nuestra guía de [GEO](https://emirodgar.es/geo) y en cómo [medir la visibilidad de marca en IA](https://emirodgar.es/visibilidad-marca-ia). Lo que conviene evitar es la tentación de limitarse a subir una nota de "agent readiness" sin comprobar si un agente termina de verdad la tarea.
