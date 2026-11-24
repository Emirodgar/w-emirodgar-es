---
title: IA física, qué es y qué cambia cuando un modelo como Gemini controla un robot
description: Google presenta Gemini 4 Hydrogen, un modelo rápido que planifica y controla un brazo robótico a partir de una cámara. Qué es la IA física, qué se ha demostrado y qué no.
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
author: Emirodgar
lang: es_ES
sitemap: 1
feed: 1
date: 2026-11-24
folder: ia
permalink: ia-fisica-robots-gemini
---

# IA física, qué es y qué cambia cuando un modelo como Gemini controla un robot

Hasta hace poco, poner a un robot a hacer algo útil era trabajo de especialistas: drivers, calibración, simulador, visión por ordenador y una interfaz, todo a mano. El 17 de noviembre de 2026 Google publicó en su [blog para desarrolladores](https://developers.googleblog.com/gemini-hydrogen-for-robotics/) algo que apunta a otro sitio: un modelo de lenguaje que, con una cámara y un objetivo escrito en lenguaje natural, planifica la tarea, escribe el código de control y maneja un brazo robótico real. Se llama **Gemini 4 Hydrogen**.

Te cuento qué es la IA física, qué ha mostrado Google exactamente y qué conviene no dar por hecho todavía.

## Qué es la IA física

Es el nombre que se da a los modelos de IA que no solo producen texto o imágenes, sino que entienden el espacio y actúan sobre él. Hablamos de reconocer objetos en una escena en 3D, estimar cómo agarrarlos y decidir qué movimiento hacer. Si un chatbot responde, un sistema de IA física **hace**.

La diferencia con un robot industrial clásico es de programación. Un brazo de una fábrica repite una secuencia que alguien programó para una tarea concreta. Aquí el modelo recibe un objetivo y va ajustando lo que hace según lo que ve en la cámara. Es la misma idea de los agentes de IA que ya usan el navegador por ti, pero aplicada al mundo físico.

## Qué ha presentado Google

Según la propia Google, Gemini 4 Hydrogen es la versión rápida y eficiente de la familia Gemini 4, pensada para usarla a diario y no solo para demostraciones. Incorpora el razonamiento espacial de sus modelos de robótica anteriores (Gemini Robotics ER 2) y, según la compañía, los supera en el benchmark público ERQA en tareas como relacionar varias vistas de una escena o razonar sobre trayectorias en 3D.

El dato medible es el de un benchmark de un tercero, [Artificial Analysis Robotics 0.1](https://artificialanalysis.ai/articles/aa-robotics): el modelo controla un brazo real de 6 ejes en ocho tareas cotidianas de mesa, como servir una bebida o meter bloques en una caja. Hydrogen saca **58 puntos**, parecido a su hermano mayor Argon pero con menor coste por token.

Junto al modelo, Google lanzó un plugin de robótica para su entorno de desarrollo Antigravity que agrupa cuatro cosas:

- **Puesta en marcha del robot:** instala drivers, detecta cámaras, calibra el brazo y comprueba que se mueve con seguridad.
- **Simulación:** construye y previsualiza escenas con MuJoCo para probar ideas antes de tocar el hardware.
- **Percepción y control:** usa la comprensión espacial de Gemini para localizar objetos, planificar agarres y controlar el robot en bucle cerrado.
- **Desarrollo de la aplicación:** genera el controlador y la simulación para pasar de la simulación al robot real.

## Qué se ha demostrado

Google enseña cuatro ejemplos. Son demos suyas, pero ayudan a entender el alcance:

1. **Un brazo listo en unos 10 minutos.** Desde un cable USB y una cámara de profundidad, el plugin instala el software, calibra y hace movimientos de prueba. También lo aplican a un brazo de bajo coste y a uno industrial.
2. **Un clasificador de snacks en aproximadamente una hora.** A partir de un boceto en una pizarra, el modelo construye una simulación de una cinta con un brazo que separa productos en cajas, valida la política de agarre y la despliega en el robot real. Los ajustes, como la fuerza de cierre de la pinza, se piden en lenguaje natural.
3. **Una tienda de jabones que prepara sus propios pedidos.** Un desarrollador crea una web de tienda y la conecta a dos brazos que, al entrar un pedido, ponen una caja, recogen las pastillas encargadas y añaden una nota impresa.
4. **Un robot que juega al ajedrez** contra sí mismo o contra personas.

## Qué no se ha demostrado

Conviene separar el titular de la evidencia:

- **Es un anuncio de la propia Google.** Los benchmarks los mide un tercero, pero las demos y los tiempos de puesta en marcha los cuenta la empresa.
- **Son tareas de mesa.** Servir una bebida o empaquetar bloques no es una cadena de montaje, ni un almacén con miles de referencias ni una cocina.
- **58 puntos no se leen solos.** Google no explica aquí cuántas veces falla el modelo ni cómo se comporta con piezas nuevas. Sin eso no sabemos qué margen de error hay.
- **No hay datos sobre seguridad en entornos con personas.** Que un brazo "se mueva con seguridad" en un banco de pruebas no es lo mismo que trabajar al lado de un operario.

Mi lectura: lo importante es que el **coste y el tiempo de montar** una aplicación robótica baja mucho, no que mañana haya robots así en las fábricas.

## Qué cambia para el empleo y la industria

Aquí hay más preguntas que respuestas, y prefiero decirlo. Si montar una célula robótica pasa de meses a un día, las tareas manuales, repetitivas y de entorno controlado son las primeras expuestas. Esa lectura enlaza con el debate que ya recogí en [la propuesta de Bill Gates de reservar empleos para humanos y gravar a los robots](https://emirodgar.es/bill-gates-riesgos-ia) y con el análisis de [cómo afecta la IA al empleo](https://emirodgar.es/impacto-ia-trabajos) y [qué profesiones están en riesgo](https://emirodgar.es/40-profesiones-en-riesgo-por-la-inteligencia-artificial).

Para una pyme industrial, la pregunta práctica no es si comprar un robot, sino qué tareas de su proceso son repetitivas y estables. Un modelo que planifica solo no arregla un proceso desordenado.

## Cómo probarlo

Según Google, Hydrogen está disponible con el identificador `gemini-4-hydrogen` en la API de Gemini y en Google AI Studio. El plugin de robótica funciona en Antigravity, que es para suscriptores de pago de Google AI Pro o Ultra. Si no tienes un robot, el simulador te permite explorar la parte de control sin hardware.

## Preguntas frecuentes

### ¿Qué es la IA física?
Son modelos de IA que entienden el entorno y actúan sobre él, normalmente a través de un robot. A diferencia de un asistente de texto, producen movimientos y no solo respuestas.

### ¿Hay ya robots así en las fábricas españolas?
No he encontrado datos que lo confirmen. Lo que Google muestra son demos de laboratorio con brazos sobre una mesa, no despliegues industriales.

### ¿Qué es la simulación "real-to-sim-to-real"?
Es construir un gemelo virtual de la escena, probar y validar ahí la tarea muchas veces y desplegar después la política ya verificada en el robot real. Reduce el riesgo de romper cosas o de que algo falle a la primera.

### ¿En qué se diferencia de un robot industrial clásico?
El clásico ejecuta una secuencia programada para un caso concreto. Aquí el modelo parte de un objetivo en lenguaje natural y corrige lo que hace según lo que ve. A cambio, depende de que el modelo acierte, y de eso todavía hay poca evidencia pública.

### ¿Tiene que ver con la AGI?
Es una pieza de la misma carrera: sistemas cada vez más generales, ahora también con cuerpo. Si quieres el marco, lo tienes en [el camino hacia la AGI](https://emirodgar.es/agi).

**Te puede interesar:** [coches autónomos en España](https://emirodgar.es/coches-autonomos), otro caso de IA actuando en el mundo físico, con la regulación como principal freno.
