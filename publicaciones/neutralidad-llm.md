---
title: Análisis de la neutralidad política en los LLM
description: "Sesgo político de ChatGPT, Claude, Gemini, Perplexity y Llama: qué dicen los estudios, de dónde viene el sesgo en el entrenamiento y qué implica."
image: 
author: Emirodgar
lang: es_ES
sitemap: 1
feed: 1
date: 2025-05-21
date_modified: 2026-11-26
folder: ia
permalink: neutralidad-llm
---

# Análisis de la neutralidad política en los modelos de lenguaje de gran escala (LLM): Sesgo y entrenamiento en la era actual

La investigación a día de hoy revela un patrón consistente de **sesgo político hacia posturas de centro-izquierda** en la mayoría de los LLMs principales. Un [estudio publicado en PLOS One](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0306621) que analizó 24 modelos conversacionales de vanguardia usando 11 pruebas políticas diferentes encontró que la mayoría manifiesta preferencias por puntos de vista progresistas o liberales. Este fenómeno no se limita a un solo modelo, sino que representa una tendencia sistémica en la industria.

### Análisis comparativo de modelos principales

**ChatGPT y GPT-4** muestran un sesgo liberal pronunciado, particularmente en temas como inmigración, aborto, control de armas y políticas económicas redistributivas. Un estudio de 2024 encontró que cuando se le pedía tomar posiciones sobre declaraciones políticas, ChatGPT consistentemente apoyaba posturas progresistas como "Los inmigrantes indocumentados benefician a la sociedad estadounidense" y "El acceso al aborto debería ser un derecho de la mujer".


<img width="961" class="img-responsive" alt="Sesgo político por LLM" src="https://github.com/user-attachments/assets/8f46106a-f350-45d9-8b70-c10cba71c559" />

Este gráfico de barras muestra claramente la distribución del sesgo político entre los principales modelos de lenguaje. Se puede observar que Google Gemini presenta el sesgo liberal más pronunciado, seguido por ChatGPT/GPT-4, mientras que Perplexity es el único modelo que muestra una ligera inclinación conservadora.

**Claude (Anthropic)** también exhibe inclinaciones liberales, aunque menos pronunciadas que ChatGPT. Un análisis comparativo reveló que Claude adopta posiciones de centro-izquierda pero con mayor cautela en sus respuestas.

**Google Gemini** demuestra el sesgo liberal más pronunciado entre los modelos principales. Un estudio multilingüe que evaluó ChatGPT y Gemini en 14 idiomas diferentes encontró que Gemini exhibía "una tendencia liberal y de izquierda más pronunciada comparado con ChatGPT".

**Perplexity** presenta un perfil único, combinando conservadurismo económico con permisividad social, ubicándose como "Libertario Capitalista".

**Meta Llama** muestra resultados variables según el tamaño del modelo. Los modelos más grandes como Llama3-70B tienden a alinearse más estrechamente con partidos políticos de izquierda, mientras que los modelos más pequeños a menudo permanecen neutrales.

### Origen del sesgo en el entrenamiento

#### Datos de Pre-entrenamiento

El sesgo político en los LLMs tiene múltiples fuentes durante el proceso de entrenamiento. Los **datos de pre-entrenamiento** constituyen la primera fuente de sesgo, ya que los modelos se entrenan principalmente con contenido de internet, Wikipedia, artículos académicos y medios de comunicación. Estos datos inherentemente contienen sesgos debido a que:

- **Wikipedia** muestra un sesgo hacia la izquierda en su contenido
- Los **periodistas** en Estados Unidos, Reino Unido y otras naciones occidentales tienden a inclinarse hacia la izquierda del espectro político
- Los **académicos** también tienden, en promedio, hacia posiciones de centro-izquierda

#### Reinforcement Learning from Human Feedback (RLHF)

El **RLHF** representa una fuente significativa de sesgo político. Este proceso utiliza retroalimentación de evaluadores humanos para alinear las salidas de los LLMs con valores humanos, pero inevitablemente incorpora los sesgos políticos de estos evaluadores. Sam Altman, CEO de OpenAI, ha expresado su preocupación específicamente sobre "el sesgo de los evaluadores de retroalimentación humana" y reconoce que los empleados de las empresas de IA afectan el sesgo del sistema.

#### Instruction tuning y alineación

