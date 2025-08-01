// FARO Dashboard - JavaScript Functionality

document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    setupEventListeners();
    createCharts();
    simulateRealTimeUpdates();
});

// Inicialización del dashboard
function initializeDashboard() {
    console.log('FARO Dashboard iniciado');
    updateTimestamp();
    setInterval(updateTimestamp, 60000); // Actualizar cada minuto
}

// Configurar event listeners
function setupEventListeners() {
    // Navegación principal
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            setActiveNavItem(this);
        });
    });

    // Filtros de plataforma
    const platformBtns = document.querySelectorAll('.platform-btn');
    platformBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            setActivePlatform(this);
            filterAlertsByPlatform(this.dataset.platform);
        });
    });

    // Checkboxes de filtro
    const filterCheckboxes = document.querySelectorAll('.filter-checkbox input');
    filterCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            applyRiskFilters();
        });
    });

    // Botones de acción en alertas
    const actionBtns = document.querySelectorAll('.action-btn');
    actionBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            handleAlertAction(this);
        });
    });

    // Botones de sección
    const sectionBtns = document.querySelectorAll('.btn-primary, .btn-secondary');
    sectionBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            handleSectionAction(this);
        });
    });
}

// Navegación
function setActiveNavItem(clickedItem) {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    clickedItem.classList.add('active');
    
    // Simular cambio de vista
    const section = clickedItem.getAttribute('href').substring(1);
    showNotification(`Navegando a: ${clickedItem.textContent.trim()}`, 'info');
}

// Filtros de plataforma
function setActivePlatform(clickedBtn) {
    document.querySelectorAll('.platform-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    clickedBtn.classList.add('active');
}

function filterAlertsByPlatform(platform) {
    const alerts = document.querySelectorAll('.alert-item');
    
    alerts.forEach(alert => {
        const alertPlatform = alert.querySelector('.alert-platform i').className;
        let shouldShow = platform === 'all';
        
        if (!shouldShow) {
            shouldShow = alertPlatform.includes(platform);
        }
        
        alert.style.display = shouldShow ? 'flex' : 'none';
    });
    
    showNotification(`Filtrado por: ${platform === 'all' ? 'Todas las plataformas' : platform}`, 'info');
}

// Filtros de riesgo
function applyRiskFilters() {
    const checkboxes = document.querySelectorAll('.filter-checkbox input');
    const activeFilters = [];
    
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            const label = checkbox.parentElement.textContent.trim();
            activeFilters.push(label.toLowerCase());
        }
    });
    
    const alerts = document.querySelectorAll('.alert-item');
    alerts.forEach(alert => {
        const riskLevel = alert.classList.contains('critical') ? 'riesgo alto' :
                         alert.classList.contains('warning') ? 'riesgo alto' :
                         alert.classList.contains('caution') ? 'riesgo medio' : 'riesgo bajo';
        
        const shouldShow = activeFilters.some(filter => riskLevel.includes(filter.replace('riesgo ', '')));
        alert.style.display = shouldShow ? 'flex' : 'none';
    });
}

// Manejo de acciones en alertas
function handleAlertAction(button) {
    const action = button.textContent.trim().toLowerCase();
    const alertItem = button.closest('.alert-item');
    const alertText = alertItem.querySelector('.alert-text').textContent;
    const alertUser = alertItem.querySelector('.alert-user').textContent;
    
    switch(true) {
        case action.includes('contactar'):
            handleContactAction(alertUser, alertText);
            break;
        case action.includes('revisar'):
            handleReviewAction(alertUser, alertText);
            break;
        case action.includes('escalar'):
            handleEscalateAction(alertUser, alertText);
            break;
        case action.includes('recursos'):
            handleResourcesAction();
            break;
        case action.includes('descartar'):
            handleDismissAction(alertItem);
            break;
        default:
            showNotification('Acción no reconocida', 'warning');
    }
}

function handleContactAction(user, text) {
    showNotification(`Iniciando protocolo de contacto para ${user}`, 'success');
    // Aquí se integraría con el sistema de comunicación
    setTimeout(() => {
        showNotification('Contacto establecido. Documentar en el sistema.', 'info');
    }, 2000);
}

function handleReviewAction(user, text) {
    showNotification(`Abriendo revisión detallada para ${user}`, 'info');
    // Aquí se abriría un modal o nueva vista con más detalles
}

