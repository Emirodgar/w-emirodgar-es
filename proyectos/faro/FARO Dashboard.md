# FARO Dashboard

**Sistema de Monitoreo de Salud Mental en Redes Sociales**

FARO es un dashboard web diseñado para identificar comentarios que puedan indicar riesgo suicida en redes sociales, permitiendo a profesionales de salud mental brindar ayuda temprana y oportuna.

## 🎯 Objetivo

Detectar y clasificar mensajes en redes sociales que puedan indicar problemas de salud mental o ideación suicida, facilitando la intervención temprana por parte de profesionales capacitados.

## 🚀 Características Principales

### Monitoreo en Tiempo Real
- Detección automática de contenido de riesgo
- Clasificación por niveles de urgencia (Crítico, Alto, Medio, Bajo)
- Alertas instantáneas para casos críticos
- Análisis de confianza basado en palabras clave

### Dashboard Intuitivo
- Resumen ejecutivo con métricas clave
- Vista de alertas en tiempo real
- Gráficos de tendencias y análisis
- Filtros por plataforma y nivel de riesgo

### Recursos de Ayuda
- Acceso rápido a líneas de crisis
- Protocolos de intervención
- Contactos de emergencia
- Recursos para profesionales

### Análisis Avanzado
- Distribución por plataformas sociales
- Tendencias temporales
- Análisis de sentimientos
- Reportes exportables

## 🔧 Tecnologías Utilizadas

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Gráficos**: Canvas API para visualizaciones
- **Diseño**: Responsive design con CSS Grid y Flexbox
- **Iconos**: Font Awesome
- **Tipografía**: Inter (Google Fonts)

## 📋 Estructura del Proyecto

```
faro-dashboard/
├── index.html          # Página principal del dashboard
├── styles.css          # Estilos y diseño responsivo
├── script.js           # Funcionalidad principal e interactividad
├── analytics.js        # Módulo de análisis avanzado
├── assets/
│   ├── faro-logo.png   # Logo del sistema
│   └── references/     # Imágenes de referencia para diseño
├── concepto-diseno.md  # Documentación del diseño
└── README.md           # Este archivo
```

## 🎨 Paleta de Colores

### Colores Principales
- **Azul Profundo** (#1e3a8a): Confianza y profesionalismo
- **Azul Claro** (#3b82f6): Elementos interactivos
- **Gris Neutro** (#6b7280): Texto secundario
- **Blanco** (#ffffff): Fondo principal

### Colores de Estado
- **Verde** (#10b981): Seguro, sin riesgo
- **Amarillo** (#f59e0b): Precaución, riesgo medio
- **Naranja** (#f97316): Alerta, riesgo alto
- **Rojo** (#ef4444): Crítico, riesgo inmediato

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

### Panel de Resumen
- **Alertas Críticas**: Casos que requieren atención inmediata
- **Riesgo Alto**: Casos prioritarios de las últimas 24 horas
- **En Monitoreo**: Casos activos bajo seguimiento
- **Casos Resueltos**: Estadística de casos completados

### Monitor de Alertas
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

## 🛠️ Instalación y Uso

### Requisitos
- Navegador web moderno (Chrome, Firefox, Safari, Edge)
- Conexión a internet para cargar fuentes e iconos

### Instalación
1. Descargar todos los archivos del proyecto
2. Mantener la estructura de carpetas intacta
3. Abrir `index.html` en un navegador web

### Uso Básico
1. **Monitoreo**: El dashboard se actualiza automáticamente
2. **Filtrado**: Usar los controles laterales para filtrar alertas
3. **Acciones**: Hacer clic en los botones de acción de cada alerta
4. **Exportación**: Usar el botón "Exportar" para generar reportes

## ⚠️ Consideraciones Importantes

### Privacidad y Ética
- Este es un prototipo para demostración
- En implementación real, se requiere cumplimiento de GDPR/CCPA
- Necesario consentimiento explícito para monitoreo
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

### Profesionales de Salud Mental
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

### Internacional
- **Línea de Prevención del Suicidio (EE.UU.)**: 988
- **Samaritans (Reino Unido)**: 116 123
- **Lifeline (Australia)**: 13 11 14

## 🤝 Contribución

Este proyecto fue desarrollado como demostración de un sistema de monitoreo de salud mental. Para implementación en producción, se recomienda:

1. Consultar con profesionales de salud mental
2. Cumplir todas las regulaciones aplicables
3. Implementar medidas de seguridad robustas
4. Realizar pruebas exhaustivas con usuarios reales
5. Establecer protocolos de respuesta a crisis

## 📄 Licencia

Este proyecto es una demostración educativa. Para uso comercial o en producción, se requiere desarrollo adicional y cumplimiento de regulaciones específicas.

---

**Nota Importante**: Este dashboard es una demostración técnica. La implementación real de un sistema de monitoreo de salud mental requiere colaboración estrecha con profesionales médicos, cumplimiento legal estricto y medidas de seguridad robustas.

