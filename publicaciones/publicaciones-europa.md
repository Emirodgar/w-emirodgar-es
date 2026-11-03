---
title: Publicaciones sobre la transformación digital en Europa
description: "Publicaciones sobre la transformación digital en Europa: regulación, estrategia de IA y comparativas con España y otros países, de la más reciente a la más antigua."
lang: es_ES
author: Emirodgar
image: 
schema: CollectionPage
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
