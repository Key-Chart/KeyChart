// Função para alternar a sidebar
function toggleSidebar() {
  const sidebar = document.getElementById("sidebar");
  const content = document.getElementById("content");

  sidebar.classList.toggle("sidebar-hidden");
  content.classList.toggle("content-expanded");
}

// Dropdown do usuário
document
  .querySelector(".user-icon-container")
  .addEventListener("click", function () {
    const dropdown = this.closest(".user-dropdown");
    dropdown.classList.toggle("active");
  });

// Fechar o menu ao clicar fora dele
document.addEventListener("click", function (event) {
  const dropdown = document.querySelector(".user-dropdown");
  if (!dropdown.contains(event.target)) {
    dropdown.classList.remove("active");
  }
});

// Navegação entre telas
function showScreenContent(contentId) {
  // Esconde todos os conteúdos
  document.querySelectorAll("[data-screen-content]").forEach((content) => {
    content.style.display = "none";
  });

  // Mostra o conteúdo selecionado
  document.getElementById(contentId + "-screen").style.display = "block";

  // Atualiza o título da tela
  const titles = {
    dashboard: '<i class="fas fa-home"></i> Dashboard',
    perfil: '<i class="fas fa-user"></i> Meu Perfil',
    estatisticas: '<i class="fas fa-chart-bar"></i> Estatísticas',
    desempenho: '<i class="fas fa-tachometer-alt"></i> Desempenho',
    competicoes: '<i class="fas fa-trophy"></i> Competições',
    resultados: '<i class="fas fa-clipboard-list"></i> Resultados',
    notificacoes: '<i class="fas fa-bell"></i> Notificações',
    configuracoes: '<i class="fas fa-cog"></i> Configurações',
  };

  document.getElementById("screen-title").innerHTML = titles[contentId] || "";
}

// Configura os listeners de navegação
document.querySelectorAll("[data-screen]").forEach((link) => {
  link.addEventListener("click", function (e) {
    e.preventDefault();
    showScreenContent(this.getAttribute("data-screen"));
  });
});

document.querySelectorAll("[data-settings-tab]").forEach((tab) => {
  tab.addEventListener("click", function (e) {
    e.preventDefault();

    // Remove a classe active de todas as tabs
    document.querySelectorAll("[data-settings-tab]").forEach((t) => {
      t.classList.remove("active");
    });

    // Adiciona a classe active na tab clicada
    this.classList.add("active");

    // Esconde todos os conteúdos de settings
    document.querySelectorAll(".settings-section").forEach((section) => {
      section.style.display = "none";
    });

    // Mostra o conteúdo correspondente
    const tabId = this.getAttribute("data-settings-tab");
    document.getElementById(tabId + "-settings").style.display = "block";

    // Atualiza o título
    const titles = {
      profile: "Configurações de Perfil",
      security: "Segurança e Privacidade",
      notifications: "Configurações de Notificação",
      privacy: "Privacidade e Dados",
    };

    document.getElementById("settings-tab-title").textContent =
      titles[tabId] || "Configurações";
  });
});

// Inicialização
document.addEventListener("DOMContentLoaded", function () {
  // Inicializa os gráficos
  initCharts();
});

// Gráficos
function initCharts() {
  // Gráfico de desempenho no dashboard
  const dashboardPerformanceCtx = document
    .getElementById("dashboardPerformanceChart")
    .getContext("2d");
  new Chart(dashboardPerformanceCtx, {
    type: "line",
    data: {
      labels: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"],
      datasets: [
        {
          label: "Pontuação Média",
          data: [72, 75, 78, 80, 82, 85],
          borderColor: "#007bff",
          backgroundColor: "rgba(0, 123, 255, 0.1)",
          fill: true,
          tension: 0.4,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: false,
        },
      },
      scales: {
        y: {
          beginAtZero: false,
          min: 50,
          max: 100,
        },
      },
    },
  });

  // Gráfico de desempenho
  const performanceCtx = document
    .getElementById("performanceChart")
    .getContext("2d");
  new Chart(performanceCtx, {
    type: "line",
    data: {
      labels: [
        "Jan",
        "Fev",
        "Mar",
        "Abr",
        "Mai",
        "Jun",
        "Jul",
        "Ago",
        "Set",
        "Out",
        "Nov",
        "Dez",
      ],
      datasets: [
        {
          label: "Pontuação Média",
          data: [65, 59, 70, 72, 75, 73, 78, 80, 82, 85, 83, 88],
          borderColor: "#007bff",
          backgroundColor: "rgba(0, 123, 255, 0.1)",
          fill: true,
          tension: 0.4,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "top",
        },
        tooltip: {
          mode: "index",
          intersect: false,
        },
      },
      scales: {
        y: {
          beginAtZero: false,
          min: 50,
          max: 100,
        },
      },
    },
  });

  // Gráfico por categoria
  const categoryCtx = document.getElementById("categoryChart").getContext("2d");
  new Chart(categoryCtx, {
    type: "bar",
    data: {
      labels: ["Kata", "Kumite", "Físico", "Técnica", "Estratégia"],
      datasets: [
        {
          label: "Pontuação",
          data: [85, 78, 82, 88, 75],
          backgroundColor: [
            "rgba(255, 99, 132, 0.7)",
            "rgba(54, 162, 235, 0.7)",
            "rgba(255, 206, 86, 0.7)",
            "rgba(75, 192, 192, 0.7)",
            "rgba(153, 102, 255, 0.7)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: false,
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
        },
      },
    },
  });

  // Gráfico de distribuição de resultados
  const resultsDistributionCtx = document
    .getElementById("resultsDistributionChart")
    .getContext("2d");
  new Chart(resultsDistributionCtx, {
    type: "doughnut",
    data: {
      labels: ["Vitórias", "Derrotas", "Empates"],
      datasets: [
        {
          data: [18, 5, 1],
          backgroundColor: [
            "rgba(40, 167, 69, 0.7)",
            "rgba(220, 53, 69, 0.7)",
            "rgba(108, 117, 125, 0.7)",
          ],
          borderColor: [
            "rgba(40, 167, 69, 1)",
            "rgba(220, 53, 69, 1)",
            "rgba(108, 117, 125, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "bottom",
        },
      },
    },
  });

  // Gráfico de progresso anual (continuação)
  new Chart(annualProgressCtx, {
    type: "radar",
    data: {
      labels: [
        "Força",
        "Velocidade",
        "Resistência",
        "Técnica",
        "Flexibilidade",
        "Estratégia",
      ],
      datasets: [
        {
          label: "2024",
          data: [70, 75, 65, 80, 60, 70],
          backgroundColor: "rgba(108, 117, 125, 0.2)",
          borderColor: "rgba(108, 117, 125, 1)",
          borderWidth: 1,
          pointBackgroundColor: "rgba(108, 117, 125, 1)",
        },
        {
          label: "2025",
          data: [85, 92, 78, 88, 65, 75],
          backgroundColor: "rgba(0, 123, 255, 0.2)",
          borderColor: "rgba(0, 123, 255, 1)",
          borderWidth: 1,
          pointBackgroundColor: "rgba(0, 123, 255, 1)",
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        r: {
          angleLines: {
            display: true,
          },
          suggestedMin: 0,
          suggestedMax: 100,
        },
      },
    },
  });
}
