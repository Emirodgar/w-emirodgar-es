// Datos simulados para el dashboard
const dashboardData = {
    metrics: {
        uniqueUsers: '2.8M',
        pageViews: '12.8M',
        avgDuration: '4:05',
        trafficQuality: '87%'
    },
    audienceData: {
        labels: ['Jul 10', 'Jul 13', 'Jul 16', 'Jul 19', 'Jul 22', 'Jul 25', 'Jul 28', 'Jul 31', 'Aug 03', 'Aug 07'],
        users: [165000, 158000, 172000, 145000, 168000, 175000, 162000, 158000, 170000, 165000],
        sessions: [98000, 95000, 103000, 87000, 101000, 105000, 97000, 95000, 102000, 99000]
    },
    roiData: {
        labels: ['Turismo España', 'Promoción Cultura', 'Educación Digital', 'Salud Pública'],
        values: [3.2, 2.8, 4.1, 2.4]
    }
};

// Variables globales para los gráficos
let audienceChart = null;
let roiChart = null;

// Inicialización del dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeTabs();
    initializeCharts();
    initializeEventListeners();
    updateMetrics();
});

// Gestión de pestañas
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            
            // Remover clase active de todos los botones y contenidos
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Agregar clase active al botón y contenido seleccionado
            button.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
            
            // Redimensionar gráficos si es necesario
            setTimeout(() => {
                if (targetTab === 'resumen' && audienceChart) {
                    audienceChart.resize();
                } else if (targetTab === 'campanas' && roiChart) {
                    roiChart.resize();
                }
            }, 100);
        });
    });
}

// Inicialización de gráficos
function initializeCharts() {
    createAudienceChart();
    createROIChart();
}

// Gráfico de audiencia
function createAudienceChart() {
    const ctx = document.getElementById('audienceChart');
    if (!ctx) return;

    audienceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dashboardData.audienceData.labels,
            datasets: [
                {
                    label: 'Usuarios',
                    data: dashboardData.audienceData.users,
                    borderColor: '#0099cc',
                    backgroundColor: 'rgba(0, 153, 204, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#0099cc',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 5
                },
                {
                    label: 'Sesiones',
                    data: dashboardData.audienceData.sessions,
                    borderColor: '#33bbee',
                    backgroundColor: 'rgba(51, 187, 238, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#33bbee',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 5
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        usePointStyle: true,
                        padding: 20,
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff',
                    borderColor: '#0099cc',
                    borderWidth: 1,
                    cornerRadius: 8,
                    displayColors: true,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y.toLocaleString();
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 11
                        },
                        color: '#666'
                    }
                },
                y: {
                    beginAtZero: false,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        font: {
                            size: 11
                        },
                        color: '#666',
                        callback: function(value) {
                            return (value / 1000) + 'K';
                        }
                    }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            },
            elements: {
                point: {
                    hoverRadius: 8
                }
            }
        }
    });
}

// Gráfico de ROI
function createROIChart() {
    const ctx = document.getElementById('roiChart');
    if (!ctx) return;

    roiChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dashboardData.roiData.labels,
            datasets: [{
                label: 'ROI',
                data: dashboardData.roiData.values,
                backgroundColor: [
                    'rgba(0, 153, 204, 0.8)',
                    'rgba(51, 187, 238, 0.8)',
                    'rgba(102, 204, 221, 0.8)',
                    'rgba(255, 153, 0, 0.8)'
                ],
                borderColor: [
                    '#0099cc',
                    '#33bbee',
                    '#66ccdd',
                    '#ff9900'
                ],
                borderWidth: 2,
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff',
                    borderColor: '#0099cc',
                    borderWidth: 1,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            return 'ROI: ' + context.parsed.y + 'x';
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 11,
                            weight: '600'
                        },
                        color: '#003366'
                    }
                },
                y: {
                    beginAtZero: true,
                    max: 5,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        font: {
                            size: 11
                        },
                        color: '#666',
                        callback: function(value) {
                            return value + 'x';
                        }
                    }
                }
            },
            elements: {
                bar: {
                    borderWidth: 2
                }
            }
        }
    });
}

// Event listeners
function initializeEventListeners() {
    // Botón de actualizar
    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            refreshData();
            showNotification('Datos actualizados correctamente', 'success');
        });
    }

    // Botón de exportar
    const exportBtn = document.getElementById('exportBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', function() {
            exportData();
        });
    }

    // Animaciones de hover para las tarjetas de métricas
    const metricCards = document.querySelectorAll('.metric-card');
    metricCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Actualizar métricas
function updateMetrics() {
    const metrics = dashboardData.metrics;
    
    document.getElementById('uniqueUsers').textContent = metrics.uniqueUsers;
    document.getElementById('pageViews').textContent = metrics.pageViews;
    document.getElementById('avgDuration').textContent = metrics.avgDuration;
    document.getElementById('trafficQuality').textContent = metrics.trafficQuality;
}

// Refrescar datos
function refreshData() {
    // Simular actualización de datos
    const refreshIcon = document.querySelector('#refreshBtn i');
    refreshIcon.classList.add('fa-spin');
    
    setTimeout(() => {
        // Actualizar métricas con pequeñas variaciones
        updateMetricsWithVariation();
        
        // Actualizar gráficos
        updateCharts();
        
        refreshIcon.classList.remove('fa-spin');
    }, 1500);
}

// Actualizar métricas con variación
function updateMetricsWithVariation() {
    // Generar pequeñas variaciones en los datos
    const variations = {
        uniqueUsers: generateVariation(2.8, 0.1) + 'M',
        pageViews: generateVariation(12.8, 0.5) + 'M',
        avgDuration: generateTimeVariation(),
        trafficQuality: Math.floor(generateVariation(87, 2)) + '%'
    };
    
    dashboardData.metrics = variations;
    updateMetrics();
}

