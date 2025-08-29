---
title: Publicaciones sobre Inteligencia Artificial
description: 
lang: es_ES
author: Emirodgar
image: 
permalink: publicaciones-inteligencia-artificial

---

# Publicaciones sobre Inteligencia Artificial

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder== "ia" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>
