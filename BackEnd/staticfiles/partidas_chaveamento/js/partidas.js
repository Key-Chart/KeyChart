// JavaScript para gerenciar a tela de partidas
document.addEventListener('DOMContentLoaded', function() {
    initializePartidas();
});

function initializePartidas() {
    // Inicializar tooltips e outros componentes
    initializeTooltips();
    setupFilterHandlers();
    setupTableInteractions();
}

function initializeTooltips() {
    // Adicionar tooltips para botões de ação
    const tooltipElements = document.querySelectorAll('[title]');
    tooltipElements.forEach(element => {
        element.setAttribute('data-mdb-toggle', 'tooltip');
    });
}

function setupFilterHandlers() {
    // Auto-submit do formulário ao mudar filtros
    const filterSelects = document.querySelectorAll('.filters-card select');
    filterSelects.forEach(select => {
        select.addEventListener('change', function() {
            if (this.value !== '') {
                document.querySelector('.filters-card form').submit();
            }
        });
    });
}

function setupTableInteractions() {
    // Adicionar efeitos hover nas linhas da tabela
    const tableRows = document.querySelectorAll('.table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(4px)';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
        });
    });
}

// Funções para gerenciar partidas
function viewMatch(matchId) {
    showLoading('match-details-content');
    
    // Simular carregamento de dados da partida
    setTimeout(() => {
        const content = `
            <div class="row">
                <div class="col-md-6">
                    <h6 class="fw-bold mb-3"><i class="bi bi-info-circle me-2"></i>Informações Gerais</h6>
                    <table class="table table-borderless">
                        <tr><td><strong>ID da Partida:</strong></td><td>#${matchId}</td></tr>
                        <tr><td><strong>Data:</strong></td><td>04/07/2025</td></tr>
                        <tr><td><strong>Horário:</strong></td><td>14:30</td></tr>
                        <tr><td><strong>Duração:</strong></td><td>3 min</td></tr>
                        <tr><td><strong>Status:</strong></td><td><span class="badge badge-status-finalizada">Finalizada</span></td></tr>
                    </table>
                </div>
                <div class="col-md-6">
                    <h6 class="fw-bold mb-3"><i class="bi bi-people me-2"></i>Atletas</h6>
                    <div class="mb-3">
                        <div class="d-flex align-items-center mb-2">
                            <div class="athlete-avatar bg-primary me-2">A1</div>
                            <div>
                                <strong>Atleta 1:</strong> João Silva<br>
                                <small class="text-muted">Academia Champions</small>
                            </div>
                        </div>
                        <div class="d-flex align-items-center">
                            <div class="athlete-avatar bg-info me-2">A2</div>
                            <div>
                                <strong>Atleta 2:</strong> Maria Santos<br>
                                <small class="text-muted">Dojo Samurai</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <hr>
            <div class="row">
                <div class="col-md-6">
                    <h6 class="fw-bold mb-3"><i class="bi bi-trophy me-2"></i>Resultado Final</h6>
                    <div class="text-center">
                        <div class="match-result display-6 mb-2">8 - 5</div>
                        <div class="badge bg-success fs-6 p-3">
                            <i class="bi bi-trophy-fill me-2"></i>Vencedor: João Silva
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <h6 class="fw-bold mb-3"><i class="bi bi-graph-up me-2"></i>Estatísticas</h6>
                    <table class="table table-sm">
                        <tr><td>Ippons:</td><td>2 - 1</td></tr>
                        <tr><td>Waza-aris:</td><td>1 - 2</td></tr>
                        <tr><td>Yukos:</td><td>3 - 1</td></tr>
                        <tr><td>Advertências:</td><td>0 - 1</td></tr>
                    </table>
                </div>
            </div>
            <div class="row mt-3">
                <div class="col-12">
                    <h6 class="fw-bold mb-3"><i class="bi bi-journal-text me-2"></i>Observações</h6>
                    <div class="alert alert-info">
                        <i class="bi bi-info-circle me-2"></i>
                        Partida muito equilibrada. João Silva conseguiu a vitória com um ippon no final do combate.
                    </div>
                </div>
            </div>
        `;
        document.getElementById('match-details-content').innerHTML = content;
    }, 800);
}

