---
title: "Parley con ALIA: ¿IA pública gratuita? Y qué otros modelos abiertos hay"
description: Una pasarela abierta con modelos de pesos abiertos no cuesta licencia, pero tampoco es gratis. Qué aporta ALIA, qué alternativas abiertas existen y qué criterios importan para elegir modelo en la administración pública.
image:
author: Emirodgar
lang: es_ES
sitemap: 1
feed: 1
date: 2026-11-22
folder: ia
permalink: modelos-abiertos-administracion-publica
---

# Parley con ALIA: ¿IA pública gratuita? Y qué otros modelos abiertos hay

Si juntamos una pasarela como [Parley](https://emirodgar.es/parley-ia-institucional-mit) con un modelo abierto como ALIA, ¿tenemos una IA pública, abierta y gratuita? Casi. La parte de "abierta" es cierta. La de "gratuita", solo a medias.

## Qué es abierto y qué no cuesta

ALIA es una familia de modelos del Barcelona Supercomputing Center, financiada con dinero público y publicada con licencia Apache 2.0, una licencia permisiva, en Hugging Face y GitHub. Se puede descargar y ajustar sin pagar licencia. Ahí termina lo gratuito.

Ejecutar un modelo grande con buen rendimiento cuesta:

- **GPU, energía y refrigeración**, si se aloja en infraestructura propia.
- **Personal que lo mantenga**, lo actualice y lo vigile.
- **Consumo por uso**, si se contrata a un proveedor que lo ejecute por ti.

Es lo que cuenta el informe del MIT sobre los modelos abiertos más grandes: pueden dar prestaciones parecidas a las comerciales en muchas tareas, pero exigen clústeres de GPU muy grandes para correr en local. Que no haya licencia que pagar no significa que no haya factura. Lo desarrollo en el [coste real de la IA](https://emirodgar.es/coste-real-ia).

## Lo que aporta ALIA y lo que le falta

Lo que a mí me parece valioso de ALIA es su entrenamiento en castellano y en las lenguas cooficiales, con documentación abierta, y la posibilidad de que una administración lo use sin enviar datos fuera. Para jerga jurídica y administrativa en español es la apuesta con más sentido.

Pero hay que matizarlo con lo que ya conté en [la promesa fallida de ALIA](https://emirodgar.es/alia-promesa-fallida-ia-publica-espana): el uso real ha sido muy bajo y el modelo de 40.000 millones de parámetros es inviable para la mayoría de las pymes y de las administraciones pequeñas. La propia ficha del modelo base en Hugging Face avisa de que no está alineado ni ajustado para seguir instrucciones, así que puede dar salidas inadecuadas. Existe una versión ajustada para instrucciones, pero no he podido comprobar cómo rinde frente a otras. También se anunció un asistente piloto para la Agencia Tributaria, y no he encontrado confirmación de su despliegue ni de sus resultados, así que no lo doy por hecho.

## Si no es ALIA, ¿cuál?

Conviene aclarar que "modelo abierto" tiene grados, y que lo que sigue es un mapa general, no una recomendación. Hay que revisar la licencia concreta de cada versión antes de usarla.

**Europeos**
- **Mistral.** Francesa. Algunos modelos van con licencia permisiva y otros con condiciones, según la versión.
- **EuroLLM.** Iniciativa europea centrada en las lenguas de la UE.
- **Apertus.** Un modelo abierto de las universidades suizas ETH Zúrich y EPFL.

**Internacionales**
- **Qwen.** Familia china con muchos tamaños, desde modelos pequeños a grandes.
- **Llama.** De Meta. Muy extendido y con mucho soporte, pero su licencia tiene condiciones que hay que leer.
- **DeepSeek y GLM.** Potentes en razonamiento y código, y los grandes piden mucho hardware.

Que sea un modelo chino o estadounidense con pesos abiertos no es un problema por sí mismo si se ejecuta en infraestructura propia, porque los datos no salen. Pero en una administración puede serlo en términos de percepción, de contratación pública o de seguridad. Es una decisión de cada organismo.

## Cómo elegir

Yo me quedaría con cuatro preguntas, en este orden:

1. **¿Para qué tarea?** Resumir normativa, redactar pliegos, atender consultas y analizar expedientes no exigen el mismo modelo. Hay que probar con documentos reales y no fiarse de las clasificaciones.
2. **¿Qué idioma y qué contexto?** ALIA parte con ventaja en español administrativo, pero esa ventaja hay que medirla, no suponerla.
3. **¿Qué hardware hay?** Un modelo pequeño o cuantizado cabe en un servidor modesto. Uno enorme, no.
4. **¿Dónde se procesan los datos y con qué licencia?** Esto decide el cumplimiento con el [Reglamento europeo de IA](https://emirodgar.es/reglamento-europeo-ia-act) y con la normativa de protección de datos.

La ventaja de tener una pasarela agnóstica es precisamente que no hace falta acertar a la primera. Se puede empezar con un modelo, medir y cambiarlo.

Gratis es la licencia. Poner la IA a funcionar, no.

## Fuentes

- BSC, ficha de [ALIA-40b en Hugging Face](https://huggingface.co/BSC-LT/ALIA-40b) (licencia y advertencias de uso).
- Xataka, [Pedro Sánchez anuncia el lanzamiento de los primeros modelos de ALIA](https://www.xataka.com/robotica-e-ia/pedro-sanchez-anuncia-lanzamiento-primeros-modelos-alia-asi-ia-publica-abierta-que-impulsa-estado) y [El arranque de ALIA ha sido errático y decepcionante](https://www.xataka.com/robotica-e-ia/arranque-alia-modelo-ia-espanol-ha-sido-erratico-decepcionante-ahora-sabemos-que).
- Informe del comité ad hoc del MIT sobre el uso de la IA (13 de agosto de 2026), apartado 3.3.8.
