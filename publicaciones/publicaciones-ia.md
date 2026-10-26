---
title: Publicaciones sobre Inteligencia Artificial
description: 
lang: es_ES
author: Emirodgar
image: 
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