function editMatch(matchId) {
    showLoading('edit-match-content');
    
    // Simular carregamento de dados para edição
    setTimeout(() => {
        const content = `
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label for="editMatchDate" class="form-label">Data da Partida</label>
                    <input type="date" class="form-control" id="editMatchDate" value="2025-07-04" required>
                </div>
                <div class="col-md-6 mb-3">
                    <label for="editMatchTime" class="form-label">Horário</label>
                    <input type="time" class="form-control" id="editMatchTime" value="14:30" required>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label for="editScore1" class="form-label">Pontos Atleta 1</label>
                    <input type="number" class="form-control" id="editScore1" value="8" min="0" required>
                </div>
                <div class="col-md-6 mb-3">
                    <label for="editScore2" class="form-label">Pontos Atleta 2</label>
                    <input type="number" class="form-control" id="editScore2" value="5" min="0" required>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label for="editWarnings1" class="form-label">Advertências Atleta 1</label>
                    <input type="number" class="form-control" id="editWarnings1" value="0" min="0" max="4">
                </div>
                <div class="col-md-6 mb-3">
                    <label for="editWarnings2" class="form-label">Advertências Atleta 2</label>
                    <input type="number" class="form-control" id="editWarnings2" value="1" min="0" max="4">
                </div>
            </div>
            <div class="mb-3">
                <label for="editStatus" class="form-label">Status da Partida</label>
                <select class="form-select" id="editStatus" required>
                    <option value="agendada">Agendada</option>
                    <option value="em_andamento">Em Andamento</option>
                    <option value="finalizada" selected>Finalizada</option>
                    <option value="cancelada">Cancelada</option>
                </select>
            </div>
            <div class="mb-3">
                <label for="editDuration" class="form-label">Duração (minutos)</label>
                <input type="number" class="form-control" id="editDuration" value="3" min="1" max="10">
            </div>
            <div class="mb-3">
                <label for="editObservations" class="form-label">Observações</label>
                <textarea class="form-control" id="editObservations" rows="3" 
                          placeholder="Observações sobre a partida...">Partida muito equilibrada. João Silva conseguiu a vitória com um ippon no final do combate.</textarea>
            </div>
            <input type="hidden" id="editMatchId" value="${matchId}">
        `;
        document.getElementById('edit-match-content').innerHTML = content;
    }, 500);
}

function generateReport(matchId) {
    // Mostrar loading
    showToast('Gerando relatório...', 'info');
    
    // Simular geração de relatório
    setTimeout(() => {
        showToast(`Relatório da partida #${matchId} gerado com sucesso!`, 'success');
        
        // Simular download do relatório
        const link = document.createElement('a');
        link.href = '#'; // Aqui seria a URL real do relatório
        link.download = `relatorio-partida-${matchId}.pdf`;
        link.click();
    }, 2000);
}

function saveMatchChanges() {
    const matchId = document.getElementById('editMatchId').value;
    const form = document.getElementById('editMatchForm');
    
    // Validar formulário
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    // Mostrar loading
    showLoading('edit-match-content');
    showToast('Salvando alterações...', 'info');
    
    // Simular salvamento
    setTimeout(() => {
        showToast(`Partida #${matchId} atualizada com sucesso!`, 'success');
        
        // Fechar modal
        const modal = mdb.Modal.getInstance(document.getElementById('editMatchModal'));
        modal.hide();
        
        // Recarregar página
        setTimeout(() => {
            location.reload();
        }, 1000);
    }, 1500);
}

function printMatchDetails() {
    const content = document.getElementById('match-details-content').innerHTML;
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <html>
        <head>
            <title>Detalhes da Partida - KeyChart</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css">
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    margin: 20px; 
                    background: white;
                    color: black;
                }
                .no-print { display: none; }
                .match-result {
                    color: #333 !important;
                    font-weight: bold;
                }
                .badge {
                    border: 1px solid #333;
                    padding: 0.5em;
                }
                @media print {
                    body { margin: 0; }
                    .btn { display: none; }
                }
            </style>
        </head>
        <body>
            <div class="text-center mb-4">
                <h2>KeyChart - Sistema de Gerenciamento de Competições</h2>
                <h3>Relatório Detalhado da Partida</h3>
                <hr>
            </div>
            ${content}
            <div class="mt-4 text-center">
                <small class="text-muted">
                    Relatório gerado em ${new Date().toLocaleString('pt-BR')}
                </small>
            </div>
        </body>
        </html>
    `);
    printWindow.document.close();
    printWindow.print();
}

function clearFilters() {
    document.querySelector('input[name="q"]').value = '';
    document.querySelector('select[name="competicao"]').value = '';
    document.querySelector('input[name="data"]').value = '';
    document.querySelector('select[name="status"]').value = '';
    document.querySelector('.filters-card form').submit();
}

// Função para mostrar loading
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    element.innerHTML = `
        <div class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Carregando...</span>
            </div>
            <div class="mt-2">Carregando dados...</div>
        </div>
    `;
}

// Função para mostrar toast notifications
function showToast(message, type = 'info') {
    // Remover toasts existentes
    const existingToasts = document.querySelectorAll('.toast');
    existingToasts.forEach(toast => toast.remove());
    
    const toastHtml = `
        <div class="toast show align-items-center text-white bg-${type === 'success' ? 'success' : type === 'error' ? 'danger' : 'primary'} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi bi-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    const toastElement = document.createElement('div');
    toastElement.innerHTML = toastHtml;
    toastElement.style.position = 'fixed';
    toastElement.style.top = '20px';
    toastElement.style.right = '20px';
    toastElement.style.zIndex = '1055';
    
    document.body.appendChild(toastElement);
    
    // Auto-remove após 3 segundos
    setTimeout(() => {
        toastElement.remove();
    }, 3000);
}

