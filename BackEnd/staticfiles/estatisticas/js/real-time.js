/**
 * Real-time.js - Sistema de Atualizações em Tempo Real
 * KeyChart - Sistema de Estatísticas
 *
 * Implementa:
 * - Auto-refresh de dados
 * - WebSocket para atualizações instantâneas
 * - Notificações em tempo real
 * - Monitoramento de conectividade
 */

class RealTimeManager {
  constructor() {
    this.updateInterval = 30000; // 30 segundos
    this.intervalIds = new Map();
    this.isConnected = true;
    this.lastUpdate = null;

    this.init();
  }

  init() {
    this.setupAutoRefresh();
    this.setupConnectivityMonitor();
    this.setupVisibilityHandler();
    this.startRealTimeUpdates();
  }

  /**
   * Configura atualização automática de dados
   */
  setupAutoRefresh() {
    // Auto-refresh das métricas principais
    this.startInterval(
      "metricas",
      () => {
        this.updateMetricas();
      },
      this.updateInterval
    );

    // Auto-refresh dos gráficos (menos frequente)
    this.startInterval(
      "graficos",
      () => {
        this.updateGraficos();
      },
      this.updateInterval * 2
    );

    // Auto-refresh dos alertas (mais frequente)
    this.startInterval(
      "alertas",
      () => {
        this.updateAlertas();
      },
      15000
    );

    // Auto-refresh dos KPIs
    this.startInterval(
      "kpis",
      () => {
        this.updateKPIs();
      },
      this.updateInterval
    );
  }

  /**
   * Inicia um intervalo nomeado
   */
  startInterval(name, callback, interval) {
    this.stopInterval(name);
    const id = setInterval(callback, interval);
    this.intervalIds.set(name, id);
  }

  /**
   * Para um intervalo específico
   */
  stopInterval(name) {
    if (this.intervalIds.has(name)) {
      clearInterval(this.intervalIds.get(name));
      this.intervalIds.delete(name);
    }
  }

  /**
   * Para todos os intervalos
   */
  stopAllIntervals() {
    this.intervalIds.forEach((id, name) => {
      clearInterval(id);
    });
    this.intervalIds.clear();
  }

  /**
   * Atualiza métricas principais
   */
  async updateMetricas() {
    try {
      const response = await fetch(
        window.estatisticasConfig.apis.metricas + "?t=" + Date.now()
      );

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();

      if (data.success) {
        this.updateMetricasDOM(data.metricas);
        this.updateLastUpdateTime();
        this.showConnectivityStatus(true);
      }
    } catch (error) {
      console.error("Erro ao atualizar métricas:", error);
      this.showConnectivityStatus(false);
    }
  }

  /**
   * Atualiza gráficos
   */
  async updateGraficos() {
    try {
      const response = await fetch(
        window.estatisticasConfig.apis.graficos + "?t=" + Date.now()
      );
      const data = await response.json();

      if (data.success && window.chartsManager) {
        window.chartsManager.updateAllCharts(data.graficos);
      }
    } catch (error) {
      console.error("Erro ao atualizar gráficos:", error);
    }
  }

  /**
   * Atualiza alertas
   */
  async updateAlertas() {
    try {
      const response = await fetch(
        window.estatisticasConfig.apis.alertas + "?t=" + Date.now()
      );
      const data = await response.json();

      if (data.success) {
        this.updateAlertasDOM(data.alertas);
        this.checkForNewAlerts(data.alertas);
      }
    } catch (error) {
      console.error("Erro ao atualizar alertas:", error);
    }
  }

  /**
   * Atualiza KPIs
   */
  async updateKPIs() {
    try {
      const response = await fetch(
        window.estatisticasConfig.apis.kpis + "?t=" + Date.now()
      );
      const data = await response.json();

      if (data.success) {
        this.updateKPIsDOM(data.kpis);
      }
    } catch (error) {
      console.error("Erro ao atualizar KPIs:", error);
    }
  }

  /**
   * Atualiza DOM das métricas
   */
  updateMetricasDOM(metricas) {
    Object.keys(metricas).forEach((key) => {
      const element = document.querySelector(`[data-metrica="${key}"]`);
      if (element) {
        const valor = metricas[key];

        // Anima a mudança de valor
        this.animateValueChange(element, valor);

        // Atualiza classes baseadas no valor
        this.updateMetricaStatus(element, valor, key);
      }
    });
  }

