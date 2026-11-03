---
title: Qué son los agentes de IA y por qué son el siguiente salto tras los chatbots
description: Los agentes de IA ya mueven un mercado de 45.000 millones de dólares y el 74% de las empresas planea usarlos. Explicamos qué son, para qué sirven y qué riesgos traen consigo.
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
author: Emirodgar
lang: es_ES
sitemap: 1
feed: 1
date: 2026-09-10
date_modified: 2026-11-03
folder: ia
permalink: agentes-de-ia
---

# Qué son los agentes de IA y por qué son el siguiente salto tras los chatbots

Durante un par de años, "usar IA" significó básicamente escribirle a un chatbot y copiar su respuesta. Eso ya ha cambiado. Lo que está creciendo ahora son los **agentes de IA**: sistemas que no se limitan a responder, sino que planifican, usan herramientas y ejecutan tareas completas por su cuenta. Si el término te suena, pero no tienes muy claro en qué se diferencia de un chatbot normal, esta es la explicación.

## De responder preguntas a ejecutar tareas

Un chatbot recibe una pregunta y devuelve una respuesta. Un **agente de IA** recibe un objetivo, y decide por sí solo los pasos necesarios para cumplirlo: buscar información, consultar una base de datos, ejecutar código, rellenar un formulario o encadenar varias de esas acciones seguidas, sin que un humano tenga que ir dando la instrucción paso a paso. Si necesitas repasar antes los términos básicos, tienes las definiciones en nuestro [glosario de inteligencia artificial](https://emirodgar.es/glosario-ia).

Ejemplo sencillo: en vez de pedirle a una IA "resume estas facturas", un agente puede recibir la instrucción "concilia las facturas del mes y avísame si hay alguna discrepancia", y encargarse él solo de abrir los archivos, cruzarlos con el sistema contable y generar el informe. Ese salto —de responder a actuar— es lo que está detrás de buena parte del entusiasmo (y también de la preocupación) alrededor de la IA en 2026.

## Un mercado que ya es real, no una promesa

El mercado de la IA agéntica alcanzó los **45.000 millones de dólares en febrero de 2026**, y según Gartner, el **74% de las empresas** planea desplegar agentes autónomos en los próximos dos años, cifras recogidas por [El Ecosistema Startup](https://ecosistemastartup.com/agentes-ia-2026-74-de-empresas-los-adoptara-este-ano/). No es un mercado de una sola empresa: **Manus** (agente generalista de uso del ordenador, en la órbita de Meta), **ChatGPT Agent** de OpenAI (heredero de lo que antes se llamaba Operator) y **Claude** de Anthropic, con Claude Code para desarrollo y agentes gestionados para procesos de negocio, concentran buena parte de la conversación.

Por debajo de esas marcas conocidas hay todo un ecosistema de herramientas para construir agentes propios: n8n, CrewAI, LangChain/LangGraph o Microsoft AutoGen, entre otras. Y el estándar que está permitiendo que estos agentes se conecten de forma ordenada con herramientas externas es el [Model Context Protocol (MCP)](https://emirodgar.es/mcp), del que ya hablamos en detalle.

## Dónde se están usando ya

Los casos de uso más citados se concentran en tareas repetitivas con datos estructurados, justo donde un agente aporta más y se equivoca menos:

- **Finanzas**: agentes que monitorizan mercados, generan informes de compliance y optimizan el flujo de caja.
- **E-commerce**: detección automática de productos con bajo rendimiento, tests A/B sin intervención manual y recomendaciones en tiempo real.
- **Logística**: optimización de inventario y de la cadena de suministro sobre datos que cambian constantemente.

La ciencia es otro terreno donde los agentes ya se prueban. Google.org ha repartido **36 millones de dólares entre 17 organizaciones** de su Impact Challenge: AI for Science, elegidas entre candidaturas de 30 países. Entre ellas, el MIT entrena agentes que interpretan de forma autónoma imágenes de microscopía para descubrir materiales, y UC San Diego ha montado una *pipeline* agéntica que extrae física climática de las observaciones de la Tierra y decide dónde conviene recoger nuevas mediciones del océano.

No es casualidad que estos sean los primeros terrenos: son entornos con datos limpios, reglas claras y un margen de error acotado. Justo lo contrario de lo que ocurre, por ejemplo, cuando un agente tiene que moverse en una web abierta o interactuar con un cliente real.

## Los riesgos que conviene no ignorar

Cuanta más autonomía le das a un sistema, menos supervisión humana directa hay en cada paso, y ahí es donde aparecen los problemas. Un informe de la alianza de inteligencia **Five Eyes**, de mayo de 2026, identificó **23 riesgos agrupados en 5 categorías**: privilegios excesivos, diseño o configuración incorrecta, comportamiento no alineado o directamente engañoso, una superficie de ataque más amplia por la cantidad de componentes interconectados, y falta de auditoría y trazabilidad, según recoge [DonWeb](https://blog.donweb.com/agentes-ia-riesgos-seguridad-five-eyes-2026/).

Entre esos riesgos, la **inyección de instrucciones maliciosas (prompt injection)** aparece señalada como la amenaza más difícil de mitigar: un documento, una web o un correo pueden contener texto diseñado para hacer que el agente actúe en contra de lo que le pidió el usuario real. Además, el [International AI Safety Report 2026](https://academiadeia.es/international-ai-safety-report-2026-descargar/) documentó, en evaluaciones sobre modelos tanto de Anthropic como de OpenAI, comportamientos de autonomía y engaño en escenarios cercanos a situaciones reales; la primera vez que se observan con tanta claridad en modelos de este nivel. No es un problema de una empresa concreta, es un riesgo del propio paradigma de "delegar decisiones" a un sistema que puede alucinar, como ya vimos que hacen los [LLM en general](https://emirodgar.es/truth-coping-afrontar-la-verdad-era-inteligencia-artificial).

La recomendación que se repite entre quienes estudian esto es priorizar la resiliencia sobre la velocidad: despliegue incremental, permisos mínimos, registro de cada acción y supervisión humana obligatoria antes de cualquier acción crítica, en vez de dar a un agente las llaves de todo el sistema de golpe.

## Un caso real: Muse, el agente de Meta

Estos riesgos ya no son teóricos. **Muse**, el asistente personal de Meta lanzado el 8 de septiembre de 2026, se ha convertido en un éxito de descargas: millones de personas lo conectan a sus cuentas bancarias, mensajes o datos de salud para que haga tareas por ellas. Y dos noticias recientes muestran las dos caras del problema.

**La privacidad.** Varios investigadores lograron sacar de la propia app las instrucciones internas del agente, algo que Meta dice haber permitido a propósito en aras de la transparencia. Según [WIRED](https://www.wired.com/story/muse-creates-detailed-profiles-of-all-your-friends-and-family/), entre ellas figura la de crear cada hora una "página" por cada persona del entorno del usuario (familia, pareja, amigos, compañeros), con datos como cumpleaños, hechos relevantes, cómo es la relación y sugerencias para reforzarla. Meta defiende que necesita ese contexto para ser útil, que cada usuario tiene su propia máquina virtual aislada, que puede borrar la memoria y que Muse pide confirmación antes de enviar un correo o comprar algo. Aun así, la experta Miranda Bogen señala que estas herramientas piden "enchufar" la vida entera del usuario, y el volumen de lo que saben sobre nosotros (y sobre terceros que nunca aceptaron nada) no deja de crecer. Es el mismo dilema de [permisos mínimos y trazabilidad](https://emirodgar.es/peligros-ia) que mencionábamos arriba, aplicado a un producto de consumo.

**El dinero.** Torsten Sløk, economista jefe de Apollo, ha advertido de una posible "fuga bancaria agéntica": si un agente recibe la orden de "ganar rentabilidad", podría mover los saldos parados en cuentas que pagan un 0,1% hacia depósitos que ofrecen hasta un 5%. Sus cálculos, recogidos por [Yahoo Finance](https://finance.yahoo.com/technology/ai/articles/wall-street-giant-warns-ai-172119618.html), apuntan a que los bancos perderían los depósitos baratos con los que financian sus préstamos. Hoy es un escenario remoto, porque ni Muse ni Dots, de OpenAI, pueden mover dinero. Pero muestra algo que va más allá de la banca: la **inercia del cliente** sostiene el negocio de muchos sectores (seguros, telecos, suministros), y un agente que cambia de proveedor sin esfuerzo la rompe.

## Cuando compra un agente, se rompen modelos de negocio enteros

La fuga bancaria es solo el ejemplo más vistoso. Malte Landwehr, consultor de búsqueda e IA, ha reunido en [34 hipótesis sobre el impacto de los agentes en la economía digital](https://www.maltelandwehr.de/articles/ai-agents-digital-economy/) (28 de octubre de 2026) una idea de fondo: la búsqueda con IA ya movió la decisión de compra de la web al chat, y los agentes la sacan directamente de manos humanas. Eso perjudica a todo negocio que dependa de que el cliente esté ocupado, se olvide o esté mal informado. Él mismo avisa de que algunas hipótesis las ve claras y otras son suposiciones razonadas, así que conviene leerlas como escenarios, no como hechos.

- **Comparadores y metabuscadores, los más expuestos.** Un agente no necesita al intermediario para ahorrar tiempo y, si lo usa, comprobará después el precio en el hotel o la tienda, sin pasar por el enlace de afiliado. Los mercados con muchísima oferta, como hoteles o tiendas online, aguantan algo mejor. En vuelos o coches de alquiler, donde se puede consultar a cada proveedor, el valor del agregador tiende a cero. Los marketplaces que gestionan pago, envío y devoluciones tienen más opciones si se convierten en empresas de servicio.
- **Promociones que solo funcionan porque casi nadie las usa.** El agente reclamará siempre la garantía de igualación de precio, aplicará todos los cupones públicos, perseguirá cada bono de bienvenida de bancos o eléctricas y cancelará las suscripciones que no se usan. Si los miembros inactivos dejan de pagar, gimnasios o plataformas de streaming tendrán que subir precios o pasar a cobrar por uso.
- **Adiós a parte de la publicidad y las ventas adicionales.** Un agente lee toda la lista, no solo los primeros resultados: según una de las fuentes de Landwehr, el 64% de los productos que recomienda Rufus, el asistente de Amazon, no están entre los diez primeros resultados orgánicos de la tienda. Y el seguro que se ofrece en el mostrador del coche de alquiler, con valor esperado negativo para el cliente, no lo comprará nunca.
- **Marcas y fichas de producto.** Los agentes premian la calidad percibida (reseñas, especificaciones, tasa de devoluciones) más que la publicidad de marca, y las fichas se escribirán también para ellos: especificaciones exactas, precios, plazos y condiciones de devolución en un formato que puedan entender. Esto enlaza con lo que contamos sobre [GEO](https://emirodgar.es/geo) y con la guía para [preparar tu web para agentes de IA](https://emirodgar.es/web-para-agentes-ia).
- **Quién decide, quién responde.** Landwehr teme una brecha entre quien paga por un agente que trabaja para él y quien usa uno gratuito, financiado por anunciantes. Y plantea la pregunta que acabarán resolviendo los tribunales: quién responde cuando un agente se equivoca, el usuario o quien creó el agente.
- **Empleo.** Los centros de llamadas, la negociación (concesionarios, inmobiliarias) y las compras B2B de bienes estándar pasarían a ser conversaciones entre agentes. Como contrapartida, aparecerían oficios nuevos como la experiencia de agente (AX, el equivalente a la UX) y las relaciones con agentes.

La conclusión práctica para una empresa es incómoda: Landwehr cree que bloquear a los agentes saldrá caro, y dejar que compren sin condiciones también puede serlo. Dos caminos ya a la vista: el [pleito entre Amazon y Perplexity](https://emirodgar.es/navegadores-ia), que apuesta por el bloqueo, y el de Walmart, que fija permisos y límites de gasto, y que explicamos en esa misma publicación.

## Qué significa esto para una empresa

Antes de adoptar agentes de IA sin más, tiene sentido hacerse tres preguntas: ¿qué tarea concreta quiero delegar, con qué margen de error asumible?, ¿qué permisos mínimos necesita el agente para hacerla, y ni uno más?, y ¿quién revisa sus decisiones antes de que tengan consecuencias reales? Esto conecta directamente con el papel que cada vez más empresas delegan en un [Chief AI Officer](https://emirodgar.es/chief-ai-officer), y con la necesidad de contar con [herramientas de IA para empresas](https://emirodgar.es/herramientas-ia-empresas) bien seleccionadas, no solo las más de moda.

## El chatbot fue el aperitivo

Los chatbots nos acostumbraron a hablar con una IA. Los agentes nos están acostumbrando a que esa IA actúe por nosotros. Es un cambio de categoría, no solo de grado, y como todo cambio de categoría, trae consigo tanto la mayor promesa de productividad de los últimos años como los riesgos más nuevos y menos entendidos. Ambas cosas son ciertas a la vez, y conviene no perder de vista ninguna de las dos.
