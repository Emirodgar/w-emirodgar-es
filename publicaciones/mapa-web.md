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

## Análisis

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder== "analisis" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>

---

## Elecciones

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder== "elecciones" %}
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

## España

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder== "espana" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>


---

## Europa

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder== "europa" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>

---

## Inteligencia Artificial

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder== "ia" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>

---




