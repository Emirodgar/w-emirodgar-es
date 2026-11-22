---
title: "El coste real de la IA: económico, humano, organizativo y ambiental"
description: La suscripción es la parte visible. El coste real de la IA incluye el consumo por tokens, la integración, la supervisión humana, la formación, la dependencia de proveedores y la huella ambiental de los centros de datos.
image:
author: Emirodgar
lang: es_ES
sitemap: 1
feed: 1
date: 2026-11-22
folder: ia
permalink: coste-real-ia
---

# El coste real de la IA: económico, humano, organizativo y ambiental

Cuando una empresa o una administración calcula lo que le cuesta la IA, casi siempre suma licencias. Es la parte que se ve en la factura, y creo que es la más pequeña. Esto es lo que habría que sumar.

## Coste económico

La cuota fija de una suscripción es previsible. Lo que se dispara es el consumo. El informe del MIT lo ilustra bien: los planes comerciales más caros llegan a **200 dólares al mes por usuario**, y algunos investigadores gastan **miles de dólares adicionales** al mes en acceso por API, pagando por token, para herramientas de programación. En flujos con varios agentes encadenados el consumo se multiplica, porque cada paso es una nueva llamada.

A eso se suman costes menos visibles:

- **Integración con sistemas heredados**, que casi nunca están preparados para conectarse con una IA.
- **Mantenimiento** de lo que se construye, porque los modelos cambian y lo que funcionaba deja de hacerlo.
- **Dependencia del proveedor.** Si todo tu flujo de trabajo depende de un modelo ajeno, el precio lo marca otro. De ahí el valor de [una pasarela agnóstica como Parley](https://emirodgar.es/parley-ia-institucional-mit).

## Coste humano

Es el que menos se presupuesta. Alguien tiene que revisar lo que produce la IA, porque se equivoca con aplomo, como conté al hablar de la [inteligencia irregular](https://emirodgar.es/bucle-aprendizaje-ia). Esa revisión consume horas, y a veces recae en quien menos lo esperaba: el estudio de Berkeley que conté en la [paradoja de Jevons](https://emirodgar.es/paradoja-jevons-ia) vio cómo los ingenieros acababan revisando el código que otros generaban con IA.

También cuesta formar a la plantilla. El MIT insiste en que no sirve "marcar la casilla" con cursos genéricos de terceros, y que hace falta formación propia, seminarios internos y comunidades donde la gente comparta lo que le funciona. Hablo de ello en [la estrategia de adopción](https://emirodgar.es/estrategia-adopcion-ia-administracion-publica).

Hay otro coste humano más difícil de medir: la [rendición cognitiva](https://emirodgar.es/ia-empleo-ampliar-capacidades). Si un equipo deja de razonar porque delega, se queda sin criterio para detectar cuándo falla la herramienta, y eso se paga más tarde.

## Coste organizativo

La IA no se adopta comprando una herramienta. Exige decidir quién puede usar qué, con qué datos, quién responde de un error y cómo se reparte el acceso. Si solo algunos departamentos pueden pagar los modelos avanzados, se abre una brecha interna. El MIT lo describe como una "incomodidad": estudiantes que pagan 200 dólares al mes frente a otros que no pueden, con ventaja en las tareas que se resuelven en una noche. Una administración tiene el mismo riesgo entre áreas con presupuesto y áreas sin él.

## Coste ambiental

Entrenar y usar modelos consume electricidad y agua en los centros de datos, además de los materiales y la construcción. El informe del MIT lo reconoce, y también que es difícil de cuantificar porque las empresas no publican esos datos. Recomienda que las instituciones informen del coste ambiental y financiero real de lo que usan, por ejemplo mostrando una estimación por modelo, y que auditen su propia huella.

Mi opinión es que este coste suele quedar fuera de la conversación porque no lo paga quien decide. Está muy relacionado con lo que conté sobre la [inversión en centros de datos](https://emirodgar.es/centros-de-datos).

## Qué hacer con esto

Tres cosas, y todas son más baratas que ignorarlo:

1. **Presupuestar por consumo, no por licencia**, con límites por usuario o por área.
2. **Medir qué se obtiene a cambio**, porque sin medir no sabes si compensa.
3. **Poner nombre al coste humano**: horas de revisión y de formación, aunque no salgan en ninguna factura.

La suscripción es el precio de entrada. Lo demás es el precio de que funcione.

## Fuentes

- Informe del comité ad hoc del MIT sobre el uso de la IA (13 de agosto de 2026), apartados 3.3.5, 3.3.7 y 3.3.10: [informe completo](https://bpb-us-e1.wpmucdn.com/sites.mit.edu/dist/d/2418/files/2026/09/AI-Committee-Final-Report-Aug-13.pdf).
- Ranganathan y Ye, [AI Doesn't Reduce Work, It Intensifies It](https://newsroom.haas.berkeley.edu/ai-promised-to-free-up-workers-time-uc-berkeley-haas-researchers-found-the-opposite/), UC Berkeley Haas (febrero 2026).
