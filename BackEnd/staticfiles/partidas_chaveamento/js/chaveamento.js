// JavaScript para a tela de chaveamento
document.addEventListener('DOMContentLoaded', function() {
    initializeChaveamento();
});

function initializeChaveamento() {
    // Inicializar componentes da página
    setupRealTimeUpdates();
    setupKeyboardShortcuts();
    setupAnimations();
}

function setupRealTimeUpdates() {
    // Configurar atualizações em tempo real se a partida estiver em andamento
    const statusElement = document.querySelector('.status-badge');
    if (statusElement && statusElement.classList.contains('status-em-andamento')) {
        // Verificar atualizações a cada 10 segundos
        setInterval(checkForUpdates, 10000);
    }
}

function setupKeyboardShortcuts() {
    // Atalhos de teclado para ações rápidas
    document.addEventListener('keydown', function(event) {
        // Ctrl + I = Iniciar partida
        if (event.ctrlKey && event.key === 'i') {
            event.preventDefault();
            iniciarPartida();
        }
        
        // Ctrl + P = Pausar partida
        if (event.ctrlKey && event.key === 'p') {
            event.preventDefault();
            pausarPartida();
        }
        
        // Ctrl + F = Finalizar partida
        if (event.ctrlKey && event.key === 'f') {
            event.preventDefault();
            finalizarPartida();
        }
        
        // Ctrl + U = Atualizar placar
        if (event.ctrlKey && event.key === 'u') {
            event.preventDefault();
            atualizarPlacar();
        }
        
        // ESC = Voltar às partidas
        if (event.key === 'Escape') {
            event.preventDefault();
            voltarPartidas();
        }
    });
}

function setupAnimations() {
    // Animações de entrada
    const cards = document.querySelectorAll('.atleta-card, .chaveamento-container');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 200);
    });
}

function checkForUpdates() {
    // Verificar se há atualizações na partida
    const currentUrl = window.location.href;
    
    fetch(currentUrl, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.text())
    .then(html => {
        // Criar um elemento temporário para parsear o HTML
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        
        // Verificar se os placares mudaram
        const currentScore1 = document.querySelector('.score');
        const newScore1 = doc.querySelector('.score');
        
        if (currentScore1 && newScore1 && currentScore1.textContent !== newScore1.textContent) {
            showNotification('Placar atualizado!', 'info');
            updateScoreDisplay(doc);
        }
        
        // Verificar mudança de status
        const currentStatus = document.querySelector('.status-badge');
        const newStatus = doc.querySelector('.status-badge');
        
        if (currentStatus && newStatus && currentStatus.textContent !== newStatus.textContent) {
            showNotification('Status da partida atualizado!', 'warning');
            updateStatusDisplay(doc);
        }
    })
    .catch(error => {
        console.error('Erro ao verificar atualizações:', error);
    });
}

function updateScoreDisplay(newDoc) {
    // Atualizar os placares com animação
    const scores = document.querySelectorAll('.score');
    const newScores = newDoc.querySelectorAll('.score');
    
    scores.forEach((score, index) => {
        if (newScores[index]) {
            score.style.transform = 'scale(1.2)';
            score.style.color = '#e74c3c';
            
            setTimeout(() => {
                score.textContent = newScores[index].textContent;
                score.style.transform = 'scale(1)';
                score.style.color = '';
            }, 300);
        }
    });
}

function updateStatusDisplay(newDoc) {
    // Atualizar o status da partida
    const statusBadge = document.querySelector('.status-badge');
    const newStatusBadge = newDoc.querySelector('.status-badge');
    
    if (newStatusBadge) {
        statusBadge.className = newStatusBadge.className;
        statusBadge.textContent = newStatusBadge.textContent;
        
        // Adicionar efeito de destaque
        statusBadge.style.animation = 'pulse 1s ease-in-out 3';
    }
}

// Funções de controle da partida
function iniciarPartida() {
    showConfirmDialog(
        'Iniciar Partida',
        'Tem certeza que deseja iniciar esta partida?',
        () => {
            showLoading('main-content');
            
            // Simulação de chamada AJAX
            setTimeout(() => {
                hideLoading('main-content');
                showNotification('Partida iniciada com sucesso!', 'success');
                
                // Atualizar status visual
                const statusBadge = document.querySelector('.status-badge');
                if (statusBadge) {
                    statusBadge.className = 'status-badge status-em-andamento';
                    statusBadge.textContent = 'EM ANDAMENTO';
                }
            }, 1500);
        }
    );
}

