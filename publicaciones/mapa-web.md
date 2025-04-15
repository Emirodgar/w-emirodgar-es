---
title: Mapa web
description: 
lang: es_ES
image: https://emirodgar.com/cdn/images/og/marketing-digital.png
permalink: mapa

---

# Mapa web

Toda página web que se precie debe tener un **mapa web** para poder organizar los contenidos y facilitar la navegación de sus usuarios.

## <a name="seo"></a> Publicaciones 

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder== "politica" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>



