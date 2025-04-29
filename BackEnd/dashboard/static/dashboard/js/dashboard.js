
// Função para expandir ou recolher o chat
function toggleChat() {
    const chatContainer = document.getElementById('chatContainer');
    chatContainer.classList.toggle('collapsed');
}

// Gráfico de barras mostrando o ranking de equipes
var ctx1 = document.getElementById('rankingChart').getContext('2d');
new Chart(ctx1, {
    type: 'bar', // Tipo do gráfico: barras
    data: {
        labels: ['Equipe A', 'Equipe B', 'Equipe C', 'Equipe D'], // Labels no eixo X
        datasets: [{
            label: 'Pontos', // Nome do conjunto de dados
            data: [50, 42, 38, 36], // Pontuação das equipes
            backgroundColor: ['#007bff', '#28a745', '#ffc107', '#dc3545'] // Cores das barras
        }]
    }
});

// Gráfico de linhas mostrando o desempenho de atletas
var ctx2 = document.getElementById('goalsChart').getContext('2d');
new Chart(ctx2, {
    type: 'line', // Tipo do gráfico: linha
    data: {
        labels: ['Atleta 1', 'Atleta 2', 'Atleta 3', 'Atleta 4'], // Labels no eixo X
        datasets: [{
            label: 'Pontos', // Nome do conjunto de dados
            data: [2, 4, 3, 5], // Pontuação dos atletas
            borderColor: '#007bff', // Cor da linha
            fill: false // Não preencher abaixo da linha
        }]
    }
});

// Evento para abrir/fechar o dropdown do usuário ao clicar no ícone
document.querySelector('.user-icon-container').addEventListener('click', function () {
    const dropdown = this.closest('.user-dropdown');
    dropdown.classList.toggle('active');
});

// Evento para fechar o dropdown ao clicar fora dele
document.addEventListener('click', function (event) {
    const dropdown = document.querySelector('.user-dropdown');
    if (!dropdown.contains(event.target)) {
        dropdown.classList.remove('active');
    }
});
