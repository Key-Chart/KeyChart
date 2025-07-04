// JavaScript para a tela de relatórios - KeyChart

// Configurações globais dos gráficos
Chart.defaults.font.family = 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif';
Chart.defaults.font.size = 12;
Chart.defaults.plugins.legend.display = true;

// Paleta de cores profissional
const colors = {
    primary: '#667eea',
    secondary: '#764ba2',
    success: '#27ae60',
    warning: '#f39c12',
    info: '#3498db',
    danger: '#e74c3c',
    light: '#ecf0f1',
    dark: '#2c3e50'
};

// Gradientes para os gráficos
function createGradient(ctx, color1, color2) {
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, color1);
    gradient.addColorStop(1, color2);
    return gradient;
}

// Configurações padrão para todos os gráficos
const defaultChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'top',
            labels: {
                padding: 20,
                usePointStyle: true,
                font: {
                    size: 11,
                    weight: '500'
                }
            }
        },
        tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleColor: '#fff',
            bodyColor: '#fff',
            cornerRadius: 8,
            padding: 12,
            displayColors: true
        }
    },
    elements: {
        point: {
            radius: 6,
            hoverRadius: 8
        },
        line: {
            borderWidth: 3,
            tension: 0.4
        }
    }
};

// Variáveis globais para os gráficos
let inscricoesChart, sexoChart, partidasChart, idadesChart, faixasChart;

// Função para inicializar todos os gráficos
function initializeCharts() {
    initInscricoesChart();
    initSexoChart();
    initPartidasChart();
    initIdadesChart();
    initFaixasChart();
}

// Gráfico de evolução de inscrições
function initInscricoesChart() {
    const ctx = document.getElementById('inscricoesChart');
    if (!ctx) return;
    
    const gradient = createGradient(ctx.getContext('2d'), colors.primary, colors.secondary);
    
    inscricoesChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.inscricoes.labels,
            datasets: [{
                label: 'Inscrições',
                data: chartData.inscricoes.data,
                borderColor: colors.primary,
                backgroundColor: gradient,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: colors.primary,
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 8
            }]
        },
        options: {
            ...defaultChartOptions,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0,0,0,0.1)',
                        borderDash: [5, 5]
                    },
                    ticks: {
                        font: {
                            size: 11
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 11
                        }
                    }
                }
            },
            plugins: {
                ...defaultChartOptions.plugins,
                tooltip: {
                    ...defaultChartOptions.plugins.tooltip,
                    callbacks: {
                        label: function(context) {
                            return `Inscrições: ${context.parsed.y}`;
                        }
                    }
                }
            }
        }
    });
}

// Gráfico de distribuição por sexo
function initSexoChart() {
    const ctx = document.getElementById('sexoChart');
    if (!ctx) return;
    
    sexoChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Masculino', 'Feminino'],
            datasets: [{
                data: [chartData.sexo.masculino, chartData.sexo.feminino],
                backgroundColor: [
                    colors.info,
                    colors.warning
                ],
                borderWidth: 3,
                borderColor: '#fff',
                hoverBorderWidth: 4
            }]
        },
        options: {
            ...defaultChartOptions,
            cutout: '60%',
            plugins: {
                ...defaultChartOptions.plugins,
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        font: {
                            size: 12,
                            weight: '500'
                        }
                    }
                },
                tooltip: {
                    ...defaultChartOptions.plugins.tooltip,
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((context.parsed * 100) / total).toFixed(1);
                            return `${context.label}: ${context.parsed} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Gráfico de status das partidas
function initPartidasChart() {
    const ctx = document.getElementById('partidasChart');
    if (!ctx) return;
    
    partidasChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Finalizadas', 'Em Andamento', 'Agendadas'],
            datasets: [{
                data: [
                    chartData.partidas.finalizadas,
                    chartData.partidas.em_andamento,
                    chartData.partidas.agendadas
                ],
                backgroundColor: [
                    colors.success,
                    colors.warning,
                    colors.info
                ],
                borderWidth: 3,
                borderColor: '#fff',
                hoverBorderWidth: 4
            }]
        },
        options: {
            ...defaultChartOptions,
            cutout: '60%',
            plugins: {
                ...defaultChartOptions.plugins,
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        usePointStyle: true,
                        font: {
                            size: 11,
                            weight: '500'
                        }
                    }
                },
                tooltip: {
                    ...defaultChartOptions.plugins.tooltip,
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = total > 0 ? ((context.parsed * 100) / total).toFixed(1) : 0;
                            return `${context.label}: ${context.parsed} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Gráfico de distribuição por idades
function initIdadesChart() {
    const ctx = document.getElementById('idadesChart');
    if (!ctx) return;
    
    const labels = chartData.idades.map(item => item.label);
    const data = chartData.idades.map(item => item.value);
    
    idadesChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Atletas',
                data: data,
                backgroundColor: colors.primary,
                borderColor: colors.secondary,
                borderWidth: 2,
                borderRadius: 6,
                borderSkipped: false
            }]
        },
        options: {
            ...defaultChartOptions,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0,0,0,0.1)',
                        borderDash: [5, 5]
                    },
                    ticks: {
                        font: {
                            size: 11
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 11
                        }
                    }
                }
            },
            plugins: {
                ...defaultChartOptions.plugins,
                legend: {
                    display: false
                },
                tooltip: {
                    ...defaultChartOptions.plugins.tooltip,
                    callbacks: {
                        label: function(context) {
                            return `Faixa ${context.label}: ${context.parsed.y} atletas`;
                        }
                    }
                }
            }
        }
    });
}