function handleEscalateAction(user, text) {
    showNotification(`Escalando caso de ${user} al supervisor`, 'warning');
    // Aquí se notificaría al supervisor y se actualizaría el estado
}

function handleResourcesAction() {
    showNotification('Abriendo recursos de ayuda', 'info');
    // Aquí se mostrarían recursos específicos
}

function handleDismissAction(alertItem) {
    if (confirm('¿Está seguro de descartar esta alerta?')) {
        alertItem.style.opacity = '0.5';
        alertItem.style.transform = 'translateX(-100%)';
        setTimeout(() => {
            alertItem.remove();
        }, 300);
        showNotification('Alerta descartada', 'info');
    }
}

// Acciones de sección
function handleSectionAction(button) {
    const action = button.textContent.trim().toLowerCase();
    
    if (action.includes('filtrar')) {
        showNotification('Abriendo filtros avanzados', 'info');
    } else if (action.includes('exportar')) {
        handleExport();
    }
}

function handleExport() {
    showNotification('Generando reporte de exportación...', 'info');
    setTimeout(() => {
        showNotification('Reporte exportado exitosamente', 'success');
    }, 2000);
}

// Sistema de notificaciones
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${getNotificationIcon(type)}"></i>
        <span>${message}</span>
        <button class="notification-close">&times;</button>
    `;
    
    // Estilos para la notificación
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${getNotificationColor(type)};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        display: flex;
        align-items: center;
        gap: 0.75rem;
        z-index: 1000;
        min-width: 300px;
        animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove después de 5 segundos
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 5000);
    
    // Botón de cerrar
    notification.querySelector('.notification-close').addEventListener('click', () => {
        notification.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    });
}

function getNotificationIcon(type) {
    switch(type) {
        case 'success': return 'check-circle';
        case 'warning': return 'exclamation-triangle';
        case 'error': return 'times-circle';
        default: return 'info-circle';
    }
}

function getNotificationColor(type) {
    switch(type) {
        case 'success': return '#10b981';
        case 'warning': return '#f59e0b';
        case 'error': return '#ef4444';
        default: return '#3b82f6';
    }
}

// Crear gráficos
function createCharts() {
    createHourlyChart();
    createPlatformChart();
}

function createHourlyChart() {
    const canvas = document.getElementById('hourlyCanvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Datos simulados para las últimas 24 horas
    const hours = [];
    const data = [];
    for (let i = 23; i >= 0; i--) {
        const hour = new Date();
        hour.setHours(hour.getHours() - i);
        hours.push(hour.getHours() + ':00');
        data.push(Math.floor(Math.random() * 20) + 5);
    }
    
    // Limpiar canvas
    ctx.clearRect(0, 0, width, height);
    
    // Configuración
    const padding = 40;
    const chartWidth = width - 2 * padding;
    const chartHeight = height - 2 * padding;
    const maxValue = Math.max(...data);
    
    // Dibujar ejes
    ctx.strokeStyle = '#e5e7eb';
    ctx.lineWidth = 1;
    
    // Eje Y
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, height - padding);
    ctx.stroke();
    
    // Eje X
    ctx.beginPath();
    ctx.moveTo(padding, height - padding);
    ctx.lineTo(width - padding, height - padding);
    ctx.stroke();
    
    // Dibujar línea de datos
    ctx.strokeStyle = '#3b82f6';
    ctx.lineWidth = 2;
    ctx.beginPath();
    
    data.forEach((value, index) => {
        const x = padding + (index * chartWidth) / (data.length - 1);
        const y = height - padding - (value * chartHeight) / maxValue;
        
        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    
    ctx.stroke();
    
    // Dibujar puntos
    ctx.fillStyle = '#3b82f6';
    data.forEach((value, index) => {
        const x = padding + (index * chartWidth) / (data.length - 1);
        const y = height - padding - (value * chartHeight) / maxValue;
        
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, 2 * Math.PI);
        ctx.fill();
    });
    
    // Etiquetas
    ctx.fillStyle = '#6b7280';
    ctx.font = '10px Inter';
    ctx.textAlign = 'center';
    
    // Etiquetas X (cada 4 horas)
    for (let i = 0; i < hours.length; i += 4) {
        const x = padding + (i * chartWidth) / (data.length - 1);
        ctx.fillText(hours[i], x, height - padding + 15);
    }
}

function createPlatformChart() {
    const canvas = document.getElementById('platformCanvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Datos simulados
    const platforms = [
        { name: 'Twitter', value: 45, color: '#1da1f2' },
        { name: 'Facebook', value: 30, color: '#4267b2' },
        { name: 'Instagram', value: 20, color: '#e4405f' },
        { name: 'Otros', value: 5, color: '#6b7280' }
    ];
    
    const total = platforms.reduce((sum, platform) => sum + platform.value, 0);
    
    // Limpiar canvas
    ctx.clearRect(0, 0, width, height);
    
    // Configuración del gráfico de dona
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) / 3;
    const innerRadius = radius * 0.6;
    
    let currentAngle = -Math.PI / 2;
    
    // Dibujar segmentos
    platforms.forEach(platform => {
        const sliceAngle = (platform.value / total) * 2 * Math.PI;
        
        // Segmento exterior
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
        ctx.arc(centerX, centerY, innerRadius, currentAngle + sliceAngle, currentAngle, true);
        ctx.closePath();
        ctx.fillStyle = platform.color;
        ctx.fill();
        
        currentAngle += sliceAngle;
    });
    
    // Texto central
    ctx.fillStyle = '#374151';
    ctx.font = 'bold 16px Inter';
    ctx.textAlign = 'center';
    ctx.fillText('Total', centerX, centerY - 5);
    ctx.font = '12px Inter';
    ctx.fillText(`${total}%`, centerX, centerY + 10);
    
    // Leyenda
    const legendY = height - 60;
    let legendX = 20;
    
    platforms.forEach(platform => {
        // Cuadrado de color
        ctx.fillStyle = platform.color;
        ctx.fillRect(legendX, legendY, 12, 12);
        
        // Texto
        ctx.fillStyle = '#374151';
        ctx.font = '10px Inter';
        ctx.textAlign = 'left';
        ctx.fillText(`${platform.name} (${platform.value}%)`, legendX + 16, legendY + 9);
        
        legendX += 70;
    });
}

// Simulación de actualizaciones en tiempo real
function simulateRealTimeUpdates() {
    setInterval(() => {
        updateAlertCounts();
        updateSystemStatus();
    }, 30000); // Cada 30 segundos
    
    setInterval(() => {
        createCharts(); // Actualizar gráficos cada 5 minutos
    }, 300000);
}

function updateAlertCounts() {
    const cards = document.querySelectorAll('.summary-card');
    cards.forEach(card => {
        const numberElement = card.querySelector('.card-number');
        if (numberElement) {
            const currentValue = parseInt(numberElement.textContent);
            const change = Math.floor(Math.random() * 3) - 1; // -1, 0, o 1
            const newValue = Math.max(0, currentValue + change);
            
            if (change !== 0) {
                numberElement.style.transform = 'scale(1.1)';
                numberElement.textContent = newValue;
                setTimeout(() => {
                    numberElement.style.transform = 'scale(1)';
                }, 200);
            }
        }
    });
}

function updateSystemStatus() {
    const statusIndicator = document.querySelector('.status-indicator');
    const statusText = document.querySelector('.status-text');
    
    // Simular ocasionalmente un estado de "procesando"
    if (Math.random() < 0.1) {
        statusIndicator.style.background = '#f59e0b';
        statusText.textContent = 'Procesando...';
        statusText.style.color = '#f59e0b';
        
        setTimeout(() => {
            statusIndicator.style.background = '#10b981';
            statusText.textContent = 'Sistema Activo';
            statusText.style.color = '#10b981';
        }, 3000);
    }
}

function updateTimestamp() {
    const now = new Date();
    const timestamp = now.toLocaleString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
    
    // Actualizar cualquier elemento de timestamp si existe
    const timestampElements = document.querySelectorAll('.timestamp');
    timestampElements.forEach(element => {
        element.textContent = timestamp;
    });
}

// Agregar estilos para animaciones
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .notification-close {
        background: none;
        border: none;
        color: white;
        font-size: 1.2rem;
        cursor: pointer;
        padding: 0;
        margin-left: auto;
    }
    
    .notification-close:hover {
        opacity: 0.8;
    }
`;
document.head.appendChild(style);

// Funciones de utilidad
function formatTime(date) {
    return date.toLocaleTimeString('es-ES', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatDate(date) {
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    });
}

// Exportar funciones para uso externo si es necesario
window.FaroDashboard = {
    showNotification,
    updateAlertCounts,
    createCharts
};

