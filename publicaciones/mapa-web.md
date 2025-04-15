---
title: Mapa web
description: Página web personal de Emilio. Informático con más de 10 años en Marketing Digital.
lang: es_ES
layout: emirodgar_post
image: https://emirodgar.com/cdn/images/og/marketing-digital.png
permalink: mapa-web

---

# Mapa web

Toda página web que se precie debe tener un **mapa web** para poder organizar los contenidos y facilitar la navegación de sus usuarios.

## <a name="seo"></a> Publicaciones 

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
{% endif %}
{% endfor %}
</ul>


