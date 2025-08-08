---
title: Sistema de monitorización de salud mental en redes sociales - FARO
description: 
image: https://emirodgar.com/cdn/images/og/estrategia-seo.png
author: Emirodgar
lang: es_ES
sitemap: 1
feed: 1
date: 01-08-2025
date_modified: 08/08/2025
folder: proyectos
permalink: faro-monitorizacion-salud-mental
---


# Sistema de monitorización de salud mental en redes sociales

Una de las causas principales de fallecimiento en España son los problemas de salud mental. El auge de las redes sociales y la sensación de que estamos en una sociedad conectada -cuando la realidad demuestra que esa conexión de no es de calidad- ha generado múltiples problemas. 
En nuestro análisis de [Muertes por problemas de salud mental en España: Análisis estadístico y evolución temporal](https://emirodgar.es/muertes-salud-mental) se aprecia claramente la tendencia y evolución al alza, tal como podemos también constatar con la siguiente gráfica.

<img width="2400" class="img-responsive" alt="image" src="https://github.com/user-attachments/assets/02f34088-e495-4e15-8b70-cb9eafd972ca" />

Afortunadamente, una detección temprana de estos síntomas puede ayudar a prevenir las muertes. Con ello en mente he diseñado esta prueba de concepto de un sistema de que nos permita monitorizar y prevenir estas muertes.
Es como la línea de la esperanza (teléfono gratuito al que las personas pueden llamar para recibir ayuda) pero sin que la persona afectada tenga que dar el paso. Analizando mensajes y conversaciones en la red, se podrían identificar casos concretos y ser los especialistas quienes contacten con la persona.

> He desarrollado una versión navegable del dashboard que se puede [ver aquí](https://emirodgar.es/proyectos/faro/).

## ¿Qué es el proyecto FARO?

FARO es un dashboard web diseñado para **identificar comentarios que puedan indicar riesgo suicida en redes sociales**, permitiendo a profesionales de salud mental brindar ayuda temprana y oportuna. Se trata de un proyecto educativo y puramente informacional que ha sido desarrollado como demostración de un posible sistema de monitorización.

<img width="216" height="223" class="img-responsive" alt="image" src="https://github.com/user-attachments/assets/1ab81207-fe2a-483f-8d24-11e558b1e39d" />


## 🎯 Objetivo

Detectar y clasificar mensajes en redes sociales que puedan indicar problemas de salud mental o ideas suicidas, facilitando la intervención temprana por parte de profesionales capacitados.

## 🚀 Características Principales

### Monitorización en tiempo real

- Detección automática de contenido de riesgo
- Clasificación por niveles de urgencia (Crítico, Alto, Medio, Bajo)
- Alertas instantáneas para casos críticos
- Análisis de confianza basado en palabras clave (análisis de lenguaje natural)


  <img width="997" height="557" class="img-responsive" alt="image" src="https://github.com/user-attachments/assets/744a8c04-3d8c-4354-b64d-2c053dc2e3f0" />


### Dashboard Intuitivo
- Resumen ejecutivo con métricas clave
- Vista de alertas en tiempo real
- Gráficos de tendencias y análisis
- Filtros por plataforma y nivel de riesgo


<img width="698" height="296" class="img-responsive" alt="image" src="https://github.com/user-attachments/assets/07651fe5-890e-4612-83c1-6b879f3683c8" />


### Recursos de Ayuda
- Acceso rápido a líneas de crisis
- Protocolos de intervención
- Contactos de emergencia
- Recursos para profesionales


<img width="265" height="493" class="img-responsive" alt="image" src="https://github.com/user-attachments/assets/9e84a71f-ef05-4e25-b4d5-66be438ce8aa" />


### Análisis Avanzado
- Distribución por plataformas sociales
- Tendencias temporales
- Análisis de sentimientos
- Reportes exportables



<img width="1006" height="375" class="img-responsive" alt="image" src="https://github.com/user-attachments/assets/f7e02088-8d48-4d5b-ad07-ea7e800d6e8a" />


## 🚦 Niveles de Riesgo

### Crítico (Rojo)
- Requiere atención inmediata
- Palabras clave: "suicidio", "matarme", "terminar con todo"
- Confianza: 80-95%
- Acción: Contacto directo y escalación

### Alto (Naranja)
- Requiere atención prioritaria
- Palabras clave: "depresión", "sin esperanza", "no puedo más"
- Confianza: 70-90%
- Acción: Revisión y posible contacto

### Medio (Amarillo)
- Monitoreo activo recomendado
- Palabras clave: "triste", "solo", "cansado"
- Confianza: 60-85%
- Acción: Provisión de recursos

### Bajo (Verde)
- Seguimiento rutinario
- Palabras clave: "un poco triste", "día difícil"
- Confianza: 50-75%
- Acción: Monitoreo pasivo

## 🔍 Funcionalidades del Dashboard

### Panel de resumen
- **Alertas Críticas**: Casos que requieren atención inmediata
- **Riesgo Alto**: Casos prioritarios de las últimas 24 horas
- **En Monitoreo**: Casos activos bajo seguimiento
- **Casos Resueltos**: Estadística de casos completados

### Monitor de alertas
- Lista en tiempo real de comentarios detectados
- Información de plataforma, usuario y timestamp
- Nivel de confianza del análisis
- Acciones rápidas por alerta

### Análisis de Tendencias
- **Gráfico por Horas**: Detecciones en las últimas 24 horas
- **Distribución por Plataforma**: Porcentaje por red social
- **Niveles de Riesgo**: Distribución de casos por severidad

### Filtros y Búsqueda
- Filtro por nivel de riesgo
- Filtro por plataforma social
- Búsqueda por palabras clave
- Rango de fechas personalizable


## ⚠️ Consideraciones Importantes

### Privacidad y Ética
- Este es un prototipo para demostración
- En implementación real, se requiere cumplimiento de GDPR/CCPA
- Anonimización de datos personales obligatoria

### Limitaciones Técnicas
- Los datos mostrados son simulados
- El análisis de sentimientos es básico (basado en palabras clave)
- No hay integración real con APIs de redes sociales
- Almacenamiento solo en memoria local

### Recomendaciones de Implementación
- Integrar con APIs oficiales de redes sociales
- Implementar ML/AI para análisis más sofisticado
- Agregar base de datos para persistencia
- Incluir sistema de autenticación y autorización
- Implementar cifrado de datos sensibles

## 🔒 Seguridad y Cumplimiento

### Medidas Recomendadas
- Autenticación multifactor para usuarios
- Cifrado de datos en tránsito y reposo
- Auditoría de accesos y acciones
- Cumplimiento de regulaciones de salud mental
- Protocolos de manejo de datos sensibles

### Aspectos Legales
- Consultar con abogados especializados en privacidad
- Cumplir regulaciones locales de salud mental
- Establecer acuerdos de uso con plataformas sociales
- Implementar políticas de retención de datos

## 👥 Usuarios Objetivo

### Profesionales de salud mental
- Psicólogos clínicos
- Trabajadores sociales
- Consejeros de crisis
- Coordinadores de prevención

### Organizaciones
- Centros de salud mental
- Líneas de crisis y prevención
- Instituciones educativas
- Organizaciones sin fines de lucro

## 📞 Recursos de Emergencia

### España
- **Teléfono de la Esperanza**: 717 003 717
- **Emergencias**: 112
- **Salud Mental**: 061

## 📄 Licencia

Este proyecto es una demostración educativa. Para uso comercial o en producción, se requiere desarrollo adicional y cumplimiento de regulaciones específicas.

