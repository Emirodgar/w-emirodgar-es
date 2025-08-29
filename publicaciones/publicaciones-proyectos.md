---
title: Proyectos e ideas de transformación digital
description: 
lang: es_ES
author: Emirodgar
image: 
permalink: publicaciones-proyectos

---

Proyectos e ideas para mejorar nuestra sociedad a través de la política

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder== "proyectos" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>