// Generar variación en los datos
function generateVariation(base, range) {
    const variation = (Math.random() - 0.5) * range * 2;
    return Math.round((base + variation) * 10) / 10;
}

// Generar variación en tiempo
function generateTimeVariation() {
    const baseMinutes = 4;
    const baseSeconds = 5;
    const totalSeconds = baseMinutes * 60 + baseSeconds;
    const variation = Math.floor((Math.random() - 0.5) * 60);
    const newTotalSeconds = Math.max(180, totalSeconds + variation); // Mínimo 3 minutos
    
    const minutes = Math.floor(newTotalSeconds / 60);
    const seconds = newTotalSeconds % 60;
    
    return minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
}

// Actualizar gráficos
function updateCharts() {
    if (audienceChart) {
        // Generar nuevos datos para el gráfico de audiencia
        const newUsers = dashboardData.audienceData.users.map(value => 
            Math.floor(generateVariation(value, value * 0.1))
        );
        const newSessions = dashboardData.audienceData.sessions.map(value => 
            Math.floor(generateVariation(value, value * 0.1))
        );
        
        audienceChart.data.datasets[0].data = newUsers;
        audienceChart.data.datasets[1].data = newSessions;
        audienceChart.update('active');
    }
    
    if (roiChart) {
        // Generar nuevos datos para el gráfico de ROI
        const newROI = dashboardData.roiData.values.map(value => 
            Math.round(generateVariation(value, 0.3) * 10) / 10
        );
        
        roiChart.data.datasets[0].data = newROI;
        roiChart.update('active');
    }
}

// Exportar datos
function exportData() {
    const activeTab = document.querySelector('.tab-button.active').getAttribute('data-tab');
    
    let exportData = {};
    let filename = 'dashboard_data';
    
    switch(activeTab) {
        case 'resumen':
            exportData = {
                metrics: dashboardData.metrics,
                audienceData: dashboardData.audienceData,
                timestamp: new Date().toISOString()
            };
            filename = 'resumen_audiencias';
            break;
        case 'medios':
            exportData = {
                ranking: [
                    { position: 1, name: 'El País Digital', users: '1.2M', quality: '92%', sessions: '2.2M' },
                    { position: 2, name: 'El Mundo Online', users: '987.2K', quality: '89%', sessions: '1.8M' },
                    { position: 3, name: 'ABC Digital', users: '734.8K', quality: '91%', sessions: '1.4M' },
                    { position: 4, name: 'La Vanguardia', users: '623.8K', quality: '88%', sessions: '1.2M' },
                    { position: 5, name: 'El Confidencial', users: '584.7K', quality: '94%', sessions: '1.0M' }
                ],
                timestamp: new Date().toISOString()
            };
            filename = 'ranking_medios';
            break;
        case 'calidad':
            exportData = {
                trafficQuality: {
                    human: '87%',
                    bots: '13%'
                },
                fraudDetection: {
                    botsBlocked: '1.8M',
                    suspiciousIPs: '23.8K',
                    invalidClicks: '8.5K'
                },
                timestamp: new Date().toISOString()
            };
            filename = 'calidad_trafico';
            break;
        case 'campanas':
            exportData = {
                campaigns: [
                    { name: 'Campaña Turismo España', roi: '3.2x', investment: '€450,000', reach: '2.1M', conversions: '15,600' },
                    { name: 'Promoción Cultura', roi: '2.8x', investment: '€320,000', reach: '1.8M', conversions: '12,400' },
                    { name: 'Educación Digital', roi: '4.1x', investment: '€280,000', reach: '1.5M', conversions: '18,200' }
                ],
                roiData: dashboardData.roiData,
                timestamp: new Date().toISOString()
            };
            filename = 'campanas_roi';
            break;
    }
    
    // Crear y descargar archivo JSON
    const dataStr = JSON.stringify(exportData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = filename + '_' + new Date().toISOString().split('T')[0] + '.json';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
    showNotification('Datos exportados correctamente', 'success');
}

// Mostrar notificaciones
function showNotification(message, type = 'info') {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    // Estilos para la notificación
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#d4edda' : '#d1ecf1'};
        color: ${type === 'success' ? '#155724' : '#0c5460'};
        padding: 1rem 1.5rem;
        border-radius: 8px;
        border: 1px solid ${type === 'success' ? '#c3e6cb' : '#bee5eb'};
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Animar entrada
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remover después de 3 segundos
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Función para redimensionar gráficos en cambio de ventana
window.addEventListener('resize', function() {
    setTimeout(() => {
        if (audienceChart) audienceChart.resize();
        if (roiChart) roiChart.resize();
    }, 100);
});

// Animaciones adicionales al cargar
window.addEventListener('load', function() {
    // Animar métricas principales
    const metricCards = document.querySelectorAll('.metric-card');
    metricCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Animar barras geográficas
    setTimeout(() => {
        const geoFills = document.querySelectorAll('.geo-fill');
        geoFills.forEach((fill, index) => {
            const width = fill.style.width;
            fill.style.width = '0%';
            
            setTimeout(() => {
                fill.style.transition = 'width 1s ease';
                fill.style.width = width;
            }, index * 200);
        });
    }, 1000);
    
    // Animar barras de tráfico
    setTimeout(() => {
        const trafficFills = document.querySelectorAll('.traffic-fill');
        trafficFills.forEach((fill, index) => {
            const width = fill.style.width;
            fill.style.width = '0%';
            
            setTimeout(() => {
                fill.style.transition = 'width 1s ease';
                fill.style.width = width;
            }, index * 300);
        });
    }, 1500);
});