// Função para alternar a sidebar
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');
    
    if (window.innerWidth <= 992) {
        // Comportamento mobile
        sidebar.classList.toggle('show');
    } else {
        // Comportamento desktop
        if (sidebar.style.width === '250px') {
            sidebar.style.width = '60px';
            content.style.marginLeft = '60px';
            document.querySelectorAll('.sidebar a span').forEach(el => {
                el.style.display = 'none';
            });
            document.querySelector('.sidebar .small').style.display = 'none';
        } else {
            sidebar.style.width = '250px';
            content.style.marginLeft = '250px';
            document.querySelectorAll('.sidebar a span').forEach(el => {
                el.style.display = 'inline';
            });
            document.querySelector('.sidebar .small').style.display = 'block';
        }
    }
}

// Fechar sidebar ao clicar no conteúdo (mobile)
document.getElementById('content').addEventListener('click', function() {
    if (window.innerWidth <= 992) {
        document.getElementById('sidebar').classList.remove('show');
    }
});

// Atualizar ao redimensionar
window.addEventListener('resize', function() {
    if (window.innerWidth > 992) {
        document.getElementById('sidebar').style.width = '250px';
        document.getElementById('content').style.marginLeft = '250px';
        document.querySelectorAll('.sidebar a span').forEach(el => {
            el.style.display = 'inline';
        });
        document.querySelector('.sidebar .small').style.display = 'block';
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.querySelector('input[type="text"]');
    const selectCompeticao = document.querySelector('select');
    const inputData = document.querySelector('input[type="date"]');
    const btnBuscar = document.querySelectorAll('button.btn-secondary')[1];
    const btnLimpar = document.querySelectorAll('button.btn-secondary')[0];
    const linhasPartidas = document.querySelectorAll("tbody tr");

    function normalizarTexto(texto) {
        return texto.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    }

    function aplicarFiltro() {
        const termoBusca = normalizarTexto(searchInput.value.trim());
        const competenciaSelecionada = selectCompeticao.value;
        const dataSelecionada = inputData.value;

        linhasPartidas.forEach(tr => {
            const textoCompleto = tr.innerText;
            const textoNormalizado = normalizarTexto(textoCompleto);

            const dataPartida = tr.children[0].textContent.trim().split('\n')[0].split("/").reverse().join("-");
            const competenciaMatch = competenciaSelecionada === "Todas as competições" || textoNormalizado.includes(normalizarTexto(competenciaSelecionada));
            const textoMatch = textoNormalizado.includes(termoBusca);
            const dataMatch = !dataSelecionada || dataSelecionada === dataPartida;

            if (competenciaMatch && textoMatch && dataMatch) {
                tr.style.display = "";
            } else {
                tr.style.display = "none";
            }
        });
    }

    function limparFiltros() {
        searchInput.value = "";
        selectCompeticao.selectedIndex = 0;
        inputData.value = "";
        aplicarFiltro();
    }

    btnBuscar.addEventListener("click", aplicarFiltro);
    btnLimpar.addEventListener("click", limparFiltros);

    // Filtro automático ao digitar
    searchInput.addEventListener("input", aplicarFiltro);
    selectCompeticao.addEventListener("change", aplicarFiltro);
    inputData.addEventListener("change", aplicarFiltro);
});

document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('.sidebar a');
    const activeLink = localStorage.getItem('activeLink');

    // Se tiver algo salvo, marca o link
    if (activeLink) {
        links.forEach(link => {
            if (link.href === activeLink) {
                link.classList.add('active');
            }
        });
    }

    // Quando clicar, salva o link clicado
    links.forEach(link => {
        link.addEventListener('click', function() {
            links.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            localStorage.setItem('activeLink', this.href);
        });
    });
});

// Função para exportar relatório
function exportarRelatorio() {
    showLoading('main-content');
    
    // Coletar dados dos filtros aplicados
    const form = document.querySelector('.filters-card form');
    const formData = new FormData(form);
    const params = new URLSearchParams(formData);
    
    // Adicionar parâmetro de exportação
    params.append('export', 'excel');
    
    // Criar link temporário para download
    const downloadLink = document.createElement('a');
    downloadLink.href = `${window.location.pathname}?${params.toString()}`;
    downloadLink.download = `relatorio_partidas_${new Date().toISOString().split('T')[0]}.xlsx`;
    
    // Simular clique para iniciar download
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
    
    hideLoading('main-content');
    
    showNotification('Relatório exportado com sucesso!', 'success');
}