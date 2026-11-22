---
title: "Parley: la plataforma de IA del MIT y lo que puede aprender una administración"
description: Parley no es un modelo, es la pasarela con la que el MIT da acceso a varias IA bajo sus propias reglas de privacidad y gasto. Cómo funciona, qué límites reconoce el propio MIT y por qué es un patrón útil para la administración pública.
image:
author: Emirodgar
lang: es_ES
sitemap: 1
feed: 1
date: 2026-11-22
folder: ia
permalink: parley-ia-institucional-mit
---

# Parley: la plataforma de IA del MIT y lo que puede aprender una administración

Al hablar del [informe del MIT sobre IA](https://emirodgar.es/informe-mit-ia-educacion) mencioné de pasada Parley, y es la pieza que más me interesa para el sector público. Conviene empezar por aclarar qué es, porque se suele entender mal: Parley **no es un modelo de IA**. Es la plataforma con la que el MIT ofrece a toda su comunidad acceso a varios modelos, comerciales y abiertos, desde un único sitio que controla la propia institución.

## Cómo funciona

Según el anuncio del servicio de informática del MIT (IS&T), Parley se desplegó para toda la institución en marzo de 2026, tras un piloto desde el otoño de 2025. Con lo que he podido comprobar, estas son sus características:

- **Acceso con credenciales institucionales.** Estudiantes, profesorado y personal entran con su cuenta del MIT.
- **Varios modelos detrás de una misma puerta.** Entre ellos hay modelos abiertos como Llama y comerciales de Google, OpenAI o Anthropic. El usuario elige cuál usa.
- **Privacidad por contrato y por diseño.** Lo que se escribe en Parley no se usa para entrenar modelos ni se comparte fuera. Es una diferencia importante: el informe recuerda que en muchas herramientas comerciales la opción por defecto es registrar las sesiones para entrenamiento.
- **Presupuesto por persona.** Cada usuario dispone de hasta 30 dólares al mes en créditos.
- **API.** Desde el verano de 2026 hay acceso por API, para usar la plataforma con herramientas de programación y para que otras aplicaciones se conecten a ella.

No voy a describir más funciones de las que consta que existen. La información pública es la del propio MIT y puede haber cambiado.

## Por qué lo llaman agnóstica de modelo

Es la palabra clave del informe. El comité pide que el MIT mantenga una plataforma "agnóstica de modelo" que no ate a la comunidad a un solo proveedor, y apoya "con firmeza" ese enfoque. La razón es práctica: los modelos cambian y rinden distinto según la tarea. Si la herramienta que usa la plantilla es la pasarela y no el modelo, se puede cambiar el motor sin reformar a nadie ni cambiar de herramienta.

Para una administración esto resuelve tres cosas a la vez:

1. **Dependencia de un proveedor.** No hay que casarse con ninguno.
2. **Privacidad.** Las peticiones pasan por la infraestructura de la institución antes de salir, y es la institución quien fija qué se puede enviar y a qué modelo.
3. **Gasto controlado.** Se pueden poner límites por usuario, y en una administración, por departamento.

## Lo que el propio MIT reconoce que no funciona del todo

Me gusta que el informe no venda Parley como solución cerrada. Menciona tres problemas:

- **El presupuesto se queda corto.** Algunos usuarios consideran que 30 dólares al mes es poco, sobre todo en asignaturas de ingeniería del software.
- **Pagar por tokens sale más caro que una suscripción.** Varios grupos siguen pagando modelos comerciales por su cuenta porque los planes de suscripción subvencionan el consumo respecto al precio por token de Parley.
- **Registrar o no registrar.** Como la plataforma es del MIT, en teoría puede ver cada petición y cada respuesta. El informe pide una política clara sobre qué se registra, cuánto tiempo y quién accede, porque la gente consulta a la IA asuntos de salud o emocionales. Esa tensión entre auditar y respetar la confidencialidad no tiene una respuesta obvia.

Y hay un límite que cuenta el informe y que no conviene olvidar: los modelos abiertos más grandes necesitan clústeres de GPU enormes para funcionar en local.

## Qué se puede trasladar a España

Mi lectura es que el patrón sirve, y la tecnología es lo de menos. Lo que importa es que la administración sea quien decida qué datos salen, qué modelo los recibe y quién paga. Una pasarela propia o contratada a un proveedor europeo, con acceso unificado, cuotas por área y auditoría, permitiría que un ayuntamiento o una consejería usara IA sin que cada funcionario se abra una cuenta personal en un servicio comercial.

Esto es una extrapolación mía. El MIT es una universidad rica y con un servicio de informática potente, y no sé si una administración pequeña podría montarlo y mantenerlo sola. Probablemente la respuesta sea compartirlo entre varias, como ya se hace con otros servicios comunes. Hay herramientas de código abierto similares, como LibreChat u Open WebUI, pero no las he probado en un entorno público y no voy a recomendarlas sin hacerlo.

La pasarela es solo la mitad. Falta decidir qué modelos van detrás, y ahí entra [ALIA y las alternativas abiertas](https://emirodgar.es/modelos-abiertos-administracion-publica). Y la otra mitad es el [coste real de todo esto](https://emirodgar.es/coste-real-ia).

La IA en una administración debería parecerse más a un suministro con contador que a cien suscripciones sueltas.

## Fuentes

- MIT IS&T, [Introducing Parley: MIT's Generative AI Platform](https://orgchart.mit.edu/node/1555) y [Parley API now available to the MIT community](https://orgchart.mit.edu/node/1583).
- Informe del comité ad hoc del MIT sobre el uso de la IA (13 de agosto de 2026), apartados 3.3.7 a 3.3.10: [informe completo](https://bpb-us-e1.wpmucdn.com/sites.mit.edu/dist/d/2418/files/2026/09/AI-Committee-Final-Report-Aug-13.pdf).