function pausarPartida() {
    showConfirmDialog(
        'Pausar Partida',
        'Deseja pausar a partida temporariamente?',
        () => {
            showLoading('main-content');
            
            setTimeout(() => {
                hideLoading('main-content');
                showNotification('Partida pausada.', 'warning');
            }, 1000);
        }
    );
}

function finalizarPartida() {
    showConfirmDialog(
        'Finalizar Partida',
        'Atenção! Esta ação irá finalizar a partida permanentemente. Confirmar?',
        () => {
            showLoading('main-content');
            
            setTimeout(() => {
                hideLoading('main-content');
                showNotification('Partida finalizada!', 'success');
                
                // Atualizar status visual
                const statusBadge = document.querySelector('.status-badge');
                if (statusBadge) {
                    statusBadge.className = 'status-badge status-finalizada';
                    statusBadge.textContent = 'FINALIZADA';
                }
                
                // Ocultar botões de controle
                const actionsDiv = document.querySelector('.chaveamento-actions');
                if (actionsDiv) {
                    actionsDiv.style.opacity = '0.5';
                    actionsDiv.style.pointerEvents = 'none';
                }
            }, 1500);
        }
    );
}

function atualizarPlacar() {
    showLoading('main-content');
    
    // Simulação de atualização do placar
    setTimeout(() => {
        hideLoading('main-content');
        
        // Simular mudança de placar
        const scores = document.querySelectorAll('.score');
        scores.forEach(score => {
            const currentScore = parseInt(score.textContent) || 0;
            const newScore = Math.max(0, currentScore + Math.floor(Math.random() * 3) - 1);
            
            score.style.transform = 'scale(1.3)';
            score.style.color = '#27ae60';
            
            setTimeout(() => {
                score.textContent = newScore;
                score.style.transform = 'scale(1)';
                score.style.color = '';
            }, 300);
        });
        
        showNotification('Placar atualizado!', 'info');
    }, 1000);
}

function voltarPartidas() {
    const backLink = document.querySelector('a[href*="partidas"]');
    if (backLink) {
        window.location.href = backLink.href;
    }
}

// Funções utilitárias
function showLoading(elementId) {
    const element = document.getElementById(elementId) || document.querySelector('.content');
    if (element) {
        element.classList.add('loading');
    }
}

function hideLoading(elementId) {
    const element = document.getElementById(elementId) || document.querySelector('.content');
    if (element) {
        element.classList.remove('loading');
    }
}

function showNotification(message, type = 'info') {
    // Criar elemento de notificação
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} notification-toast`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        animation: slideInRight 0.5s ease;
    `;
    notification.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="bi bi-check-circle me-2"></i>
            <span>${message}</span>
            <button type="button" class="btn-close ms-auto" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remover após 5 segundos
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.animation = 'slideOutRight 0.5s ease';
            setTimeout(() => notification.remove(), 500);
        }
    }, 5000);
}

function showConfirmDialog(title, message, onConfirm) {
    // Criar modal de confirmação
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">${title}</h5>
                    <button type="button" class="btn-close" data-mdb-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <p>${message}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-mdb-dismiss="modal">Cancelar</button>
                    <button type="button" class="btn btn-primary" onclick="confirmAction()">Confirmar</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Função de confirmação
    window.confirmAction = function() {
        onConfirm();
        modal.remove();
    };
    
    // Mostrar modal usando MDB
    try {
        const bsModal = new mdb.Modal(modal);
        bsModal.show();
    } catch (error) {
        // Fallback para Bootstrap padrão
        modal.style.display = 'block';
        modal.classList.add('show');
    }
    
    // Remover modal quando fechado
    modal.addEventListener('hidden.mdb.modal', () => {
        modal.remove();
        delete window.confirmAction;
    });
}

// Estilos CSS adicionais para animações
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .notification-toast {
        border-left: 4px solid #007bff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .alert-success {
        border-left-color: #28a745;
    }
    
    .alert-warning {
        border-left-color: #ffc107;
    }
    
    .alert-danger {
        border-left-color: #dc3545;
    }
    
    .loading {
        position: relative;
    }
    
    .loading::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255,255,255,0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    }
    
    .loading::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 40px;
        height: 40px;
        border: 4px solid #f3f3f3;
        border-top: 4px solid #007bff;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        z-index: 1001;
    }
    
    @keyframes spin {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }
`;
document.head.appendChild(style);
