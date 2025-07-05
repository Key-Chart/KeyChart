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
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            font: {
                                size: 10
                            },
                            boxWidth: 12
                        }
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
                labels: dashboardData.estados.slice(0, 6).map(e => e.label), // Top 6 estados para economizar espaço
                datasets: [{
                    label: 'Número de Atletas',
                    data: dashboardData.estados.slice(0, 6).map(e => e.value),
                    backgroundColor: '#28a745'
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
                        ticks: {
                            stepSize: 1,
                            font: {
                                size: 10
                            }
                        }
                    },
                    y: {
                        ticks: {
                            font: {
                                size: 10
                            }
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

// Código do chat melhorado

// Variáveis globais do chat
let chatState = 'initial'; // initial, waiting, contact_form, conversation
let currentQuestion = null;
let chatHistory = [];
let isTyping = false;

// Banco de conhecimento do chat
const chatKnowledge = {
    greetings: ['olá', 'oi', 'bom dia', 'boa tarde', 'boa noite', 'hey', 'hello'],
    keywords: {
        'competicao': ['competição', 'competicao', 'campeonato', 'torneio', 'evento'],
        'atleta': ['atleta', 'participante', 'competidor', 'lutador'],
        'academia': ['academia', 'dojo', 'escola', 'equipe'],
        'kata': ['kata', 'forma', 'sequência'],
        'kumite': ['kumite', 'luta', 'combate', 'sparring'],
        'inscricao': ['inscrição', 'inscricao', 'cadastro', 'registro'],
        'relatorio': ['relatório', 'relatorio', 'dados', 'estatísticas', 'gráfico'],
        'problema': ['problema', 'erro', 'bug', 'falha', 'não funciona', 'travou'],
        'ajuda': ['ajuda', 'socorro', 'help', 'como fazer', 'tutorial']
    }
};

// Respostas automáticas mais inteligentes
const autoResponses = {
    competicao: {
        message: '🏆 Sobre competições, posso te ajudar com:',
        options: [
            'Como criar uma nova competição',
            'Gerenciar participantes',
            'Configurar categorias',
            'Definir chaveamento',
            'Ver relatórios de competições'
        ]
    },
    atleta: {
        message: '🥋 Sobre atletas, posso te orientar com:',
        options: [
            'Cadastrar novo atleta',
            'Gerenciar inscrições',
            'Ver perfil do atleta',
            'Histórico de participações',
            'Relatórios de desempenho'
        ]
    },
    academia: {
        message: '🏢 Sobre academias, posso te ajudar com:',
        options: [
            'Cadastrar nova academia',
            'Gerenciar atletas da academia',
            'Ver ranking de academias',
            'Relatórios por academia'
        ]
    },
    relatorio: {
        message: '📊 Sobre relatórios, posso te mostrar:',
        options: [
            'Acessar dashboard de relatórios',
            'Gerar relatório de competição',
            'Estatísticas de atletas',
            'Dados de academias',
            'Exportar dados'
        ]
    },
    problema: {
        message: '🔧 Para resolver problemas, me conte mais:',
        options: [
            'Erro ao salvar dados',
            'Problema com login',
            'Erro no sistema',
            'Página não carrega',
            'Falar com suporte técnico'
        ]
    }
};

// Alternar visibilidade do chat
function toggleChat() {
    const chatContainer = document.getElementById('chatContainer');
    const chatWindow = document.getElementById('chatWindow');

    if (chatContainer.classList.contains('collapsed')) {
        chatContainer.classList.remove('collapsed');
        chatWindow.style.display = 'flex';
        
        // Marcar como online
        updateChatStatus('online');
        
        // Se for a primeira vez abrindo, mostrar mensagem de boas-vindas mais completa
        if (chatHistory.length === 0) {
            setTimeout(() => {
                addBotMessage('👋 Olá! Sou o assistente virtual da KeyChart. Estou aqui para te ajudar com:', [
                    'Dúvidas sobre competições',
                    'Gerenciar atletas e academias', 
                    'Problemas técnicos',
                    'Ver relatórios e estatísticas',
                    'Falar com suporte humano'
                ]);
            }, 500);
        }
    } else {
        chatContainer.classList.add('collapsed');
        chatWindow.style.display = 'none';
        updateChatStatus('away');
    }
}

// Atualizar status do chat
function updateChatStatus(status) {
    const statusDot = document.querySelector('.status-dot');
    const statusText = document.querySelector('.status-indicator small');
    
    if (status === 'online') {
        statusDot.className = 'status-dot online';
        statusText.textContent = 'Online';
    } else {
        statusDot.className = 'status-dot';
        statusText.textContent = 'Ausente';
    }
}

// Simular digitação do bot
function showTypingIndicator() {
    if (isTyping) return;
    
    isTyping = true;
    const chatMessages = document.getElementById('chatMessages');
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'bot-message typing-indicator';
    typingDiv.id = 'typing-indicator';
    typingDiv.innerHTML = `
        <div class="message-content">
            <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava6-bg.webp" 
                 alt="avatar" class="avatar-img">
            <div class="message-bubble">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
    isTyping = false;
}

// Enviar mensagem do usuário
function sendMessage() {
    const userInput = document.getElementById('userMessage');
    const message = userInput.value.trim();

    if (message === '') return;

    // Adiciona mensagem do usuário ao chat e histórico
    addUserMessage(message);
    chatHistory.push({type: 'user', message: message, timestamp: new Date()});
    userInput.value = '';

    // Mostrar indicador de digitação
    showTypingIndicator();

    // Processa a resposta do bot com delay realista
    setTimeout(() => {
        hideTypingIndicator();
        processBotResponse(message);
    }, Math.random() * 1000 + 500); // 500ms a 1.5s
}

// Adicionar mensagem do usuário ao chat
function addUserMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    const time = new Date().toLocaleTimeString('pt-BR', {hour: '2-digit', minute: '2-digit'});

    const messageDiv = document.createElement('div');
    messageDiv.className = 'message-content user-message';
    messageDiv.innerHTML = `
        <div class="message-bubble">
            <p>${message}</p>
            <small class="message-time">${time}</small>
        </div>
    `;

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Adicionar mensagem do bot ao chat
function addBotMessage(message, options = null) {
    const chatMessages = document.getElementById('chatMessages');
    const time = new Date().toLocaleTimeString('pt-BR', {hour: '2-digit', minute: '2-digit'});

    const messageDiv = document.createElement('div');
    messageDiv.className = 'bot-message';

    let optionsHTML = '';
    if (options) {
        optionsHTML = '<div class="quick-options">';
        options.forEach((option, index) => {
            optionsHTML += `<button class="btn-quick-option" onclick="selectQuickOption(${index}, '${option}')">${option}</button>`;
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
                <small class="message-time">${time}</small>
            </div>
        </div>
    `;

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Adicionar ao histórico
    chatHistory.push({type: 'bot', message: message, options: options, timestamp: new Date()});
}

// Processamento inteligente de mensagens
function processBotResponse(message) {
    const lowerMessage = message.toLowerCase();
    
    // Verificar saudações
    if (chatKnowledge.greetings.some(greeting => lowerMessage.includes(greeting))) {
        addBotMessage('Olá! 😊 Como posso te ajudar hoje?', [
            'Dúvidas sobre competições',
            'Gerenciar atletas e academias',
            'Problemas técnicos',
            'Ver relatórios'
        ]);
        return;
    }
    
    // Verificar palavras-chave
    for (const [category, keywords] of Object.entries(chatKnowledge.keywords)) {
        if (keywords.some(keyword => lowerMessage.includes(keyword))) {
            if (autoResponses[category]) {
                addBotMessage(autoResponses[category].message, autoResponses[category].options);
                currentQuestion = category;
                chatState = 'waiting';
                return;
            }
        }
    }
    
    // Perguntas sobre navegação no sistema
    if (lowerMessage.includes('onde') || lowerMessage.includes('como acessar')) {
        addBotMessage('Para navegar no sistema, use o menu lateral. Posso te ajudar a encontrar:', [
            'Competições',
            'Atletas',
            'Relatórios',
            'Configurações'
        ]);
        return;
    }
    
    // Perguntas sobre funcionalidades
    if (lowerMessage.includes('o que posso fazer') || lowerMessage.includes('funcionalidades')) {
        addBotMessage('No KeyChart você pode: 🏆 Criar e gerenciar competições 🥋 Cadastrar atletas e academias 📊 Visualizar relatórios detalhados ⚙️ Configurar o sistema 🔄 Gerenciar chaveamentos. O que te interessa mais?', [
            'Criar competição',
            'Cadastrar atletas',
            'Ver relatórios',
            'Configurações'
        ]);
        return;
    }
    
    // Resposta padrão mais útil
    addBotMessage('Não entendi exatamente, mas posso te ajudar com essas opções populares:', [
        'Dúvidas sobre competições',
        'Problemas técnicos',
        'Como usar o sistema',
        'Falar com suporte humano'
    ]);
}

// Selecionar opção rápida melhorada
function selectQuickOption(optionIndex, optionText) {
    // Adicionar a opção selecionada como mensagem do usuário
    addUserMessage(optionText);
    chatHistory.push({type: 'user', message: optionText, timestamp: new Date()});
    
    // Mostrar digitação
    showTypingIndicator();
    
    setTimeout(() => {
        hideTypingIndicator();
        
        // Processar baseado no texto da opção
        if (optionText.includes('competição') || optionText.includes('competicao')) {
            handleCompetitionQuestions(optionText);
        } else if (optionText.includes('atleta')) {
            handleAthleteQuestions(optionText);
        } else if (optionText.includes('academia')) {
            handleAcademyQuestions(optionText);
        } else if (optionText.includes('relatório') || optionText.includes('relatorio')) {
            handleReportQuestions(optionText);
        } else if (optionText.includes('problema') || optionText.includes('técnico')) {
            handleTechnicalQuestions(optionText);
        } else if (optionText.includes('suporte humano') || optionText.includes('Falar com suporte')) {
            showContactForm();
        } else {
            // Resposta genérica
            addBotMessage('Entendi! Posso te ajudar com mais alguma coisa?', [
                'Dúvidas sobre competições',
                'Problemas técnicos',
                'Relatórios',
                'Falar com suporte'
            ]);
        }
    }, 800);
}

// Handlers específicos para cada categoria
function handleCompetitionQuestions(question) {
    if (question.includes('criar')) {
        addBotMessage('Para criar uma competição: 1️⃣ Acesse "Competições" no menu 2️⃣ Clique em "Nova Competição" 3️⃣ Preencha os dados básicos 4️⃣ Configure modalidades e categorias 5️⃣ Defina datas e locais 6️⃣ Salve e publique', [
            'Como adicionar categorias',
            'Como definir chaveamento',
            'Voltar ao menu principal'
        ]);
    } else if (question.includes('participantes')) {
        addBotMessage('Para gerenciar participantes: 1️⃣ Acesse a competição 2️⃣ Vá em "Participantes" 3️⃣ Use "Adicionar Atleta" ou "Importar Lista" 4️⃣ Confirme as inscrições', [
            'Como importar atletas',
            'Como organizar por categorias',
            'Voltar ao menu principal'
        ]);
    } else {
        addBotMessage('Sobre competições, posso te ajudar com mais detalhes:', [
            'Configurar modalidades',
            'Gerenciar árbitros',
            'Definir premiação',
            'Voltar ao menu principal'
        ]);
    }
}

function handleAthleteQuestions(question) {
    addBotMessage('Para gerenciar atletas: 📝 Acesse "Atletas" no menu 👤 Clique em "Novo Atleta" para cadastrar 📋 Preencha dados pessoais e da academia 🥋 Defina faixa e categoria 💾 Salve o cadastro', [
        'Como editar dados do atleta',
        'Como ver histórico de competições',
        'Como gerar relatório do atleta',
        'Voltar ao menu principal'
    ]);
}

function handleAcademyQuestions(question) {
    addBotMessage('Para gerenciar academias: 🏢 Acesse "Academias" no menu ➕ Cadastre nova academia com dados completos 👥 Associe atletas à academia 📊 Acompanhe desempenho da equipe', [
        'Como ver ranking de academias',
        'Como gerar relatório da academia',
        'Voltar ao menu principal'
    ]);
}

function handleReportQuestions(question) {
    addBotMessage('📊 Para acessar relatórios: 1️⃣ Clique em "Relatórios" no menu 2️⃣ Escolha o tipo de relatório 3️⃣ Configure os filtros 4️⃣ Visualize os dados 5️⃣ Exporte se necessário', [
        'Tipos de relatórios disponíveis',
        'Como exportar dados',
        'Como configurar filtros',
        'Voltar ao menu principal'
    ]);
}

function handleTechnicalQuestions(question) {
    if (question.includes('login')) {
        addBotMessage('Problemas de login: ✅ Verifique usuário e senha ✅ Limpe cache do navegador ✅ Tente outro navegador ✅ Entre em contato se persistir', [
            'Esqueci minha senha',
            'Conta bloqueada',
            'Falar com suporte técnico'
        ]);
    } else if (question.includes('salvar')) {
        addBotMessage('Problemas ao salvar: ✅ Verifique sua conexão ✅ Confira se todos os campos obrigatórios estão preenchidos ✅ Tente atualizar a página ✅ Use outro navegador', [
            'Dados não aparecem',
            'Erro específico',
            'Falar com suporte técnico'
        ]);
    } else {
        addBotMessage('Para problemas técnicos, me diga mais sobre o erro:', [
            'Página não carrega',
            'Erro ao salvar dados',
            'Sistema travou',
            'Outro problema',
            'Falar com suporte técnico'
        ]);
    }
}

// Mostrar formulário de contato melhorado
function showContactForm() {
    document.getElementById('chatMessages').style.display = 'none';
    document.getElementById('contactForm').style.display = 'block';
    document.getElementById('userMessage').disabled = true;
    document.getElementById('sendButton').disabled = true;
    chatState = 'contact_form';

    // Pré-preencher assunto baseado no contexto
    if (currentQuestion) {
        const subjectMap = {
            'competicao': 'Dúvida sobre competições',
            'atleta': 'Dúvida sobre atletas',
            'academia': 'Dúvida sobre academias',
            'relatorio': 'Dúvida sobre relatórios',
            'problema': 'Problema técnico'
        };
        
        const subjectSelect = document.getElementById('subject');
        if (subjectSelect && subjectMap[currentQuestion]) {
            subjectSelect.value = subjectMap[currentQuestion];
        }
    }
}

// Enviar formulário de contato
function submitContactForm() {
    const form = document.getElementById('supportForm');
    const formData = new FormData(form);
    
    // Validação básica
    if (!formData.get('name') || !formData.get('email') || !formData.get('message')) {
        alert('Por favor, preencha todos os campos obrigatórios.');
        return;
    }

    // Simular envio
    const submitBtn = form.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="bi bi-clock"></i> Enviando...';

    setTimeout(() => {
        document.getElementById('contactForm').style.display = 'none';
        document.getElementById('chatMessages').style.display = 'block';
        document.getElementById('userMessage').disabled = false;
        document.getElementById('sendButton').disabled = false;

        const ticketId = 'KC' + Math.floor(Math.random() * 90000 + 10000);
        addBotMessage(`✅ Solicitação enviada com sucesso! 🎫 Protocolo: ${ticketId} 📧 Você receberá um email de confirmação ⏰ Nosso time responderá em até 24h. Posso te ajudar com mais alguma coisa?`, [
            'Dúvidas sobre competições',
            'Problemas técnicos',
            'Ver status do chamado',
            'Nova solicitação'
        ]);

        chatState = 'initial';
        currentQuestion = null;
        form.reset();
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Enviar solicitação';
    }, 2000);
}

// Funções adicionais do chat melhorado

// Enviar mensagem rápida
function sendQuickMessage(message) {
    document.getElementById('userMessage').value = message;
    sendMessage();
    toggleSuggestions(); // Fechar sugestões
}

// Alternar sugestões rápidas
function toggleSuggestions() {
    const suggestions = document.getElementById('quickSuggestions');
    const isVisible = suggestions.style.display !== 'none';
    suggestions.style.display = isVisible ? 'none' : 'block';
}

// Limpar conversa
function clearChat() {
    if (confirm('Tem certeza que deseja limpar toda a conversa?')) {
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.innerHTML = '';
        chatHistory = [];
        chatState = 'initial';
        currentQuestion = null;
        updateMessageCount();
        
        // Mostrar mensagem de boas-vindas novamente
        setTimeout(() => {
            addBotMessage('👋 Conversa reiniciada! Como posso te ajudar?', [
                'Dúvidas sobre competições',
                'Gerenciar atletas e academias', 
                'Problemas técnicos',
                'Ver relatórios e estatísticas',
                'Falar com suporte humano'
            ]);
        }, 500);
    }
}

// Cancelar formulário de contato
function cancelContactForm() {
    document.getElementById('contactForm').style.display = 'none';
    document.getElementById('chatMessages').style.display = 'block';
    document.getElementById('userMessage').disabled = false;
    document.getElementById('sendButton').disabled = false;
    chatState = 'initial';
    
    addBotMessage('Formulário cancelado. Como mais posso te ajudar?', [
        'Dúvidas sobre competições',
        'Problemas técnicos',
        'Ver relatórios'
    ]);
}

// Atualizar contador de mensagens
function updateMessageCount() {
    const count = chatHistory.length;
    const messageCountElement = document.getElementById('messageCount');
    if (messageCountElement) {
        messageCountElement.textContent = `${count} mensagem${count !== 1 ? 's' : ''}`;
    }
}

// Adicionar notificação de nova mensagem
function showChatNotification() {
    const notification = document.getElementById('chatNotification');
    const chatContainer = document.getElementById('chatContainer');
    
    if (chatContainer.classList.contains('collapsed')) {
        notification.style.display = 'block';
        notification.textContent = '1';
        
        // Animar o botão
        const chatBtn = document.querySelector('.chat-toggle-btn');
        chatBtn.classList.add('animate__animated', 'animate__pulse');
        
        setTimeout(() => {
            chatBtn.classList.remove('animate__animated', 'animate__pulse');
        }, 1000);
    }
}

// Remover notificação quando abrir o chat
function clearChatNotification() {
    const notification = document.getElementById('chatNotification');
    notification.style.display = 'none';
}

// Função melhorada para adicionar mensagem do bot
function addBotMessageEnhanced(message, options = null, delay = 0) {
    setTimeout(() => {
        addBotMessage(message, options);
        updateMessageCount();
        showChatNotification();
    }, delay);
}

// Validação aprimorada do formulário
function validateContactForm() {
    const form = document.getElementById('supportForm');
    const name = form.querySelector('#name').value.trim();
    const email = form.querySelector('#email').value.trim();
    const subject = form.querySelector('#subject').value;
    const message = form.querySelector('#message').value.trim();
    
    const errors = [];
    
    if (!name) errors.push('Nome é obrigatório');
    if (!email) errors.push('E-mail é obrigatório');
    if (!email.includes('@')) errors.push('E-mail inválido');
    if (!subject) errors.push('Assunto é obrigatório');
    if (!message) errors.push('Mensagem é obrigatória');
    if (message.length < 10) errors.push('Mensagem muito curta (mínimo 10 caracteres)');
    
    if (errors.length > 0) {
        alert('Erros encontrados:\n\n' + errors.join('\n'));
        return false;
    }
    
    return true;
}

// Função para formatar texto com emojis e links
function formatMessage(text) {
    // Adicionar links automáticos
    text = text.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');
    
    // Adicionar formatação para códigos
    text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // Adicionar quebras de linha para listas numeradas
    text = text.replace(/(\d+\))/g, '<br>$1');
    
    return text;
}

// Override da função addBotMessage para usar formatação
const originalAddBotMessage = addBotMessage;
addBotMessage = function(message, options = null) {
    const formattedMessage = formatMessage(message);
    return originalAddBotMessage(formattedMessage, options);
};

// Adicionar funcionalidade de histórico de comandos
let commandHistory = [];
let historyIndex = -1;

// Navegação no histórico com setas do teclado
function handleKeyNavigation(event) {
    const userMessage = document.getElementById('userMessage');
    
    if (event.key === 'ArrowUp') {
        event.preventDefault();
        if (historyIndex < commandHistory.length - 1) {
            historyIndex++;
            userMessage.value = commandHistory[commandHistory.length - 1 - historyIndex];
        }
    } else if (event.key === 'ArrowDown') {
        event.preventDefault();
        if (historyIndex > 0) {
            historyIndex--;
            userMessage.value = commandHistory[commandHistory.length - 1 - historyIndex];
        } else if (historyIndex === 0) {
            historyIndex = -1;
            userMessage.value = '';
        }
    }
}

// Override da função sendMessage para incluir histórico
const originalSendMessage = sendMessage;
sendMessage = function() {
    const userInput = document.getElementById('userMessage');
    const message = userInput.value.trim();
    
    if (message && !commandHistory.includes(message)) {
        commandHistory.push(message);
        if (commandHistory.length > 20) { // Manter apenas 20 comandos
            commandHistory.shift();
        }
    }
    historyIndex = -1;
    
    return originalSendMessage();
};

// Adicionar suporte a comandos especiais
function processSpecialCommands(message) {
    const lowerMessage = message.toLowerCase();
    
    if (lowerMessage === '/help' || lowerMessage === '/ajuda') {
        addBotMessage(`🤖 **Comandos especiais:**
        
/help - Mostra esta ajuda
/limpar - Limpa a conversa  
/status - Mostra status do sistema
/contato - Abre formulário de contato direto
/docs - Link para documentação
/versao - Informações da versão

**Atalhos:**
↑/↓ - Navegar no histórico de mensagens
Enter - Enviar mensagem
Shift+Enter - Nova linha`, [
            'Voltar ao menu principal',
            'Falar com suporte'
        ]);
        return true;
    }
    
    if (lowerMessage === '/limpar') {
        clearChat();
        return true;
    }
    
    if (lowerMessage === '/status') {
        addBotMessage(`📊 **Status do Sistema:**
        
✅ Sistema Online
✅ Base de dados conectada  
✅ Suporte disponível 24/7
⚡ Tempo de resposta: < 1s
🔄 Última atualização: ${new Date().toLocaleString('pt-BR')}`, [
            'Ver mais detalhes',
            'Voltar ao menu principal'
        ]);
        return true;
    }
    
    if (lowerMessage === '/contato') {
        showContactForm();
        return true;
    }
    
    if (lowerMessage === '/docs') {
        addBotMessage('📚 **Documentação KeyChart:**\n\n📖 Manual do usuário: [docs.keychart.com](https://docs.keychart.com)\n🎥 Vídeos tutoriais: [youtube.com/keychart](https://youtube.com/keychart)\n❓ FAQ: [help.keychart.com](https://help.keychart.com)', [
            'Preciso de ajuda específica',
            'Voltar ao menu principal'
        ]);
        return true;
    }
    
    if (lowerMessage === '/versao') {
        addBotMessage('ℹ️ **KeyChart v2.1.0**\n\nBuild: 2025.01.04\n🆕 Novidades desta versão:\n• Dashboard melhorado\n• Chat inteligente\n• Relatórios avançados\n• Performance otimizada', [
            'Ver changelog completo',
            'Voltar ao menu principal'
        ]);
        return true;
    }
    
    return false;
}

// Override da função processBotResponse para incluir comandos especiais
const originalProcessBotResponse = processBotResponse;
processBotResponse = function(message) {
    // Verificar comandos especiais primeiro
    if (processSpecialCommands(message)) {
        return;
    }
    
    // Processar normalmente
    return originalProcessBotResponse(message);
};