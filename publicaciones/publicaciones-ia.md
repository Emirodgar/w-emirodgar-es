---
title: Publicaciones sobre Inteligencia Artificial
description: "Publicaciones sobre inteligencia artificial: agentes, LLM, riesgos, empleo y aplicaciones en empresa y administración pública, ordenadas de la más reciente."
lang: es_ES
author: Emirodgar
image: 
schema: CollectionPage
permalink: publicaciones-inteligencia-artificial

---

# Publicaciones sobre Inteligencia Artificial

> Si buscas una visión ordenada para el sector público, empieza por la [guía de IA en la administración pública](https://emirodgar.es/guia-ia-administracion-publica).

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder== "ia" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>
