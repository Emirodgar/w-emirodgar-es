---
title: Lo fácil que es manipular a la IA, 50.000 estadísticas falsas por 50 dólares y ChatGPT las citó
description: Un investigador de GEO publicó 50.000 estadísticas inventadas en una web nueva. Siete meses después, ChatGPT sigue citándola, más de 330 dominios la enlazan y sus cifras falsas han llegado a un paper y a un informe bancario. Explicamos cómo funciona y qué hacer para no caer.
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
author: Emirodgar
lang: es_ES
sitemap: 1
feed: 1
date: 2026-10-13
folder: ia
permalink: manipular-ia-estadisticas-falsas
---

# Lo fácil que es manipular a la IA: 50.000 estadísticas falsas por 50 dólares y ChatGPT las citó

Hace siete meses, un investigador de GEO publicó una web con 50.000 estadísticas. Todas eran falsas, y nadie las revisó. Hoy Google ha olvidado el sitio, pero **ChatGPT sigue yendo a buscarlo**, decenas de webs reconocidas lo enlazan y sus cifras inventadas han acabado citadas en un artículo académico y en un informe de inversión de un banco. Si alguna vez has pensado que una respuesta de IA con fuente es una respuesta fiable, esta historia debería hacerte dudar.

El experimento lo ha contado [Metehan Yesilyurt, investigador de GEO en Peec AI](https://peec.ai/blog/publish-stats-get-cited-the-tactic-that-put-my-data-all-over-the-web), y conviene leerlo no como un truco de marketing, sino como una prueba de estrés de cómo funcionan hoy los motores de respuesta.

## El experimento: una web, un día y unos 50 dólares

El montaje fue casi trivial. Yesilyurt compró un dominio nuevo, **StateGlobe**, y generó con GPT-4.1 unas **50.000 páginas de estadísticas** sobre SEO, marketing de contenidos, redes sociales, comercio electrónico y tecnología web, desglosadas para 200 países. El prompt era poco más que una lista de países y temas con dos frases de instrucciones. No verificó ni una sola cifra y las publicó con una plantilla web genérica creada también con IA. Después añadió 15.000 listados más. Coste total: **en torno a 50 dólares**.

Esto último es lo importante: no hizo falta dinero, ni un equipo, ni una marca con autoridad. Hizo falta un día de trabajo.

## Lo que pasó después

Los resultados, medidos siete meses más tarde, son difíciles de ignorar:

- **Google lo enterró casi de inmediato.** Tras indexarse bien la primera semana, dos actualizaciones del buscador hundieron su visibilidad y hoy sus páginas indexadas apenas suman entre 5 y 20 impresiones.
- **ChatGPT no se ha ido.** En los últimos 30 días, el sitio recibió más de 600.000 peticiones de bots, y unas **72.000 fueron de ChatGPT-User**, el agente que abre una página en tiempo real para responder a una pregunta de un usuario. No son rastreos de entrenamiento: es ChatGPT consultando una estadística inventada para contestar a una persona real.
- **Más de 10.000 sesiones** llegadas desde ChatGPT según Google Analytics, y más de **330 dominios** que enlazan al sitio, entre ellos grandes marcas como Shopify, DHL o Bluehost.
- En las pruebas de seguimiento de prompts de Peec, StateGlobe llegó a ocupar **el segundo puesto de visibilidad**, solo por detrás de Statista.

## Recuperar no es posicionar

Lo primero que enseña el caso es que **estar bien posicionado en Google y ser recuperable por una IA son dos problemas distintos**. Cuando ChatGPT busca, no copia los diez primeros resultados: reescribe tu pregunta en varias subconsultas, reúne candidatos de sus fuentes y de su propia caché, los reordena y abre unas pocas páginas para apoyar la respuesta. Una página puede ser invisible en Google y salir airosa en cada uno de esos pasos. Es exactamente el patrón que ya veíamos en [qué es el GEO](https://emirodgar.es/geo), donde casi el 90% de las citas de ChatGPT Search procedían de páginas fuera de la primera página de Google.

## Por qué la IA se traga una estadística falsa

El mecanismo, según el autor, es sencillo y tiene tres piezas:

1. **Cada vez más contenido se escribe con IA.**
2. Cuando un modelo redacta, **investiga el tema**, y esa investigación se traduce en subconsultas con palabras como "estadísticas", "datos" o el año en curso. Si le piden un artículo sobre teletrabajo, buscará algo como "estadísticas teletrabajo 2026".
3. Cuando el modelo encuentra un hueco, **busca un número para taparlo**. Una afirmación vaga ("el teletrabajo crece") aporta poco, pero "el X% de los empleados teletrabaja al menos una vez por semana" es concreto, citable y parece evidencia.

Y aquí viene lo incómodo: **nadie comprueba el número**. Un sistema que responde a miles de millones de consultas tiene un presupuesto muy ajustado de tiempo y de coste. Verificar una sola cifra exigiría buscar fuentes independientes, compararlas y resolver contradicciones, algo inviable a esa escala. Los reordenadores que seleccionan los fragmentos puntúan la **relevancia**, no la **verdad**: si un pasaje encaja con la pregunta y suena autorizado, se usa. A eso se suma que una página de estadísticas lleva el año en el título, en los encabezados y en la URL, tres señales de frescura que los modelos premian, un sesgo hacia lo reciente que el propio autor ya había documentado.

Es una versión práctica de lo que ya explicábamos con las [alucinaciones](https://emirodgar.es/glosario-ia): el modelo no sabe cosas, calcula qué es plausible. La diferencia es que aquí ni siquiera inventa él, **hereda la mentira de una fuente que parece seria**.

## El blanqueo de citas: cuando una mentira gana credibilidad

La parte más inquietante no es que ChatGPT cite a StateGlobe, sino lo que ocurrió a continuación. Los datos inventados acabaron:

- citados en un **artículo académico**,
- utilizados en un **informe de inversión del mayor grupo financiero de Catar**,
- recogidos por una **publicación económica india**,
- y usados como fuente en un informe de una comunidad canadiense de influencers.

Y eso solo cuenta las citas que enlazaban de vuelta. El autor da por hecho que muchas más usaron los datos sin enlace.

Llámalo **blanqueo de citas** (*citation laundering*). El primer día, una cifra falsa en un dominio recién estrenado no tenía ninguna autoridad. Después la citó un paper, luego un banco, y ahora el siguiente humano, o el siguiente modelo, que la encuentre verá un número con fuente, y esa fuente la citan instituciones serias. **El dato no se volvió verdadero, pero cada cita lo hizo parecer más fiable.**

Hay un segundo paso aún peor, que el autor solo apunta como esperanza de que no ocurra: con tanta recuperación y tanta cita, esas páginas acaban en los rastreos web, y los rastreos acaban en los datos de entrenamiento. Una cifra que nació como una ocurrencia de GPT-4.1 podría convertirse en algo que el siguiente modelo "sabe". Sería un bucle en el que la IA acaba aprendiendo de contenido que otra IA inventó, y del que además se discute con qué [datos se entrenan realmente estos modelos](https://emirodgar.es/ia-publica-contenido-entrenamiento).

## La prueba de control: con datos reales también funciona

Para descartar que fuese un fallo exclusivo del contenido falso, el equipo de Peec repitió la prueba con una página de estadísticas de GEO **verificadas una a una y con su fuente citada**. Casi de inmediato, webs que sospechan que escriben con IA empezaron a enlazarla. Es decir, la táctica funciona igual con datos reales: lo que cambia es de qué lado de la verdad estás. Y, como recuerda el autor, es una táctica, no una estrategia, y nada garantiza que siga funcionando cuando los modelos cierren este hueco.

## Qué significa para quien crea contenido

El propio estudio ofrece, de rebote, una guía de buenas prácticas para publicar estadísticas **de verdad**, que casa con lo que ya contábamos sobre [cómo medir la visibilidad de una marca en IA](https://emirodgar.es/visibilidad-marca-ia):

- **Una afirmación por frase**, que se entienda sola. La recuperación trabaja con fragmentos, no con páginas enteras.
- **Fuente y año junto a cada cifra** ("según X, 2026"), por el lector, por el modelo y por la credibilidad.
- **Encabezados que imiten las consultas que hacen los modelos**: "[tema] estadísticas", "[tema] tamaño de mercado", "[tema] por países".
- **Fecha de actualización visible y real.**
- **HTML renderizado en servidor**, sin esconder los datos tras JavaScript, pestañas o imágenes, y revisando que el `robots.txt` o el cortafuegos no bloqueen a los bots de IA.
- **Datos originales siempre que puedas**: decir algo que nadie más dice te convierte en fuente primaria.

Y para saber si funciona, no mires solo Search Console, que no ve a estos bots: revisa los registros del servidor o de tu CDN (busca ChatGPT-User, OAI-SearchBot o PerplexityBot), las sesiones de referencia desde chatgpt.com y perplexity.ai en Analytics, y busca tus cifras exactas entre comillas para encontrar menciones sin enlace.

## Qué significa para quien lee (y cita)

Aquí está la lección más importante, y no es para quien publica sino para quien consume:

- **Una respuesta con fuente no es una respuesta verificada.** Que la IA enlace una web solo prueba que la web existe y encajaba con la pregunta.
- **Desconfía de las cifras muy redondas, muy específicas y sin origen primario.** Si una estadística no remite a un estudio, a un organismo oficial o a una metodología, trátala como una hipótesis.
- **Sube por la cadena de citas.** Antes de copiar un dato en una presentación, un informe o un artículo, busca de dónde sale originalmente. Si todos los caminos terminan en una web sin autoría ni metodología, ahí está el problema.
- **Contrasta con dos fuentes independientes** cuando la cifra vaya a sostener una decisión: una inversión, una política pública, un titular.

Es un ejercicio de [truth coping](https://emirodgar.es/truth-coping-afrontar-la-verdad-era-inteligencia-artificial) muy concreto: aprender a convivir con una información que llega pulida, citada y con aspecto de rigor, sin que eso la haga cierta.

## Una vulnerabilidad cara de arreglar

Conviene no sacar la conclusión equivocada. Este experimento no demuestra que ChatGPT sea "malo", demuestra que **verificar a escala es muy caro** y que los sistemas de recuperación están optimizados para ser rápidos y relevantes, no para ser veraces. Es la misma lógica que hace tan eficaz la manipulación en otros terrenos, desde los [deepfakes que ya cuestan 929 millones de euros](https://emirodgar.es/deepfakes-desinformacion-ia) hasta el arte de la [hipnocracia](https://emirodgar.es/hipnocracia): donde la verificación es más cara que la producción, la mentira tiene ventaja.

Y hay un matiz ético que el propio investigador subraya: publicó el experimento como **investigación, no como manual**, y el sitio lleva ahora un aviso. La conclusión que queda no es "inventa datos para que te cite una IA", sino la contraria: **si los modelos premian los números sin preguntarse si son ciertos, la responsabilidad de que sean ciertos recae en quien los publica y en quien los copia.**

*Fuente principal: [Peec AI, "Publish stats, get cited"](https://peec.ai/blog/publish-stats-get-cited-the-tactic-that-put-my-data-all-over-the-web), 7 de octubre de 2026. Las cifras del experimento son las que ofrece el propio autor.*

**Te puede interesar:** [el cuarteto de Anscombe y por qué hay que visualizar los datos](https://emirodgar.es/cuarteto-anscombe).
