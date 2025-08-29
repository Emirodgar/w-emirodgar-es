---
title: Publicaciones sobre la transformación digital en Europa
description: 
lang: es_ES
author: Emirodgar
image: 
permalink: publicaciones-europa

---

# Publicaciones sobre Europa, la transformación digital y la inteligencia artificial

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder== "europa" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>
