---
title: Mapa web
description: 
lang: es_ES
image: https://emirodgar.com/cdn/images/og/marketing-digital.png
permalink: mapa

---

# Mapa web

Toda página web que se precie debe tener un **mapa web** para poder organizar los contenidos y facilitar la navegación de sus usuarios.

## Publicaciones 

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder== "politica" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>

---

## Formación

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder== "formacion" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>

---

{% assign politica_pages = site.pages | where: "folder", "politica" %}
{% assign politica_pages_sorted = politica_pages | sort: "date" | reverse %}

<ul>
  {% for page in politica_pages_sorted %}
    {% if page.date %}
      <li>
        <a href="{{ page.url }}">{{ page.title }}</a> - {{ page.date | date: "%Y-%m-%d" }}
      </li>
    {% endif %}
  {% endfor %}
</ul>





