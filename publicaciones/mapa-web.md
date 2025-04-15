---
title: Mapa web
description: 
lang: es_ES
layout: emirodgar_post
image: https://emirodgar.com/cdn/images/og/marketing-digital.png
permalink: publicaciones

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
-
<ul>
{% for post in site.posts %}
{% if post.title != null  %}
	  <li><a href="{{ post.url }}">{{ post.title }}</a></li>
{% endif %}
{% endfor %}
</ul>


