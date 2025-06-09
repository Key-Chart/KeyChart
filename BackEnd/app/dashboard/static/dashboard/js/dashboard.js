
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