// Fechar sidebar ao clicar no conteúdo (mobile)
document.getElementById('content').addEventListener('click', function() {
    if (window.innerWidth <= 992) {
        document.getElementById('sidebar').classList.remove('show');
    }
});

// Atualizar ao redimensionar
window.addEventListener('resize', function() {
    if (window.innerWidth > 992) {
        document.getElementById('sidebar').style.width = '280px';
        document.getElementById('content').style.marginLeft = '280px';
        document.querySelectorAll('.sidebar a span').forEach(el => {
            el.style.display = 'inline';
        });
        document.querySelector('.sidebar .small').style.display = 'block';
    }
});

// Função para salvar alterações
function saveChanges() {
    // Lógica para salvar alterações
    alert('Alterações salvas com sucesso!');
    const modal = bootstrap.Modal.getInstance(document.getElementById('editModal'));
    modal.hide();
}

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

// Funções para os modais de impressão e exportação
function abrirModalImprimir() {
    document.getElementById('modalImprimir').style.display = 'block';
    document.getElementById('printProgress').style.width = '0%';
}

function abrirModalExportar() {
    document.getElementById('modalExportar').style.display = 'block';
    document.getElementById('exportProgress').style.width = '0%';
    document.getElementById('exportProgressContainer').style.display = 'none';
}

function fecharModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

function cancelarImpressao() {
    fecharModal('modalImprimir');
    // Lógica adicional de cancelamento se necessário
}

function iniciarImpressao() {
    const progressBar = document.getElementById('printProgress');
    let progress = 0;
    
    const interval = setInterval(() => {
        progress += 10;
        progressBar.style.width = `${progress}%`;
        
        if (progress >= 100) {
            clearInterval(interval);
            setTimeout(() => {
                fecharModal('modalImprimir');
                // Aqui você pode adicionar a lógica real de impressão
                window.print();
            }, 500);
        }
    }, 200);
}

function iniciarExportacao() {
    const format = document.querySelector('input[name="exportFormat"]:checked').value;
    const progressContainer = document.getElementById('exportProgressContainer');
    const progressBar = document.getElementById('exportProgress');
    
    progressContainer.style.display = 'block';
    let progress = 0;
    
    const interval = setInterval(() => {
        progress += 10;
        progressBar.style.width = `${progress}%`;
        
        if (progress >= 100) {
            clearInterval(interval);
            setTimeout(() => {
                fecharModal('modalExportar');
                // Lógica de exportação baseada no formato selecionado
                exportarDados(format);
            }, 500);
        }
    }, 200);
}

function exportarDados(format) {
    // Simulação de exportação - substitua pela sua lógica real
    let blob;
    let filename;
    let mimeType;
    
    switch(format) {
        case 'pdf':
            // Simular geração de PDF
            mimeType = 'application/pdf';
            filename = 'competicoes.pdf';
            blob = new Blob(['Conteúdo do PDF simulado'], {type: mimeType});
            break;
        case 'excel':
            // Simular geração de Excel
            mimeType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
            filename = 'competicoes.xlsx';
            blob = new Blob(['Conteúdo do Excel simulado'], {type: mimeType});
            break;
        case 'csv':
            // Simular geração de CSV
            mimeType = 'text/csv';
            filename = 'competicoes.csv';
            blob = new Blob(['Nome,Data,Local\nCopa Regional,10/03/2025,Estádio Municipal'], {type: mimeType});
            break;
    }
    
    // Criar link de download
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    // Mostrar mensagem de sucesso
    alert(`Arquivo ${filename} exportado com sucesso!`);
}

// Fechar modal ao clicar fora do conteúdo
window.onclick = function(event) {
    if (event.target.className === 'modal-custom') {
        event.target.style.display = 'none';
    }
}