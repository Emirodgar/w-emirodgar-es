---
title: Publicaciones sobre Elecciones en España
description: 
lang: es_ES
author: Emirodgar
image: 
permalink: publicaciones-elecciones

---

# Listado de publicaciones relacionadas con las elecciones en España

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder== "elecciones" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>
