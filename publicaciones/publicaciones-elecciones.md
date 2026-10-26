---
title: Publicaciones sobre Elecciones en España
description: 
lang: es_ES
author: Emirodgar
image: 
permalink: publicaciones-elecciones

---

# Publicaciones sobre las elecciones en España

> Todo para las generales del 29N (panel, encuestas, programas, test de afinidad y voto por correo) está en el [hub de elecciones](https://emirodgar.es/elecciones/).

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder== "elecciones" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>
