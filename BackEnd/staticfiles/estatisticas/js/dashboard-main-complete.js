// Dashboard Principal - KeyChart Estatísticas (Versão Completa)
class DashboardMainComplete {
  constructor() {
    this.charts = {};
    this.updateInterval = null;
    this.currentPeriod = "7d";
    this.autoRefresh = false;
    this.init();
  }

  init() {
    this.setupEventListeners();
    this.loadInitialData();
    this.initializeAnimations();
  }

  setupEventListeners() {
    // Botão refresh
    document.getElementById("refreshData")?.addEventListener("click", () => {
      this.refreshAllData();
    });

    // Auto refresh toggle
    const autoRefreshBtn = document.querySelector(
      'button[onclick="toggleAutoRefresh()"]'
    );
    if (autoRefreshBtn) {
      autoRefreshBtn.onclick = () => this.toggleAutoRefresh();
    }

    // Export dropdown
    document.querySelectorAll('[onclick*="exportDashboard"]').forEach((btn) => {
      const match = btn
        .getAttribute("onclick")
        .match(/exportDashboard\('(\w+)'\)/);
      if (match) {
        btn.onclick = (e) => {
          e.preventDefault();
          this.exportDashboard(match[1]);
        };
      }
    });

    // Resize handler para gráficos
    window.addEventListener("resize", () => {
      this.resizeCharts();
    });
  }

  async loadInitialData() {
    this.showLoading();

    try {
      // Simular dados (em produção virá da API)
      const data = this.getMockData();

      // Inicializar todos os gráficos
      this.initializeAllCharts(data);

      // Atualizar timestamp
      this.updateLastUpdate();
    } catch (error) {
      console.error("Erro ao carregar dados:", error);
      this.showError("Erro ao carregar dados do dashboard");
    } finally {
      this.hideLoading();
    }
  }

  getMockData() {
    return {
      evolucao_atletas: {
        labels: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"],
        datasets: [
          {
            label: "Atletas Cadastrados",
            data: [150, 180, 220, 280, 320, 380],
            borderColor: "#3498db",
            backgroundColor: "rgba(52, 152, 219, 0.1)",
            fill: true,
            tension: 0.4,
          },
        ],
      },
      distribuicao_sexo: {
        labels: ["Masculino", "Feminino"],
        datasets: [
          {
            data: [65, 35],
            backgroundColor: ["#3498db", "#e74c3c"],
            borderWidth: 0,
          },
        ],
      },
      distribuicao_categoria: {
        labels: ["Infantil", "Juvenil", "Adulto", "Master"],
        datasets: [
          {
            data: [25, 30, 35, 10],
            backgroundColor: ["#f39c12", "#27ae60", "#8e44ad", "#e67e22"],
            borderWidth: 0,
          },
        ],
      },
      competicoes_timeline: {
        labels: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"],
        datasets: [
          {
            label: "Competições Realizadas",
            data: [8, 12, 15, 18, 22, 25],
            borderColor: "#27ae60",
            backgroundColor: "rgba(39, 174, 96, 0.1)",
            fill: true,
          },
        ],
      },
      modalidades_stats: {
        labels: ["Kata", "Kumite", "Kobudo"],
        datasets: [
          {
            data: [40, 45, 15],
            backgroundColor: ["#9b59b6", "#3498db", "#f39c12"],
          },
        ],
      },
      progressao_faixas: {
        labels: [
          "Branca",
          "Amarela",
          "Laranja",
          "Verde",
          "Azul",
          "Marrom",
          "Preta",
        ],
        datasets: [
          {
            label: "Quantidade de Atletas",
            data: [45, 38, 32, 28, 22, 15, 8],
            backgroundColor: [
              "#ecf0f1",
              "#f1c40f",
              "#e67e22",
              "#27ae60",
              "#3498db",
              "#8b4513",
              "#2c3e50",
            ],
          },
        ],
      },
      crescimento_regional: {
        labels: ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"],
        datasets: [
          {
            label: "Crescimento %",
            data: [15, 22, 18, 35, 28],
            backgroundColor: "rgba(52, 152, 219, 0.8)",
          },
        ],
      },
      comparativo_periodo: {
        labels: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"],
        datasets: [
          {
            label: "2024",
            data: [20, 25, 30, 35, 40, 45],
            borderColor: "#3498db",
            backgroundColor: "rgba(52, 152, 219, 0.1)",
          },
          {
            label: "2025",
            data: [25, 32, 38, 42, 48, 55],
            borderColor: "#27ae60",
            backgroundColor: "rgba(39, 174, 96, 0.1)",
          },
        ],
      },
      projecoes: {
        labels: ["Jul", "Ago", "Set", "Out", "Nov", "Dez"],
        datasets: [
          {
            label: "Projeção de Crescimento",
            data: [60, 68, 75, 82, 90, 100],
            borderColor: "#e74c3c",
            backgroundColor: "rgba(231, 76, 60, 0.1)",
            borderDash: [5, 5],
          },
        ],
      },
    };
  }

