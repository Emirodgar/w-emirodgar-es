---
title: Flujos de trabajo en sistemas multi-agente, por qué la arquitectura importa más que el modelo
description: Un modelo líder que escribe el plan, cientos de agentes que lo ejecutan en paralelo, un presupuesto con tope y agentes escépticos que filtran errores. Repasamos esta arquitectura de flujos de trabajo dinámicos y qué enseña a quien diseña sistemas agénticos.
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
author: Emirodgar
lang: es_ES
sitemap: 1
feed: 1
date: 2026-11-10
folder: ia
permalink: arquitectura-flujos-trabajo-agentes-ia
---

# Flujos de trabajo en sistemas multi-agente, por qué la arquitectura importa más que el modelo

Cuando un sistema de [agentes de IA](https://emirodgar.es/agentes-de-ia) falla en una tarea grande, lo habitual es culpar al modelo: que si no es lo bastante listo, que si alucina, que si hay que esperar a la siguiente versión. Para mí, muchas veces el problema es otro: **cómo está organizado el trabajo**. Un modelo excelente metido en un flujo mal diseñado seguirá chocando con los mismos muros. Os cuento una arquitectura que ataca justo eso y lo que se puede aprender de ella.

## Los tres muros de siempre

Los sistemas con un solo agente, o con una cadena rígida de pasos, se estrellan casi siempre contra lo mismo:

- **El cuello de botella.** Un agente que procesa las tareas una por una tarda lo que tarda la suma de todas. Si hay mil documentos que revisar, hay mil turnos en fila.
- **El límite de memoria o contexto.** Cuanto más trabajo acumula un agente, más se le llena la ventana de contexto y más se degrada lo que recuerda del principio.
- **La rigidez.** Una tubería programada de antemano sirve para el caso que previó su autor. Cuando la tarea cambia de forma, hay que reescribirla.

Tiene sentido pararse en el tercero, porque es el menos obvio. Una pipeline fija es fácil de auditar, pero no se adapta. Un agente que decide todo sobre la marcha se adapta, pero es difícil de controlar y de presupuestar. La arquitectura que sigue intenta quedarse con lo mejor de cada lado.

## La idea central: que el líder escriba el plan

En lugar de ejecutar tareas, un modelo "líder" lee un resumen breve del proyecto (una *fact sheet*) y escribe un **plan de acción en forma de script de Python restringido**. Ese script es el que se ejecuta después, coordinando a cientos de agentes trabajadores en paralelo.

Lo importante es la separación. El modelo más capaz no hace el trabajo pesado: lo **planifica**. Los trabajadores, más baratos y numerosos, lo ejecutan. Y como el plan es código y no una conversación, se puede leer, validar, repetir y detener. Un plan escrito es mucho más fácil de supervisar que una cadena de decisiones improvisadas.

## Las cuatro piezas que lo sostienen

### Libro mayor de respuestas (Answer Ledger)

Es una caché que guarda el resultado de cada petición al modelo. Sirve para dos cosas: **reanudar tras un fallo** sin empezar de cero y **no pagar nunca dos veces por la misma consulta**. Parece un detalle de ingeniería, pero cuando se lanzan cientos de agentes, un fallo a mitad de camino es cuestión de cuándo, no de si. Sin esta pieza, cada caída es una factura doble.

### Tiempo de ejecución y presupuesto (Runtime & Budget)

Un entorno que ejecuta el plan abriendo hilos en paralelo bajo un **presupuesto de créditos unificado**. Incluye un tope de gasto: si se alcanza, el trabajo se pausa hasta que un humano lo apruebe. Es el mismo principio de permisos mínimos y límites de gasto que ya comentábamos al hablar de los [navegadores con IA](https://emirodgar.es/navegadores-ia), llevado al nivel de arquitectura. El control no depende de que el agente "se porte bien": está en el propio sistema.

### Validación del plan (Restricted Plan Language)

El código que genera el líder no se ejecuta sin más. Pasa primero por una **lista blanca** que solo permite las operaciones previstas y después por un **simulacro gratuito (dry run)** que estima coste y viabilidad antes de gastar saldo real. Es la respuesta directa a uno de los riesgos que más se repiten cuando se habla de [peligros de la IA](https://emirodgar.es/peligros-ia): un agente con privilegios de más y sin trazabilidad. Aquí el plan puede equivocarse, pero no puede salirse del carril.

### Kit de auditoría (Audit Kit)

Divide el trabajo en fragmentos (*shards*) para repartirlo entre los trabajadores y añade agentes **escépticos**: revisores que examinan los errores encontrados y los someten a votación para descartar falsos positivos. Es un buen recordatorio de algo que se olvida a menudo: un agente que busca fallos tiende a encontrarlos, existan o no. Hace falta otro que dude de lo que el primero afirma.

## Qué se puede aprender, tengas cien agentes o uno

No hace falta montar una flota para aprovechar las ideas. Estas son las que me parecen más trasladables:

1. **Separa planificar de ejecutar.** El modelo caro decide qué hacer; los baratos lo hacen.
2. **Haz que el plan sea un artefacto revisable**, no una conversación que se pierde.
3. **Guarda todo lo que ya has pagado.** Caché y reanudación desde el primer día.
4. **Pon el tope de gasto en el sistema**, no en la buena voluntad del agente.
5. **Simula antes de ejecutar.** Un dry run barato evita sorpresas caras.
6. **Mete a alguien que dude.** La verificación cruzada es lo que baja los falsos positivos.

Sobre todo esto conviene hacerse una pregunta honesta: ¿cuánto de lo que llamamos "fallo del modelo" es en realidad fallo del diseño? La [paradoja de la productividad de la IA](https://emirodgar.es/la-paradoja-de-la-inteligencia-artificial-y-la-productividad) tiene mucho de esto: se compra la herramienta y no se rediseña el proceso alrededor.

## Qué significa para una empresa

Para quien dirige, el mensaje es práctico. Elegir las [herramientas de IA](https://emirodgar.es/herramientas-ia-empresas) importa, pero lo que decide si un sistema agéntico da resultados es el flujo de trabajo: quién planifica, quién ejecuta, quién revisa y quién puede parar la máquina. Es el tipo de decisión que le toca a un [Chief AI Officer](https://emirodgar.es/chief-ai-officer) o, en su defecto, a quien lidere la adopción, y es una de las diferencias entre usar IA y ser una [empresa IA first](https://emirodgar.es/empresas-ia-first). Y si los agentes tienen que conectarse a datos y herramientas externas, el [MCP](https://emirodgar.es/mcp) es hoy la forma ordenada de hacerlo.

Una cautela: es una arquitectura, no una receta mágica. Un plan generado por un modelo puede ser coherente y estar mal planteado, y el dry run estima costes, no garantiza que la tarea tenga sentido. La supervisión humana sigue siendo la última capa. Si algún término de la publicación se os ha quedado en el aire, lo tenéis en el [glosario de IA](https://emirodgar.es/glosario-ia).

## Conclusiones

- Los fallos de los sistemas agénticos suelen venir de la arquitectura antes que del modelo.
- Un líder que escribe un plan restringido y trabajadores que lo ejecutan en paralelo resuelven a la vez el cuello de botella y el límite de contexto.
- Caché, presupuesto con tope, validación previa y auditoría escéptica son las piezas que hacen que escalar sea controlable.
- Diseñar el flujo de trabajo es decidir quién hace qué, quién lo revisa y cuándo se frena. Ese diseño es lo que separa un sistema que escala de uno que solo gasta más.