// Gráfico de distribuição por faixas
function initFaixasChart() {
    const ctx = document.getElementById('faixasChart');
    if (!ctx) return;
    
    const labels = chartData.faixas.map(item => item.label);
    const data = chartData.faixas.map(item => item.value);
    
    // Cores específicas para cada faixa
    const faixaCores = {
        'Branca': '#ffffff',
        'Azul': '#3498db',
        'Amarela': '#f1c40f',
        'Laranja': '#e67e22',
        'Verde': '#27ae60',
        'Roxa': '#9b59b6',
        'Marrom': '#8b4513',
        'Preta': '#2c3e50'
    };
    
    const backgroundColors = labels.map(label => faixaCores[label] || colors.primary);
    
    faixasChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: backgroundColors,
                borderWidth: 2,
                borderColor: '#fff',
                hoverBorderWidth: 3
            }]
        },
        options: {
            ...defaultChartOptions,
            plugins: {
                ...defaultChartOptions.plugins,
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        usePointStyle: true,
                        font: {
                            size: 10,
                            weight: '500'
                        },
                        generateLabels: function(chart) {
                            const data = chart.data;
                            if (data.labels.length && data.datasets.length) {
                                return data.labels.map((label, i) => {
                                    const dataset = data.datasets[0];
                                    const value = dataset.data[i];
                                    return {
                                        text: `${label} (${value})`,
                                        fillStyle: dataset.backgroundColor[i],
                                        strokeStyle: dataset.borderColor,
                                        lineWidth: dataset.borderWidth,
                                        pointStyle: 'circle',
                                        hidden: false,
                                        index: i
                                    };
                                });
                            }
                            return [];
                        }
                    }
                },
                tooltip: {
                    ...defaultChartOptions.plugins.tooltip,
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = total > 0 ? ((context.parsed * 100) / total).toFixed(1) : 0;
                            return `${context.label}: ${context.parsed} atletas (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Função para alternar tipo de gráfico
function toggleChartType(chartName) {
    switch(chartName) {
        case 'inscricoes':
            if (inscricoesChart.config.type === 'line') {
                inscricoesChart.config.type = 'bar';
                inscricoesChart.data.datasets[0].fill = false;
                inscricoesChart.data.datasets[0].backgroundColor = colors.primary;
            } else {
                inscricoesChart.config.type = 'line';
                inscricoesChart.data.datasets[0].fill = true;
                const gradient = createGradient(inscricoesChart.ctx, colors.primary, colors.secondary);
                inscricoesChart.data.datasets[0].backgroundColor = gradient;
            }
            inscricoesChart.update('active');
            break;
    }
}

// Função para exportar relatório
function exportReport(format) {
    showLoading();
    
    setTimeout(() => {
        hideLoading();
        
        if (format === 'pdf') {
            showToast('Funcionalidade de exportação PDF em desenvolvimento', 'info');
        } else if (format === 'excel') {
            showToast('Funcionalidade de exportação Excel em desenvolvimento', 'info');
        }
    }, 2000);
}

// Função para atualizar dados
function refreshData() {
    showLoading();
    
    setTimeout(() => {
        hideLoading();
        showToast('Dados atualizados com sucesso!', 'success');
        
        // Animar as estatísticas
        animateCounters();
    }, 1500);
}

// Função para mostrar loading
function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex';
}

// Função para esconder loading
function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

// Função para mostrar toast/notificação
function showToast(message, type = 'info') {
    // Criar elemento do toast
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <i class="bi bi-${getToastIcon(type)}"></i>
            <span>${message}</span>
        </div>
    `;
    
    // Adicionar estilos CSS inline para o toast
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${getToastColor(type)};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        z-index: 10000;
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s ease;
    `;
    
    document.body.appendChild(toast);
    
    // Animar entrada
    setTimeout(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateX(0)';
    }, 100);
    
    // Remover após 3 segundos
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// Função auxiliar para ícones do toast
function getToastIcon(type) {
    const icons = {
        success: 'check-circle-fill',
        error: 'exclamation-triangle-fill',
        warning: 'exclamation-circle-fill',
        info: 'info-circle-fill'
    };
    return icons[type] || icons.info;
}

// Função auxiliar para cores do toast
function getToastColor(type) {
    const colors = {
        success: '#27ae60',
        error: '#e74c3c',
        warning: '#f39c12',
        info: '#3498db'
    };
    return colors[type] || colors.info;
}

// Função para animar contadores
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');
    
    counters.forEach(counter => {
        const target = parseInt(counter.innerText.replace(/[^\d]/g, ''));
        const increment = target / 100;
        let current = 0;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                counter.innerText = target.toLocaleString();
                clearInterval(timer);
            } else {
                counter.innerText = Math.floor(current).toLocaleString();
            }
        }, 20);
    });
}

// Função para responsive dos gráficos
function handleResize() {
    if (inscricoesChart) inscricoesChart.resize();
    if (sexoChart) sexoChart.resize();
    if (partidasChart) partidasChart.resize();
    if (idadesChart) idadesChart.resize();
    if (faixasChart) faixasChart.resize();
}

// Função para ajustar layout com sidebar
function adjustLayoutForSidebar() {
    const content = document.getElementById('content');
    const sidebar = document.getElementById('sidebar');
    
    if (!content) return;
    
    // Verificar se a sidebar existe e está minimizada
    if (sidebar && sidebar.classList.contains('sidebar-hidden')) {
        content.classList.add('content-expanded');
        content.style.marginLeft = '60px';
        content.style.width = 'calc(100% - 60px)';
    } else {
        content.classList.remove('content-expanded');
        content.style.marginLeft = '250px';
        content.style.width = 'calc(100% - 250px)';
    }
    
    // Redimensionar gráficos após mudança de layout
    setTimeout(handleResize, 300);
}

// Função para verificar periodicamente o estado da sidebar
function checkSidebarState() {
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');
    
    if (!sidebar || !content) return;
    
    // Verificar se a sidebar mudou de estado
    const isHidden = sidebar.classList.contains('sidebar-hidden');
    const contentExpanded = content.classList.contains('content-expanded');
    
    if (isHidden && !contentExpanded) {
        adjustLayoutForSidebar();
    } else if (!isHidden && contentExpanded) {
        adjustLayoutForSidebar();
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Verificar estado inicial da sidebar
    setTimeout(() => {
        adjustLayoutForSidebar();
        detectSidebarState();
    }, 100);
    
    // Inicializar gráficos
    initializeCharts();
    
    // Animar contadores na primeira carga
    setTimeout(animateCounters, 500);
    
    // Listener para redimensionamento
    window.addEventListener('resize', handleResize);
    
    // Verificar periodicamente o estado da sidebar
    setInterval(checkSidebarState, 500);
    
    // Listener para mudanças na sidebar (se existir)
    const toggleBtn = document.querySelector('.toggle-btn');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            setTimeout(() => {
                adjustLayoutForSidebar();
                detectSidebarState();
            }, 350);
        });
    }
    
    // Observer para mudanças na classe da sidebar
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                    setTimeout(() => {
                        adjustLayoutForSidebar();
                        detectSidebarState();
                    }, 100);
                }
            });
        });
        
        observer.observe(sidebar, {
            attributes: true,
            attributeFilter: ['class']
        });
    }
    
    // Listener para clicks nos cards de estatísticas
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach(card => {
        card.addEventListener('click', function() {
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });
    
    // Adicionar efeito de hover aos gráficos
    const chartCards = document.querySelectorAll('.chart-card, .data-card');
    chartCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});

// Função para detectar estado da sidebar e aplicar classes no body
function detectSidebarState() {
    const sidebar = document.getElementById('sidebar');
    const body = document.body;
    
    if (!sidebar) return;
    
    if (sidebar.classList.contains('sidebar-hidden')) {
        body.classList.add('sidebar-closed');
        body.classList.remove('sidebar-open');
    } else {
        body.classList.add('sidebar-open');
        body.classList.remove('sidebar-closed');
    }
}

// Função para debug dos dados
function debugChartData() {
    console.log('Chart Data:', chartData);
    console.log('Charts initialized:', {
        inscricoes: !!inscricoesChart,
        sexo: !!sexoChart,
        partidas: !!partidasChart,
        idades: !!idadesChart,
        faixas: !!faixasChart
    });
}

// Exportar funções para uso global
window.toggleChartType = toggleChartType;
window.exportReport = exportReport;
window.refreshData = refreshData;
window.debugChartData = debugChartData;
window.adjustLayoutForSidebar = adjustLayoutForSidebar;
window.detectSidebarState = detectSidebarState;
