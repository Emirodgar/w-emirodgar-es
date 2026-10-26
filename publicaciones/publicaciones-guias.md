---
title: Guías y conceptos clave
description: "Glosarios, guías prácticas y conceptos explicados de forma sencilla: de la inteligencia artificial a los datos."
lang: es_ES
author: Emirodgar
image: 
schema: CollectionPage
permalink: publicaciones-guias

---

# Guías y conceptos clave

Glosarios, guías prácticas y conceptos explicados de forma sencilla: de la inteligencia artificial a los datos.

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder == "guias" or page.folder == "conceptos" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>
