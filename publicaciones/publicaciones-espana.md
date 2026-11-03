---
title: Publicaciones sobre la transformación digital en España
description: "Publicaciones sobre la transformación digital en España: datos, análisis y casos de administración, empresa y sociedad, de la más reciente."
lang: es_ES
author: Emirodgar
image: 
schema: CollectionPage
permalink: publicaciones-espana

---

# Publicaciones relacionadas con España, la transformación digital y la inteligencia artificial

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder== "espana" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>
