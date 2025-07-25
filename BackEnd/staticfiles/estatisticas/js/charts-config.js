// Configurações de Gráficos - KeyChart Estatísticas
class ChartsConfig {
    constructor() {
        this.defaultColors = {
            primary: '#007bff',
            success: '#28a745',
            info: '#17a2b8',
            warning: '#ffc107',
            danger: '#dc3545',
            purple: '#6f42c1',
            gray: '#6c757d'
        };
        
        this.gradients = {};
        this.init();
    }

    init() {
        Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
        Chart.defaults.font.size = 12;
        Chart.defaults.color = '#495057';
        
        this.createGradients();
        this.registerCustomPlugins();
    }

    createGradients() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        // Gradiente azul
        this.gradients.blue = ctx.createLinearGradient(0, 0, 0, 300);
        this.gradients.blue.addColorStop(0, 'rgba(0, 123, 255, 0.3)');
        this.gradients.blue.addColorStop(1, 'rgba(0, 123, 255, 0.05)');
        
        // Gradiente verde
        this.gradients.green = ctx.createLinearGradient(0, 0, 0, 300);
        this.gradients.green.addColorStop(0, 'rgba(40, 167, 69, 0.3)');
        this.gradients.green.addColorStop(1, 'rgba(40, 167, 69, 0.05)');
        
