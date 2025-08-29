---
title: Análisis de datos
description: Listado de análisis de datos realizados
lang: es_ES
author: Emirodgar
image: 
permalink: publicaciones-analisis

---

# Análisis de datos de grandes eventos

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder== "analisis" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>
