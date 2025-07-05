
// Função para expandir ou recolher o chat
function toggleChat() {
    const chatContainer = document.getElementById('chatContainer');
    const chatWindow = document.getElementById('chatWindow');
    
    if (chatContainer.classList.contains('collapsed')) {
        chatContainer.classList.remove('collapsed');
        chatWindow.style.display = 'flex';
    } else {
        chatContainer.classList.add('collapsed');
        chatWindow.style.display = 'none';
    }
}

// Função para inicializar os gráficos quando os dados estiverem disponíveis
function initCharts() {
    // Verificar se os dados estão disponíveis
    if (typeof dashboardData === 'undefined') {
        console.warn('Dados do dashboard não estão disponíveis');
        return;
    }

    // Gráfico de barras - Top Academias
    const ctx1 = document.getElementById('rankingChart');
    if (ctx1 && dashboardData.academias && dashboardData.academias.length > 0) {
        new Chart(ctx1, {
            type: 'bar',
            data: {
                labels: dashboardData.academias.map(a => a.nome),
                datasets: [{
                    label: 'Número de Atletas',
                    data: dashboardData.academias.map(a => a.total),
                    backgroundColor: [
                        '#007bff', '#28a745', '#ffc107', '#dc3545', 
                        '#6f42c1', '#fd7e14', '#20c997', '#e83e8c'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }

    // Gráfico de linha - Inscrições por mês
    const ctx2 = document.getElementById('goalsChart');
    if (ctx2 && dashboardData.inscricoes) {
        new Chart(ctx2, {
            type: 'line',
            data: {
                labels: dashboardData.inscricoes.labels,
                datasets: [{
                    label: 'Inscrições',
                    data: dashboardData.inscricoes.data,
                    borderColor: '#007bff',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }

    // Gráfico de rosca - Distribuição por Faixas
    const ctx3 = document.getElementById('faixasChart');
    if (ctx3 && dashboardData.faixas && dashboardData.faixas.length > 0) {
        new Chart(ctx3, {
            type: 'doughnut',
            data: {
                labels: dashboardData.faixas.map(f => f.label),
                datasets: [{
                    data: dashboardData.faixas.map(f => f.value),
                    backgroundColor: [
                        '#ffffff', '#0066cc', '#ffcc00', '#ff6600',
                        '#00cc00', '#9900cc', '#8B4513', '#000000'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    // Gráfico de barras horizontais - Top Estados
    const ctx4 = document.getElementById('estadosChart');
    if (ctx4 && dashboardData.estados && dashboardData.estados.length > 0) {
        new Chart(ctx4, {
            type: 'bar',
            data: {
                labels: dashboardData.estados.slice(0, 8).map(e => e.label), // Top 8 estados
                datasets: [{
                    label: 'Número de Atletas',
                    data: dashboardData.estados.slice(0, 8).map(e => e.value),
                    backgroundColor: '#28a745'
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }
}

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

// Inicializar gráficos quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    initCharts();
});

// Código do chat (mantido do original)

// Variáveis globais
let chatState = 'initial'; // initial, waiting, contact_form, conversation
let currentQuestion = null;

// Alternar visibilidade do chat
function toggleChat() {
    const chatContainer = document.getElementById('chatContainer');
    const chatWindow = document.getElementById('chatWindow');

    if (chatContainer.classList.contains('collapsed')) {
        chatContainer.classList.remove('collapsed');
        chatWindow.style.display = 'flex';
    } else {
        chatContainer.classList.add('collapsed');
        chatWindow.style.display = 'none';
    }
}

// Enviar mensagem do usuário
function sendMessage() {
    const userInput = document.getElementById('userMessage');
    const message = userInput.value.trim();

    if (message === '') return;

    // Adiciona mensagem do usuário ao chat
    addUserMessage(message);
    userInput.value = '';

    // Processa a resposta do bot
    setTimeout(() => {
        processBotResponse(message);
    }, 800);
}

// Adicionar mensagem do usuário ao chat
function addUserMessage(message) {
    const chatMessages = document.getElementById('chatMessages');

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message-content user-message';
    messageDiv.innerHTML = `
        <div class="message-bubble">
            <p>${message}</p>
            <small class="message-time">Agora</small>
        </div>
    `;

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Adicionar mensagem do bot ao chat
function addBotMessage(message, options = null) {
    const chatMessages = document.getElementById('chatMessages');

    const messageDiv = document.createElement('div');
    messageDiv.className = 'bot-message';

    let optionsHTML = '';
    if (options) {
        optionsHTML = '<div class="quick-options">';
        options.forEach((option, index) => {
            optionsHTML += `<button class="btn-quick-option" onclick="selectQuickOption(${index})">${option}</button>`;
        });
        optionsHTML += '</div>';
    }

    messageDiv.innerHTML = `
        <div class="message-content">
            <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava6-bg.webp" 
                 alt="avatar" class="avatar-img">
            <div class="message-bubble">
                <p>${message}</p>
                ${optionsHTML}
                <small class="message-time">Agora</small>
            </div>
        </div>
    `;

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Processar resposta do bot
function processBotResponse(message) {
    const lowerMessage = message.toLowerCase();

    if (chatState === 'initial') {
        if (lowerMessage.includes('competição') || lowerMessage.includes('competicao')) {
            addBotMessage('As competições podem ser criadas na seção "Competições". Você pode configurar formato, datas, premiação e participantes. Precisa de ajuda com algo específico?',
                         ['Como criar uma competição', 'Como adicionar participantes', 'Voltar ao menu principal']);
            currentQuestion = 'competitions';
            chatState = 'waiting';
        } else if (lowerMessage.includes('suporte') || lowerMessage.includes('contato') || lowerMessage.includes('falar')) {
            showContactForm();
        } else {
            addBotMessage('Desculpe, não entendi. Como posso te ajudar?',
                         ['Dúvidas sobre competições', 'Problemas técnicos', 'Falar com suporte']);
        }
    }
    // Outros estados podem ser adicionados aqui
}

// Selecionar opção rápida
function selectQuickOption(optionIndex) {
    const chatMessages = document.getElementById('chatMessages');
    const options = {
        0: ['Dúvidas sobre competições', 'Problemas técnicos', 'Falar com suporte', 'Documentação'],
        1: ['Como criar uma competição', 'Como adicionar participantes', 'Voltar ao menu principal'],
        2: ['Problema ao salvar dados', 'Erro no sistema', 'Voltar ao menu principal'],
        3: ['Abrir formulário de contato', 'Voltar ao menu principal']
    };

    if (optionIndex === 0 && chatState === 'initial') {
        addBotMessage('As competições podem ser criadas na seção "Competições". Você pode configurar formato, datas, premiação e participantes. Precisa de ajuda com algo específico?',
                     ['Como criar uma competição', 'Como adicionar participantes', 'Voltar ao menu principal']);
        currentQuestion = 'competitions';
        chatState = 'waiting';
    } else if (optionIndex === 1 && chatState === 'initial') {
        addBotMessage('Para problemas técnicos, por favor descreva o que está acontecendo. Ou prefere:',
                     ['Problema ao salvar dados', 'Erro no sistema', 'Voltar ao menu principal']);
        currentQuestion = 'technical';
        chatState = 'waiting';
    } else if (optionIndex === 2 && chatState === 'initial') {
        showContactForm();
    } else if (optionIndex === 3 && chatState === 'initial') {
        addBotMessage('Nossa documentação está disponível em: <a href="https://docs.keychart.com" target="_blank">docs.keychart.com</a>',
                     ['Dúvidas sobre competições', 'Problemas técnicos', 'Falar com suporte']);
    } else if (chatState === 'waiting' && optionIndex === 2) {
        // Voltar ao menu principal
        addBotMessage('O que mais posso te ajudar?',
                     ['Dúvidas sobre competições', 'Problemas técnicos', 'Falar com suporte', 'Documentação']);
        chatState = 'initial';
        currentQuestion = null;
    } else {
        // Respostas específicas para cada opção
        const responses = {
            'competitions': {
                0: 'Para criar uma competição: 1) Acesse "Competições" > "Nova Competição" 2) Preencha os dados básicos 3) Configure o formato 4) Defina as datas 5) Salve. Precisa de mais detalhes?',
                1: 'Para adicionar participantes: 1) Acesse a competição 2) Vá em "Participantes" 3) Clique em "Adicionar" 4) Selecione as equipes/atletas 5) Confirme. Posso te ajudar com mais algo?'
            },
            'technical': {
                0: 'Problemas ao salvar dados podem ser causados por: 1) Conexão instável 2) Dados inválidos 3) Limite de caracteres. Recomendo verificar sua conexão e os dados inseridos. Se persistir, entre em contato com nosso suporte técnico.',
                1: 'Erros no sistema podem ser reportados para nosso time técnico. Por favor, descreva o erro e quais ações levaram a ele. Podemos abrir um formulário para você reportar com mais detalhes.'
            }
        };

        if (currentQuestion && responses[currentQuestion] && responses[currentQuestion][optionIndex]) {
            addBotMessage(responses[currentQuestion][optionIndex], ['Sim, preciso de mais ajuda', 'Voltar ao menu principal']);
        }
    }
}

// Mostrar formulário de contato
function showContactForm() {
    document.getElementById('chatMessages').style.display = 'none';
    document.getElementById('contactForm').style.display = 'block';
    document.getElementById('userMessage').disabled = true;
    document.getElementById('sendButton').disabled = true;
    chatState = 'contact_form';

    // Adiciona evento ao formulário
    document.getElementById('supportForm').addEventListener('submit', function(e) {
        e.preventDefault();
        submitContactForm();
    });
}

// Enviar formulário de contato
function submitContactForm() {
    const form = document.getElementById('supportForm');
    const formData = new FormData(form);

    // Simular envio (em produção, seria uma chamada AJAX)
    setTimeout(() => {
        document.getElementById('contactForm').style.display = 'none';
        document.getElementById('chatMessages').style.display = 'block';

        addBotMessage('Obrigado pelo contato! Sua solicitação foi registrada (#REF' + Math.floor(Math.random() * 10000) + '). Nossa equipe entrará em contato em breve. Enquanto isso, posso te ajudar com mais alguma coisa?',
                     ['Dúvidas sobre competições', 'Problemas técnicos', 'Documentação']);

        chatState = 'initial';
        form.reset();
    }, 1500);
}

// Inicializar chat
document.addEventListener('DOMContentLoaded', function() {
    // Habilitar campo de mensagem quando o chat estiver aberto
    document.getElementById('userMessage').addEventListener('focus', function() {
        if (chatState === 'initial' || chatState === 'waiting') {
            this.disabled = false;
            document.getElementById('sendButton').disabled = false;
        }
    });

    // Permitir enviar mensagem com Enter
    document.getElementById('userMessage').addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !this.disabled) {
            sendMessage();
        }
    });
});