        // Gradiente laranja
        this.gradients.orange = ctx.createLinearGradient(0, 0, 0, 300);
        this.gradients.orange.addColorStop(0, 'rgba(255, 193, 7, 0.3)');
        this.gradients.orange.addColorStop(1, 'rgba(255, 193, 7, 0.05)');
    }

    registerCustomPlugins() {
        // Plugin para valores centrais em doughnut charts
        Chart.register({
            id: 'centerText',
            beforeDraw: (chart) => {
                if (chart.config.options.plugins?.centerText) {
                    const { ctx, width, height } = chart;
                    const centerText = chart.config.options.plugins.centerText;
                    
                    ctx.save();
                    ctx.font = `${centerText.fontSize || 20}px ${centerText.fontFamily || 'Arial'}`;
                    ctx.fillStyle = centerText.color || '#333';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    
                    const text = centerText.text || '';
                    ctx.fillText(text, width / 2, height / 2);
                    ctx.restore();
                }
            }
        });

        // Plugin para animações customizadas
        Chart.register({
            id: 'customAnimations',
            beforeInit: (chart) => {
                chart.config.options.animation = {
                    ...chart.config.options.animation,
                    duration: 1000,
                    easing: 'easeInOutQuart'
                };
            }
        });
    }

    // Configuração para gráfico de linha de competições
    getCompetitionsLineConfig(data) {
        return {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Competições Realizadas',
                    data: data.values,
                    borderColor: this.defaultColors.primary,
                    backgroundColor: this.gradients.blue,
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 6,
                    pointHoverRadius: 8,
                    pointBackgroundColor: '#ffffff',
                    pointBorderColor: this.defaultColors.primary,
                    pointBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        borderColor: this.defaultColors.primary,
                        borderWidth: 1,
                        cornerRadius: 8,
                        displayColors: false,
                        callbacks: {
                            title: (context) => {
                                return `Período: ${context[0].label}`;
                            },
                            label: (context) => {
                                return `${context.parsed.y} competições`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)',
                            borderDash: [5, 5]
                        },
                        ticks: {
                            stepSize: 1,
                            callback: function(value) {
                                return Number.isInteger(value) ? value : '';
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            maxTicksLimit: 7
                        }
                    }
                }
            }
        };
    }

    // Configuração para gráfico de rosca de atletas
    getAthletesDoughnutConfig(data) {
        const total = data.values.reduce((sum, val) => sum + val, 0);
        
        return {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.values,
                    backgroundColor: [
                        this.defaultColors.primary,
                        this.defaultColors.success,
                        this.defaultColors.warning,
                        this.defaultColors.danger,
                        this.defaultColors.purple
                    ],
                    borderWidth: 0,
                    hoverBorderWidth: 2,
                    hoverBorderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '60%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true,
                            font: {
                                size: 11
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        cornerRadius: 8,
                        callbacks: {
                            label: (context) => {
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return `${context.label}: ${context.parsed} (${percentage}%)`;
                            }
                        }
                    },
                    centerText: {
                        text: total.toString(),
                        fontSize: 24,
                        color: this.defaultColors.gray
                    }
                }
            }
        };
    }

    // Configuração para gráfico de barras de performance
    getPerformanceBarConfig(data) {
        return {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Performance Score',
                    data: data.values,
                    backgroundColor: data.values.map(val => {
                        if (val >= 80) return this.defaultColors.success;
                        if (val >= 60) return this.defaultColors.warning;
                        return this.defaultColors.danger;
                    }),
                    borderColor: data.values.map(val => {
                        if (val >= 80) return this.defaultColors.success;
                        if (val >= 60) return this.defaultColors.warning;
                        return this.defaultColors.danger;
                    }),
                    borderWidth: 1,
                    borderRadius: 4,
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
                        cornerRadius: 8,
                        callbacks: {
                            label: (context) => {
                                return `Score: ${context.parsed.y}%`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)',
                            borderDash: [5, 5]
                        },
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        };
    }

    // Configuração para gráfico de área de evolução
    getEvolutionAreaConfig(data) {
        return {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: data.datasets.map((dataset, index) => ({
                    label: dataset.label,
                    data: dataset.data,
                    borderColor: this.getColorByIndex(index),
                    backgroundColor: this.getGradientByIndex(index),
                    borderWidth: 2,
                    fill: true,
                    tension: 0.3,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }))
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        cornerRadius: 8
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        };
    }

    // Configuração para gráfico de radar de habilidades
    getSkillsRadarConfig(data) {
        return {
            type: 'radar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Habilidades',
                    data: data.values,
                    borderColor: this.defaultColors.primary,
                    backgroundColor: 'rgba(0, 123, 255, 0.2)',
                    borderWidth: 2,
                    pointRadius: 4,
                    pointBackgroundColor: this.defaultColors.primary,
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        },
                        angleLines: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        },
                        pointLabels: {
                            font: {
                                size: 11
                            }
                        }
                    }
                }
            }
        };
    }

    // Configuração para gráfico de dispersão de correlação
    getCorrelationScatterConfig(data) {
        return {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Correlação',
                    data: data.points,
                    backgroundColor: this.defaultColors.primary,
                    borderColor: this.defaultColors.primary,
                    pointRadius: 6,
                    pointHoverRadius: 8
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
                        cornerRadius: 8,
                        callbacks: {
                            title: () => '',
                            label: (context) => {
                                return `X: ${context.parsed.x}, Y: ${context.parsed.y}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: data.xLabel || 'X'
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: data.yLabel || 'Y'
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    }
                }
            }
        };
    }

    // Configuração para gráfico de barras horizontais
    getHorizontalBarConfig(data) {
        return {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: data.label || 'Dados',
                    data: data.values,
                    backgroundColor: this.defaultColors.info,
                    borderColor: this.defaultColors.info,
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    },
                    y: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        };
    }

    // Métodos auxiliares
    getColorByIndex(index) {
        const colors = Object.values(this.defaultColors);
        return colors[index % colors.length];
    }

    getGradientByIndex(index) {
        const gradients = Object.values(this.gradients);
        return gradients[index % gradients.length];
    }

    // Atualizar dados de um gráfico existente
    updateChartData(chart, newData) {
        if (!chart) return;

        chart.data.labels = newData.labels;
        chart.data.datasets.forEach((dataset, index) => {
            if (newData.datasets && newData.datasets[index]) {
                dataset.data = newData.datasets[index].data;
            } else if (newData.values) {
                dataset.data = newData.values;
            }
        });

        chart.update('active');
    }

    // Criar gráfico com animação personalizada
    createAnimatedChart(ctx, config, animationType = 'default') {
        const animations = {
            default: {
                duration: 1000,
                easing: 'easeInOutQuart'
            },
            bounce: {
                duration: 1500,
                easing: 'easeOutBounce'
            },
            elastic: {
                duration: 2000,
                easing: 'easeOutElastic'
            }
        };

        config.options.animation = {
            ...config.options.animation,
            ...animations[animationType]
        };

        return new Chart(ctx, config);
    }

    // Exportar gráfico como imagem
    exportChart(chart, filename = 'chart.png') {
        const url = chart.toBase64Image();
        const link = document.createElement('a');
        link.download = filename;
        link.href = url;
        link.click();
    }

    // Redimensionar todos os gráficos
    resizeAllCharts(charts) {
        Object.values(charts).forEach(chart => {
            if (chart && typeof chart.resize === 'function') {
                chart.resize();
            }
        });
    }

    // Destruir gráfico
    destroyChart(chart) {
        if (chart && typeof chart.destroy === 'function') {
            chart.destroy();
        }
    }
}

// Instância global
window.chartsConfig = new ChartsConfig();
