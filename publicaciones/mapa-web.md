---
title: Mapa web
description: 
lang: es_ES
image: https://emirodgar.com/cdn/images/og/marketing-digital.png
permalink: mapa

---

# Mapa web

Toda página web que se precie debe tener un **mapa web** para poder organizar los contenidos y facilitar la navegación de sus usuarios.


## Política y sociedad

---

### Política

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder == "politica" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>



### España

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder == "espana" or page.folder == "analisis" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>



### Europa

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder== "europa" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>



### Geopolítica

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder== "geopolitica" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>

---

## Elecciones y datos electorales

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

## Inteligencia Artificial y Tecnología

### Actualidad

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder== "ia" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>

### Formación

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder== "formacion" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>

### Guías y conceptos clave

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder== "guias" or page.folder == "conceptos" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>


---

## Proyectos

<ul>
{% for page in site.pages %}
{% if page.title != null  %}
	{% if page.folder== "proyectos" %}
	  <li><a href="{{ page.url }}">{{ page.title }}</a></li>
	{% endif %}
{% endif %}
{% endfor %}
</ul>

---