Los procesos de **instruction tuning** diseñados para hacer los modelos más útiles, seguros y no tóxicos pueden inadvertidamente introducir sesgo político. La investigación sugiere que entrenar modelos para comportarse de manera "no prejuiciosa, positiva, no tóxica e incluso precisa" correlaciona con ideales culturales progresistas, llevando a una inclinación política hacia la izquierda.

### Variación por idioma y contexto cultural

Un aspecto particularmente preocupante es que el **sesgo político varía según el idioma** utilizado para consultar al modelo. El estudio multilingüe encontró que estos sesgos políticos difieren dependiendo del idioma de consulta, sugiriendo que los modelos han internalizado diferentes perspectivas políticas asociadas con distintos contextos lingüísticos y culturales.

La investigación indica que el sesgo es **más fuerte en inglés, francés y español**, pero existe en todos los idiomas evaluados. Además, los modelos más grandes acentúan el sesgo y aumentan las similitudes entre predicciones en diferentes idiomas. Este matiz lingüístico recuerda a otro fenómeno que ya analizamos: [cómo la simplificación del lenguaje también condiciona la forma en la que pensamos y debatimos](https://emirodgar.es/por-que-cada-vez-escribimos-y-leemos-frases-mas-cortas).

Esta variación no se limita a la política. Anthropic publicó en julio de 2026 un informe sobre los valores de Claude en los 20 idiomas más habituales, con unas 310.000 conversaciones reales, y observó que el modelo tiende a mostrar más calidez en hindi y árabe y más rigor en inglés y ruso. Y un análisis posterior en *Search Engine Journal* mostró que el idioma también altera **qué marcas recomienda** el modelo: en vuelos de Londres a Tenerife, Claude elegía British Airways en el 52,5% de las respuestas en persa y en ninguna en ruso. Lo desarrollamos en [qué es el GEO](https://emirodgar.es/geo). Los modelos no traducen una respuesta única, razonan y componen cada una en el idioma que reciben.

### Intentos de mitigación y sus limitaciones


<img width="727" class="img-responsive" alt="Respuestas de llms" src="https://github.com/user-attachments/assets/928f1f14-17ac-4924-9ba1-ab05d2c38e3d" />

Esta [visualización comparativa](https://manhattan.institute/article/measuring-political-preferences-in-ai-systems-an-integrative-approach) muestra la distribución de múltiples LLMs en el espectro político, confirmando la tendencia hacia el cuadrante libertario-izquierda que documentan los estudios académicos. La concentración de modelos en esta área del gráfico refuerza los hallazgos del análisis.


#### Constitutional AI (Anthropic)

Anthropic ha desarrollado **Constitutional AI** para Claude, estableciendo un conjunto de principios explícitos basados en fuentes como la Declaración Universal de Derechos Humanos para guiar el comportamiento del AI. Sin embargo, varios estudios han mostrado que incluso con estos principios constitucionales, persiste el sesgo político en ciertas áreas.

#### Políticas de neutralidad (OpenAI)

OpenAI ha implementado políticas de neutralidad declarando que ChatGPT "debería ser objetivo por defecto, especialmente en temas que involucran puntos de vista políticos, culturales o ideológicos en competencia". La empresa ha hecho público su **Model Spec** que establece compromisos con la neutralidad y libertad intelectual. Sin embargo, los estudios empíricos muestran que estos esfuerzos no han eliminado completamente el sesgo observable.

#### Limitaciones inherentes

La investigación sugiere que **entrenar modelos específicamente en datos "verídicos" no elimina el sesgo político**. Un estudio del MIT encontró que incluso los modelos de recompensa entrenados en declaraciones objetivamente verdaderas mantuvieron un sesgo hacia la izquierda, y que este sesgo se incrementa con modelos más grandes.

### Implicaciones para la neutralidad

Los hallazgos plantean preguntas fundamentales sobre si la **neutralidad política verdadera es alcanzable** en los LLMs. Un estudio de 2025 argumenta que "la neutralidad política en la IA es imposible" pero propone formas de lograr mayor equilibrio. Los investigadores sugieren que en lugar de buscar neutralidad absoluta, podría ser más beneficioso tener una **mayor diversidad de perspectivas en los LLMs**. Personalmente es el enfoque que veo más interesa y factible de alcanzar. 

### Consecuencias sociopolíticas

El sesgo político persistente en los LLMs tiene implicaciones significativas dado su creciente uso como fuentes de información. Un estudio de 2024 encontró que la interacción con LLMs sesgados políticamente puede **influir en las preferencias de voto** de los usuarios. Con 935 votantes registrados estadounidenses interactuando con Claude-3, Llama-3 y GPT-4, los investigadores documentaron cambios medibles en las [intenciones de voto](https://emirodgar.es/encuestas-intencion-voto). Este tipo de influencia resulta aún más relevante en un país con un mapa de [ideologías políticas](https://emirodgar.es/ideologias-politicas) tan fragmentado como España.

### Qué pasa cuando se les pregunta por los partidos españoles

Casi todo lo anterior se midió con test políticos o con votantes estadounidenses. En España hay ya datos más cercanos al uso real: el estudio de la UOC y Science4Insights de octubre de 2026 (61 preguntas, seis asistentes, cuatro lenguas, 1.464 respuestas) muestra que **lo habitual es que la IA no se moje**: en el 89,2% de los casos no recomendó ningún partido, y Claude y Gemini lo hicieron solo en dos de 244 respuestas. Grok, en cambio, eligió en el 40,6% y ChatGPT en el 14,3%.

Cuando sí eligen, el PSOE es el más recomendado (23,6%), seguido de Sumar (16,1%) y el PP (15,7%). Pero si se pondera por lo que más preocupa a los españoles, el PP pasa delante (21,8% frente al 20,5% del PSOE), porque las IA lo señalan como mejor opción en economía, paro e inmigración. En inmigración, PP y Vox se llevan cada uno el 29% de las recomendaciones. Es un resultado que **no encaja del todo con la etiqueta de «sesgo de centro-izquierda»**: el sesgo depende de la pregunta, del asistente y de las fuentes que consulta en ese momento.

Que no recomienden no significa que no orienten. ChatGPT ofreció en una de cada cinco respuestas un partido distinto según las prioridades del usuario, y el 87,6% de las respuestas incluía un aviso de imparcialidad que no siempre se cumplía: Grok llegó a decir que no hay un partido objetivamente mejor y, unos párrafos después, que el PP tenía el planteamiento más detallado. Según Lalueza, esa resistencia inicial hace al asistente más persuasivo, porque genera una confianza que no da un amigo del que ya sabes de qué pie cojea.

El contexto de uso explica por qué importa. Según el INE, el 54,8% de los españoles de 16 a 74 años ha usado asistentes de IA en los últimos tres meses, y el 83,3% entre los de 16 a 24 años, que son también quienes tienen el voto menos atado. Ninguna encuesta pública mide todavía cuántos piden consejo electoral a un chatbot y ni OpenAI ni Anthropic publican esa cifra; en las *midterms* de Estados Unidos, la National Conference on Citizenship calculó que en torno a uno de cada cuatro votantes había consultado a una IA sobre algún candidato. Lo cuenta [La Vanguardia](https://www.lavanguardia.com/politica/20261115/11683658/hola-ia-voto.html), y la parte que más nos toca es la última: como el asistente construye su respuesta con lo que encuentra en la web, quien trabaje mejor sus fuentes puede acabar inclinándola. Lo desarrollamos en [el GEO político](https://emirodgar.es/geo).

### Direcciones futuras

La investigación actual se enfoca en desarrollar **mejores métodos de evaluación de sesgo** que reflejen el uso real de los modelos, no solo pruebas políticas artificiales. También se están explorando técnicas como:

- **Entrenamiento contrastivo** con muestras negativas curadas
- **Optimización de preferencias directas** para mitigar sesgos específicos
- **Marcos de detección de sesgo** más sofisticados que pueden identificar sesgos sutiles

La evidencia sugiere que aunque la neutralidad política completa puede ser inalcanzable, es posible desarrollar enfoques más equilibrados y transparentes. El futuro de los LLMs requerirá un enfoque multifacético que combine innovaciones técnicas, supervisión ética y marcos regulatorios apropiados para abordar estos desafíos fundamentales.

Compartimos varias de las fuentes analizadas para este estudio de cara a que se pueda profundizar más:

- https://www.brookings.edu/articles/the-politics-of-ai-chatgpt-and-political-bias/

- https://rais.education/wp-content/uploads/2024/10/0451.pdf

- https://arxiv.org/pdf/2504.06436.pdf

- https://arxiv.org/abs/2504.06436

- https://arxiv.org/abs/2405.13041