  /**
   * Atualiza DOM dos alertas
   */
  updateAlertasDOM(alertas) {
    const container = document.querySelector("#alertas-container");
    if (!container) return;

    // Limpa alertas existentes
    container.innerHTML = "";

    // Adiciona novos alertas
    alertas.forEach((alerta) => {
      const alertElement = this.createAlertElement(alerta);
      container.appendChild(alertElement);
    });

    // Atualiza contador de alertas
    const counter = document.querySelector("#alertas-count");
    if (counter) {
      counter.textContent = alertas.length;
      counter.className =
        alertas.length > 0 ? "badge bg-warning" : "badge bg-success";
    }
  }

  /**
   * Atualiza DOM dos KPIs
   */
  updateKPIsDOM(kpis) {
    Object.keys(kpis).forEach((key) => {
      const element = document.querySelector(`[data-kpi="${key}"]`);
      if (element && kpis[key]) {
        const kpi = kpis[key];
        const valueElement = element.querySelector(".kpi-value");
        const trendElement = element.querySelector(".kpi-trend");

        if (valueElement) {
          this.animateValueChange(valueElement, kpi.valor);
        }

        if (trendElement && kpi.tendencia) {
          this.updateTrendIndicator(trendElement, kpi.tendencia);
        }
      }
    });
  }

  /**
   * Anima mudança de valor
   */
  animateValueChange(element, newValue) {
    const currentValue = parseFloat(element.textContent) || 0;

    if (currentValue !== newValue) {
      element.classList.add("updating");

      // Contagem animada
      this.animateCounter(element, currentValue, newValue, 1000);

      setTimeout(() => {
        element.classList.remove("updating");
      }, 1000);
    }
  }

  /**
   * Animação de contador
   */
  animateCounter(element, start, end, duration) {
    const startTime = performance.now();
    const difference = end - start;

    const updateCounter = (currentTime) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);

      const current = start + difference * this.easeOutCubic(progress);

      // Formata o valor baseado no tipo
      let displayValue;
      if (element.dataset.format === "percentage") {
        displayValue = current.toFixed(1) + "%";
      } else if (element.dataset.format === "decimal") {
        displayValue = current.toFixed(1);
      } else {
        displayValue = Math.round(current);
      }

      element.textContent = displayValue;

