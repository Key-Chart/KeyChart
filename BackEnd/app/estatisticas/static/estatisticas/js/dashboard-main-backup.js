// Dashboard Principal - KeyChart Estatísticas
class DashboardMain {
    constructor() {
        this.charts = {};
        this.updateInterval = null;
        this.currentPeriod = '7d';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadInitialData();
        this.startAutoUpdate();
        this.initializeAnimations();
    }

    setupEventListeners() {
        // Botões de período
        document.querySelectorAll('.btn-periodo').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                this.changePeriod(btn.dataset.periodo);
            });
        });

        // Filtros
        document.querySelectorAll('.filtro-grupo select, .filtro-grupo input').forEach(filter => {
            filter.addEventListener('change', () => {
                this.applyFilters();
            });
        });

        // Refresh manual
        document.getElementById('refreshData')?.addEventListener('click', () => {
            this.refreshAllData();
        });

        // Export
        document.getElementById('exportData')?.addEventListener('click', () => {
            this.exportData();
        });

        // Resize handler para gráficos
        window.addEventListener('resize', () => {
            this.resizeCharts();
        });
    }

    async loadInitialData() {
        this.showLoading();
        
        try {
            // Carregar dados principais
            await Promise.all([
                this.loadMetricas(),
                this.loadGraficos(),
                this.loadKPIs(),
                this.loadAlertas()
            ]);
            
            this.hideLoading();
            this.animateCards();
        } catch (error) {
            console.error('Erro ao carregar dados:', error);
            this.showError('Erro ao carregar dados do dashboard');
        }
    }

    async loadMetricas() {
        try {
            const response = await fetch(`/keychart/estatisticas/api/metricas/?periodo=${this.currentPeriod}`);
            const data = await response.json();
            
            if (data.success) {
                this.updateMetricasCards(data.metricas);
            }
        } catch (error) {
            console.error('Erro ao carregar métricas:', error);
        }
    }

    async loadGraficos() {
        try {
            const response = await fetch(`/keychart/estatisticas/api/graficos/?periodo=${this.currentPeriod}`);
            const data = await response.json();
            
            if (data.success) {
                this.updateCharts(data.graficos);
            }
        } catch (error) {
            console.error('Erro ao carregar gráficos:', error);
        }
    }

    async loadKPIs() {
        try {
            const response = await fetch(`/keychart/estatisticas/api/kpis/?periodo=${this.currentPeriod}`);
            const data = await response.json();
            
            if (data.success) {
                this.updateKPIs(data.kpis);
            }
        } catch (error) {
            console.error('Erro ao carregar KPIs:', error);
        }
    }

    async loadAlertas() {
        try {
            const response = await fetch('/keychart/estatisticas/api/alertas/');
            const data = await response.json();
            
            if (data.success) {
                this.updateAlertas(data.alertas);
            }
        } catch (error) {
            console.error('Erro ao carregar alertas:', error);
        }
    }

    updateMetricasCards(metricas) {
        Object.keys(metricas).forEach(key => {
            const card = document.querySelector(`[data-metrica="${key}"]`);
            if (card) {
                const valorElement = card.querySelector('.metrica-valor');
                const variacaoElement = card.querySelector('.metrica-variacao');
                
                if (valorElement) {
                    this.animateNumber(valorElement, metricas[key].valor);
                }
                
                if (variacaoElement && metricas[key].variacao !== undefined) {
                    const variacao = metricas[key].variacao;
                    const isPositive = variacao > 0;
                    const isNegative = variacao < 0;
                    
                    variacaoElement.innerHTML = `
                        <i class="bi bi-arrow-${isPositive ? 'up' : isNegative ? 'down' : 'right'}"></i>
                        ${Math.abs(variacao).toFixed(1)}%
                    `;
                    
                    variacaoElement.className = `metrica-variacao ${isPositive ? 'positiva' : isNegative ? 'negativa' : 'neutra'}`;
                }
            }
        });
    }

    updateCharts(graficosData) {
        // Gráfico de Competições
        if (graficosData.competicoes) {
            this.updateCompetitionsChart(graficosData.competicoes);
        }
        
        // Gráfico de Atletas
        if (graficosData.atletas) {
            this.updateAthletesChart(graficosData.atletas);
        }
        
        // Gráfico de Performance
        if (graficosData.performance) {
            this.updatePerformanceChart(graficosData.performance);
        }
    }

    updateCompetitionsChart(data) {
        const ctx = document.getElementById('competitionsChart')?.getContext('2d');
        if (!ctx) return;

        if (this.charts.competitions) {
            this.charts.competitions.destroy();
        }

        this.charts.competitions = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Competições Realizadas',
                    data: data.values,
                    borderColor: '#007bff',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
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
        });
    }

    updateAthletesChart(data) {
        const ctx = document.getElementById('athletesChart')?.getContext('2d');
        if (!ctx) return;

        if (this.charts.athletes) {
            this.charts.athletes.destroy();
        }

        this.charts.athletes = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.values,
                    backgroundColor: [
                        '#007bff',
                        '#28a745',
                        '#ffc107',
                        '#dc3545',
                        '#6f42c1'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true
                        }
                    }
                }
            }
        });
    }

    updatePerformanceChart(data) {
        const ctx = document.getElementById('performanceChart')?.getContext('2d');
        if (!ctx) return;

        if (this.charts.performance) {
            this.charts.performance.destroy();
        }

        this.charts.performance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Performance Score',
                    data: data.values,
                    backgroundColor: 'rgba(40, 167, 69, 0.8)',
                    borderColor: '#28a745',
                    borderWidth: 1,
                    borderRadius: 4
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
                    y: {
                        beginAtZero: true,
                        max: 100,
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
        });
    }

    updateKPIs(kpis) {
        Object.keys(kpis).forEach(key => {
            const kpiElement = document.querySelector(`[data-kpi="${key}"]`);
            if (kpiElement) {
                const valueElement = kpiElement.querySelector('.kpi-value');
                if (valueElement) {
                    this.animateNumber(valueElement, kpis[key].valor, kpis[key].formato);
                }
                
                const metaElement = kpiElement.querySelector('.kpi-meta');
                if (metaElement && kpis[key].meta) {
                    metaElement.textContent = `Meta: ${kpis[key].meta}`;
                }
            }
        });
    }

    updateAlertas(alertas) {
        const container = document.getElementById('alertasContainer');
        if (!container) return;

        if (alertas.length === 0) {
            container.innerHTML = `
                <div class="text-center text-muted py-4">
                    <i class="bi bi-check-circle" style="font-size: 3rem;"></i>
                    <p class="mt-2">Nenhum alerta no momento</p>
                </div>
            `;
            return;
        }

        container.innerHTML = alertas.map(alerta => `
            <div class="alerta-item ${alerta.tipo} fade-in">
                <div class="alerta-icon">
                    <i class="bi bi-${this.getAlertIcon(alerta.tipo)}"></i>
                </div>
                <div class="alerta-conteudo">
                    <div class="alerta-titulo">${alerta.titulo}</div>
                    <p class="alerta-descricao">${alerta.mensagem}</p>
                </div>
                <div class="alerta-timestamp">
                    ${this.formatTimestamp(alerta.created_at)}
                </div>
            </div>
        `).join('');
    }

    changePeriod(newPeriod) {
        // Atualizar botões
        document.querySelectorAll('.btn-periodo').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-periodo="${newPeriod}"]`)?.classList.add('active');
        
        this.currentPeriod = newPeriod;
        this.loadInitialData();
    }

    async applyFilters() {
        const filters = {};
        
        // Coletar valores dos filtros
        document.querySelectorAll('.filtro-grupo select, .filtro-grupo input').forEach(filter => {
            if (filter.value) {
                filters[filter.name] = filter.value;
            }
        });
        
        // Aplicar filtros
        const queryString = new URLSearchParams(filters).toString();
        await this.loadInitialData(queryString);
    }

    async refreshAllData() {
        const refreshBtn = document.getElementById('refreshData');
        if (refreshBtn) {
            refreshBtn.innerHTML = '<i class="bi bi-arrow-clockwise spin"></i>';
            refreshBtn.disabled = true;
        }
        
        await this.loadInitialData();
        
        if (refreshBtn) {
            refreshBtn.innerHTML = '<i class="bi bi-arrow-clockwise"></i>';
            refreshBtn.disabled = false;
        }
        
        this.showToast('Dados atualizados com sucesso!', 'success');
    }

    startAutoUpdate() {
        // Atualizar a cada 5 minutos
        this.updateInterval = setInterval(() => {
            this.loadInitialData();
        }, 5 * 60 * 1000);
    }

    stopAutoUpdate() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
    }

    resizeCharts() {
        Object.values(this.charts).forEach(chart => {
            if (chart && typeof chart.resize === 'function') {
                chart.resize();
            }
        });
    }

    animateNumber(element, targetValue, format = 'number') {
        const startValue = parseFloat(element.textContent.replace(/[^\d.-]/g, '')) || 0;
        const increment = (targetValue - startValue) / 20;
        let currentValue = startValue;
        
        const animate = () => {
            currentValue += increment;
            
            if ((increment > 0 && currentValue >= targetValue) || 
                (increment < 0 && currentValue <= targetValue)) {
                currentValue = targetValue;
            }
            
            element.textContent = this.formatValue(currentValue, format);
            
            if (currentValue !== targetValue) {
                requestAnimationFrame(animate);
            }
        };
        
        animate();
    }

    formatValue(value, format) {
        switch (format) {
            case 'percentage':
                return `${value.toFixed(1)}%`;
            case 'currency':
                return `R$ ${value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`;
            case 'integer':
                return Math.round(value).toLocaleString('pt-BR');
            default:
                return value.toLocaleString('pt-BR');
        }
    }

    animateCards() {
        const cards = document.querySelectorAll('.metrica-card, .grafico-card');
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('fade-in');
            }, index * 100);
        });
    }

    initializeAnimations() {
        // Intersection Observer para animações on scroll
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('slide-in');
                }
            });
        });

        document.querySelectorAll('.kpi-item, .alerta-item').forEach(el => {
            observer.observe(el);
        });
    }

    showLoading() {
        const loadingElements = document.querySelectorAll('.loading-placeholder');
        loadingElements.forEach(el => {
            el.style.display = 'block';
        });
    }

    hideLoading() {
        const loadingElements = document.querySelectorAll('.loading-placeholder');
        loadingElements.forEach(el => {
            el.style.display = 'none';
        });
    }

    showError(message) {
        this.showToast(message, 'error');
    }

    showToast(message, type = 'info') {
        // Criar toast notification
        const toast = document.createElement('div');
        toast.className = `toast-notification toast-${type}`;
        toast.innerHTML = `
            <i class="bi bi-${this.getToastIcon(type)}"></i>
            <span>${message}</span>
            <button class="toast-close">&times;</button>
        `;
        
        document.body.appendChild(toast);
        
        // Animar entrada
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Auto remover
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
        
        // Botão fechar
        toast.querySelector('.toast-close').addEventListener('click', () => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        });
    }

    getAlertIcon(tipo) {
        const icons = {
            'critico': 'exclamation-triangle-fill',
            'atencao': 'exclamation-circle-fill',
            'info': 'info-circle-fill'
        };
        return icons[tipo] || 'info-circle';
    }

    getToastIcon(type) {
        const icons = {
            'success': 'check-circle',
            'error': 'x-circle',
            'warning': 'exclamation-triangle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    formatTimestamp(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;
        
        if (diff < 60000) { // menos de 1 minuto
            return 'Agora mesmo';
        } else if (diff < 3600000) { // menos de 1 hora
            const minutes = Math.floor(diff / 60000);
            return `${minutes}m atrás`;
        } else if (diff < 86400000) { // menos de 1 dia
            const hours = Math.floor(diff / 3600000);
            return `${hours}h atrás`;
        } else {
            return date.toLocaleDateString('pt-BR');
        }
    }

    async exportData() {
        try {
            const response = await fetch('/keychart/estatisticas/api/export/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    periodo: this.currentPeriod,
                    formato: 'excel'
                })
            });
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `estatisticas_${new Date().toISOString().split('T')[0]}.xlsx`;
                a.click();
                window.URL.revokeObjectURL(url);
                
                this.showToast('Relatório exportado com sucesso!', 'success');
            } else {
                throw new Error('Erro ao exportar dados');
            }
        } catch (error) {
            console.error('Erro ao exportar:', error);
            this.showToast('Erro ao exportar relatório', 'error');
        }
    }

    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }

    destroy() {
        this.stopAutoUpdate();
        Object.values(this.charts).forEach(chart => {
            if (chart && typeof chart.destroy === 'function') {
                chart.destroy();
            }
        });
    }
}

// Inicializar dashboard quando DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    window.dashboardMain = new DashboardMain();
});

// Cleanup ao sair da página
window.addEventListener('beforeunload', () => {
    if (window.dashboardMain) {
        window.dashboardMain.destroy();
    }
});
