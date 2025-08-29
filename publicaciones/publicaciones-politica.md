---
title: Publicaciones sobre política
description: 
lang: es_ES
author: Emirodgar
image: 
permalink: publicaciones-politica

---

# Publicaciones sobre política

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder== "politica" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>