  initializeAllCharts(data) {
    // Gráficos principais
    this.initializeEvolucaoChart(data.evolucao_atletas);
    this.initializeSexoChart(data.distribuicao_sexo);
    this.initializeCategoriaChart(data.distribuicao_categoria);

    // Gráficos de competições
    this.initializeTimelineChart(data.competicoes_timeline);
    this.initializeModalidadeChart(data.modalidades_stats);

    // Gráficos de atletas
    this.initializeFaixasChart(data.progressao_faixas);

    // Gráficos de academias
    this.initializeCrescimentoRegionalChart(data.crescimento_regional);

    // Gráficos comparativos
    this.initializeComparativoChart(data.comparativo_periodo);
    this.initializeProjecoesChart(data.projecoes);
  }

  initializeEvolucaoChart(data) {
    const ctx = document.getElementById("evolucaoChart");
    if (!ctx) return;

    if (this.charts.evolucao) {
      this.charts.evolucao.destroy();
    }

    this.charts.evolucao = new Chart(ctx, {
      type: "line",
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: "rgba(0, 0, 0, 0.1)",
            },
          },
          x: {
            grid: {
              display: false,
            },
          },
        },
      },
    });
  }

  initializeSexoChart(data) {
    const ctx = document.getElementById("sexoChart");
    if (!ctx) return;

    if (this.charts.sexo) {
      this.charts.sexo.destroy();
    }

    this.charts.sexo = new Chart(ctx, {
      type: "doughnut",
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
          },
        },
      },
    });
  }

  initializeCategoriaChart(data) {
    const ctx = document.getElementById("categoriaChart");
    if (!ctx) return;

    if (this.charts.categoria) {
      this.charts.categoria.destroy();
    }

    this.charts.categoria = new Chart(ctx, {
      type: "doughnut",
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
          },
        },
      },
    });
  }

  initializeTimelineChart(data) {
    const ctx = document.getElementById("competicoesTimelineChart");
    if (!ctx) return;

    if (this.charts.timeline) {
      this.charts.timeline.destroy();
    }

    this.charts.timeline = new Chart(ctx, {
      type: "line",
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }

  initializeModalidadeChart(data) {
    const ctx = document.getElementById("modalidadeChart");
    if (!ctx) return;

    if (this.charts.modalidade) {
      this.charts.modalidade.destroy();
    }

    this.charts.modalidade = new Chart(ctx, {
      type: "pie",
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
          },
        },
      },
    });
  }

  initializeFaixasChart(data) {
    const ctx = document.getElementById("faixasChart");
    if (!ctx) return;

    if (this.charts.faixas) {
      this.charts.faixas.destroy();
    }

    this.charts.faixas = new Chart(ctx, {
      type: "bar",
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }

  initializeCrescimentoRegionalChart(data) {
    const ctx = document.getElementById("crescimentoRegionalChart");
    if (!ctx) return;

    if (this.charts.crescimentoRegional) {
      this.charts.crescimentoRegional.destroy();
    }

    this.charts.crescimentoRegional = new Chart(ctx, {
      type: "bar",
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }

  initializeComparativoChart(data) {
    const ctx = document.getElementById("comparativoChart");
    if (!ctx) return;

    if (this.charts.comparativo) {
      this.charts.comparativo.destroy();
    }

    this.charts.comparativo = new Chart(ctx, {
      type: "line",
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }

  initializeProjecoesChart(data) {
    const ctx = document.getElementById("projecoesChart");
    if (!ctx) return;

    if (this.charts.projecoes) {
      this.charts.projecoes.destroy();
    }

    this.charts.projecoes = new Chart(ctx, {
      type: "line",
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }

  toggleAutoRefresh() {
    this.autoRefresh = !this.autoRefresh;
    const icon = document.getElementById("autoRefreshIcon");
    const text = document.getElementById("autoRefreshText");

    if (this.autoRefresh) {
      icon.className = "bi bi-pause-circle me-1";
      text.textContent = "Pausar";
      this.startAutoUpdate();
    } else {
      icon.className = "bi bi-play-circle me-1";
      text.textContent = "Auto Refresh";
      this.stopAutoUpdate();
    }
  }

  startAutoUpdate() {
    if (this.updateInterval) {
      clearInterval(this.updateInterval);
    }

    // Atualizar a cada 30 segundos quando auto refresh estiver ativo
    this.updateInterval = setInterval(() => {
      this.refreshAllData();
    }, 30000);
  }

  stopAutoUpdate() {
    if (this.updateInterval) {
      clearInterval(this.updateInterval);
      this.updateInterval = null;
    }
  }

  async refreshAllData() {
    const refreshBtn = document.getElementById("refreshData");
    if (refreshBtn) {
      const originalContent = refreshBtn.innerHTML;
      refreshBtn.innerHTML =
        '<i class="bi bi-arrow-clockwise spin me-1"></i>Atualizando...';
      refreshBtn.disabled = true;
    }

    try {
      await this.loadInitialData();
      this.showToast("Dados atualizados com sucesso!", "success");
    } catch (error) {
      this.showToast("Erro ao atualizar dados", "error");
    } finally {
      if (refreshBtn) {
        refreshBtn.innerHTML =
          '<i class="bi bi-arrow-clockwise me-1"></i>Atualizar';
        refreshBtn.disabled = false;
      }
    }
  }

  exportDashboard(format) {
    try {
      // Simular exportação
      this.showToast(
        `Exportando dashboard em formato ${format.toUpperCase()}...`,
        "info"
      );

      setTimeout(() => {
        this.showToast(`Dashboard exportado com sucesso!`, "success");
      }, 2000);
    } catch (error) {
      console.error("Erro ao exportar:", error);
      this.showToast("Erro ao exportar dashboard", "error");
    }
  }

  resizeCharts() {
    Object.values(this.charts).forEach((chart) => {
      if (chart && typeof chart.resize === "function") {
        chart.resize();
      }
    });
  }

  updateLastUpdate() {
    const elements = document.querySelectorAll(".ultima-atualizacao");
    const now = new Date().toLocaleString("pt-BR");
    elements.forEach((el) => {
      el.textContent = `Última atualização: ${now}`;
    });
  }

  initializeAnimations() {
    // Intersection Observer para animações
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("animate__fadeInUp");
        }
      });
    });

    document.querySelectorAll(".stat-card, .chart-card").forEach((el) => {
      observer.observe(el);
    });
  }

  showLoading() {
    // Mostrar skeleton loaders
    document.querySelectorAll(".chart-container").forEach((container) => {
      const canvas = container.querySelector("canvas");
      if (canvas) {
        canvas.style.opacity = "0.5";
      }
    });
  }

  hideLoading() {
    // Esconder skeleton loaders
    document.querySelectorAll(".chart-container").forEach((container) => {
      const canvas = container.querySelector("canvas");
      if (canvas) {
        canvas.style.opacity = "1";
      }
    });
  }

  showError(message) {
    this.showToast(message, "error");
  }

  showToast(message, type = "info") {
    // Criar toast notification
    const toast = document.createElement("div");
    toast.className = `toast align-items-center text-white bg-${this.getBootstrapColorForType(
      type
    )} border-0 position-fixed`;
    toast.style.cssText = "top: 20px; right: 20px; z-index: 9999;";
    toast.setAttribute("role", "alert");
    toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi bi-${this.getIconForType(type)} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;

    document.body.appendChild(toast);

    // Inicializar bootstrap toast
    const bsToast = new bootstrap.Toast(toast, {
      autohide: true,
      delay: 3000,
    });

    bsToast.show();

    // Remover elemento após esconder
    toast.addEventListener("hidden.bs.toast", () => {
      toast.remove();
    });
  }

  getBootstrapColorForType(type) {
    const colors = {
      success: "success",
      error: "danger",
      warning: "warning",
      info: "info",
    };
    return colors[type] || "info";
  }

  getIconForType(type) {
    const icons = {
      success: "check-circle",
      error: "x-circle",
      warning: "exclamation-triangle",
      info: "info-circle",
    };
    return icons[type] || "info-circle";
  }

  destroy() {
    this.stopAutoUpdate();
    Object.values(this.charts).forEach((chart) => {
      if (chart && typeof chart.destroy === "function") {
        chart.destroy();
      }
    });
  }
}

// Funções globais para compatibilidade com o template
function toggleAutoRefresh() {
  if (window.dashboardMain) {
    window.dashboardMain.toggleAutoRefresh();
  }
}

function exportDashboard(format) {
  if (window.dashboardMain) {
    window.dashboardMain.exportDashboard(format);
  }
}

// Inicializar dashboard quando DOM estiver carregado
document.addEventListener("DOMContentLoaded", () => {
  window.dashboardMain = new DashboardMainComplete();
});

// Cleanup ao sair da página
window.addEventListener("beforeunload", () => {
  if (window.dashboardMain) {
    window.dashboardMain.destroy();
  }
});

// CSS adicional para animações
const additionalStyles = `
<style>
.spin {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.chart-container canvas {
    transition: opacity 0.3s ease;
}

.toast {
    min-width: 300px;
}
</style>
`;

document.head.insertAdjacentHTML("beforeend", additionalStyles);
