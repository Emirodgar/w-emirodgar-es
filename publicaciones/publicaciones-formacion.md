---
title: Publicaciones sobre formaciones de inteligencia Aritificial
description: 
lang: es_ES
author: Emirodgar
image: 
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
