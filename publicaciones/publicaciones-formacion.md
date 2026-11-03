---
title: Publicaciones sobre formaciones de inteligencia Aritificial
description: "Publicaciones sobre formación en inteligencia artificial: cursos, competencias y recursos para aprender IA y adaptarte al mercado laboral, de la más reciente."
lang: es_ES
author: Emirodgar
image: 
schema: CollectionPage
permalink: publicaciones-formacion

---

# Publicaciones de formación sobre la inteligencia artificial

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder== "formacion" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>