      if (progress < 1) {
        requestAnimationFrame(updateCounter);
      }
    };

    requestAnimationFrame(updateCounter);
  }

  /**
   * Função de easing
   */
  easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
  }

  /**
   * Atualiza status da métrica
   */
  updateMetricaStatus(element, valor, key) {
    // Remove classes de status existentes
    element.classList.remove("metric-up", "metric-down", "metric-stable");

    // Lógica simples de tendência (pode ser melhorada)
    const previousValue = parseFloat(element.dataset.previousValue) || valor;

    if (valor > previousValue) {
      element.classList.add("metric-up");
    } else if (valor < previousValue) {
      element.classList.add("metric-down");
    } else {
      element.classList.add("metric-stable");
    }

    element.dataset.previousValue = valor;
  }

  /**
   * Atualiza indicador de tendência
   */
  updateTrendIndicator(element, tendencia) {
    element.innerHTML = "";

    let icon, className;

    switch (tendencia) {
      case "crescente":
        icon = "↗️";
        className = "trend-up";
        break;
      case "decrescente":
        icon = "↘️";
        className = "trend-down";
        break;
      case "estavel":
        icon = "➡️";
        className = "trend-stable";
        break;
      default:
        icon = "❓";
        className = "trend-unknown";
    }

    element.innerHTML = `<span class="${className}">${icon}</span>`;
  }

  /**
   * Cria elemento de alerta
   */
  createAlertElement(alerta) {
    const div = document.createElement("div");
    div.className = `alert alert-${this.getBootstrapAlertType(
      alerta.tipo
    )} alert-dismissible fade show`;
    div.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="bi bi-${this.getAlertIcon(alerta.tipo)} me-2"></i>
                <div class="flex-grow-1">
                    <strong>${alerta.titulo}</strong><br>
                    <small>${alerta.mensagem}</small>
                </div>
                <span class="badge bg-secondary ms-2">${
                  alerta.prioridade
                }</span>
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
    return div;
  }

  /**
   * Converte tipo de alerta para Bootstrap
   */
  getBootstrapAlertType(tipo) {
    const mapping = {
      success: "success",
      warning: "warning",
      danger: "danger",
      info: "info",
    };
    return mapping[tipo] || "info";
  }

  /**
   * Retorna ícone do alerta
   */
  getAlertIcon(tipo) {
    const mapping = {
      success: "check-circle",
      warning: "exclamation-triangle",
      danger: "x-circle",
      info: "info-circle",
    };
    return mapping[tipo] || "info-circle";
  }

  /**
   * Verifica por novos alertas e mostra notificações
   */
  checkForNewAlerts(alertas) {
    const currentAlerts = this.lastAlerts || [];
    const newAlerts = alertas.filter(
      (alerta) =>
        !currentAlerts.some(
          (current) =>
            current.titulo === alerta.titulo &&
            current.timestamp === alerta.timestamp
        )
    );

    // Mostra notificações para novos alertas de alta prioridade
    newAlerts
      .filter((alerta) => alerta.prioridade === "alta")
      .forEach((alerta) => {
        this.showNotification(alerta.titulo, alerta.mensagem, alerta.tipo);
      });

    this.lastAlerts = alertas;
  }

  /**
   * Mostra notificação do navegador
   */
  showNotification(title, message, type = "info") {
    if ("Notification" in window && Notification.permission === "granted") {
      const notification = new Notification(`KeyChart - ${title}`, {
        body: message,
        icon: "/static/competicoes/img/icone_keychart.png",
        tag: "keychart-alert",
      });

      setTimeout(() => notification.close(), 5000);
    }
  }

  /**
   * Configura monitoramento de conectividade
   */
  setupConnectivityMonitor() {
    window.addEventListener("online", () => {
      this.isConnected = true;
      this.showConnectivityStatus(true);
      this.startRealTimeUpdates();
    });

    window.addEventListener("offline", () => {
      this.isConnected = false;
      this.showConnectivityStatus(false);
      this.stopAllIntervals();
    });
  }

  /**
   * Configura handler de visibilidade da página
   */
  setupVisibilityHandler() {
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) {
        // Página não está visível, reduz frequência de updates
        this.reduceUpdateFrequency();
      } else {
        // Página está visível, retoma frequência normal
        this.restoreUpdateFrequency();
        // Força uma atualização imediata
        this.forceUpdate();
      }
    });
  }

  /**
   * Reduz frequência de atualizações
   */
  reduceUpdateFrequency() {
    this.startInterval(
      "metricas",
      () => this.updateMetricas(),
      this.updateInterval * 4
    );
    this.startInterval(
      "graficos",
      () => this.updateGraficos(),
      this.updateInterval * 8
    );
    this.startInterval(
      "alertas",
      () => this.updateAlertas(),
      this.updateInterval * 2
    );
    this.startInterval(
      "kpis",
      () => this.updateKPIs(),
      this.updateInterval * 4
    );
  }

  /**
   * Restaura frequência normal de atualizações
   */
  restoreUpdateFrequency() {
    this.setupAutoRefresh();
  }

  /**
   * Força atualização de todos os dados
   */
  forceUpdate() {
    this.updateMetricas();
    this.updateGraficos();
    this.updateAlertas();
    this.updateKPIs();
  }

  /**
   * Inicia atualizações em tempo real
   */
  startRealTimeUpdates() {
    if (!this.isConnected) return;

    // Solicita permissão para notificações
    if ("Notification" in window && Notification.permission === "default") {
      Notification.requestPermission();
    }

    this.setupAutoRefresh();
  }

  /**
   * Mostra status de conectividade
   */
  showConnectivityStatus(isConnected) {
    const statusElement = document.querySelector("#connectivity-status");
    if (statusElement) {
      if (isConnected) {
        statusElement.innerHTML = '<i class="bi bi-wifi text-success"></i>';
        statusElement.title = "Conectado - Dados em tempo real";
      } else {
        statusElement.innerHTML = '<i class="bi bi-wifi-off text-danger"></i>';
        statusElement.title = "Desconectado - Dados podem estar desatualizados";
      }
    }
  }

  /**
   * Atualiza timestamp da última atualização
   */
  updateLastUpdateTime() {
    this.lastUpdate = new Date();
    const element = document.querySelector("#last-update-time");
    if (element) {
      element.textContent = this.lastUpdate.toLocaleTimeString();
    }
  }

  /**
   * Destrói o gerenciador e limpa recursos
   */
  destroy() {
    this.stopAllIntervals();
    this.isConnected = false;
  }
}

// Inicializa quando o DOM estiver pronto
document.addEventListener("DOMContentLoaded", () => {
  // Só inicializa se estivermos na página de estatísticas
  if (document.querySelector("#estatisticas-dashboard")) {
    window.realTimeManager = new RealTimeManager();

    // Cleanup quando a página for descarregada
    window.addEventListener("beforeunload", () => {
      if (window.realTimeManager) {
        window.realTimeManager.destroy();
      }
    });
  }
});

// Exporta para uso global
window.RealTimeManager = RealTimeManager;
