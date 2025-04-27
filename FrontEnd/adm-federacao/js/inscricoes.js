// Controle dos passos do formulário
let currentStep = 1;
        
// Dados da inscrição
const inscricaoData = {
    competicao: '',
    categoria: '',
    atleta: {
        nome: '',
        nascimento: '',
        sexo: '',
        peso: '',
        faixa: '',
        academia: '',
        foto: null
    }
};

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    updateConnectors();
    
    // Configura o formulário de atleta
    document.getElementById('form-atleta').addEventListener('submit', function(e) {
        e.preventDefault();
        saveAtletaData();
        nextStep(3);
    });
    
    // Configura o formulário de email
    document.getElementById('emailForm').addEventListener('submit', function(e) {
        e.preventDefault();
        sendEmail();
    });
    
    // Configura o input de foto
    document.getElementById('foto-atleta').addEventListener('change', function(e) {
        if (e.target.files && e.target.files[0]) {
            const file = e.target.files[0];
            
            // Verifica o tamanho do arquivo (max 2MB)
            if (file.size > 2 * 1024 * 1024) {
                alert('O arquivo é muito grande. Por favor, selecione uma imagem menor que 2MB.');
                e.target.value = '';
                return;
            }
            
            inscricaoData.atleta.foto = file;
            
            // Mostra preview da foto
            const reader = new FileReader();
            reader.onload = function(event) {
                const previewContainer = document.getElementById('foto-preview-container');
                const previewImage = document.getElementById('foto-preview');
                
                previewImage.src = event.target.result;
                previewContainer.classList.remove('d-none');
            };
            reader.readAsDataURL(file);
        }
    });
    
    // Configura o botão de toggle da sidebar
    document.getElementById('toggleSidebar').addEventListener('click', toggleSidebar);
    
    // Fechar modal ao clicar fora
    window.addEventListener('click', function(event) {
        const emailModal = document.getElementById('emailModal');
        if (event.target === emailModal) {
            closeEmailModal();
        }
        
        const successModal = document.getElementById('successModal');
        if (event.target === successModal) {
            closeSuccessModal();
        }
    });
});

// Função para salvar dados do atleta
function saveAtletaData() {
    inscricaoData.atleta.nome = document.getElementById('nome-atleta').value;
    inscricaoData.atleta.nascimento = document.getElementById('nascimento-atleta').value;
    inscricaoData.atleta.sexo = document.getElementById('sexo-atleta').value;
    inscricaoData.atleta.peso = document.getElementById('peso-atleta').value || '-';
    inscricaoData.atleta.faixa = document.getElementById('faixa-atleta').value;
    inscricaoData.atleta.academia = document.getElementById('academia-atleta').value;
    
    // Atualiza os campos de confirmação
    document.getElementById('confirm-nome').textContent = inscricaoData.atleta.nome;
    document.getElementById('confirm-nascimento').textContent = formatDate(inscricaoData.atleta.nascimento);
    document.getElementById('confirm-sexo').textContent = capitalizeFirstLetter(inscricaoData.atleta.sexo);
    document.getElementById('confirm-peso').textContent = inscricaoData.atleta.peso;
    document.getElementById('confirm-faixa').textContent = capitalizeFirstLetter(inscricaoData.atleta.faixa);
    document.getElementById('confirm-academia').textContent = inscricaoData.atleta.academia;
}

// Função para formatar data
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}

// Função para capitalizar primeira letra
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

// Função para filtrar categorias
function filterCategories() {
    const tipo = document.getElementById('tipo-categoria').value.toLowerCase();
    const sexo = document.getElementById('sexo-categoria').value.toLowerCase();
    const rows = document.querySelectorAll('#categorias-table tbody tr');
    
    rows.forEach(row => {
        const rowTipo = row.getAttribute('data-tipo').toLowerCase();
        const rowSexo = row.getAttribute('data-sexo').toLowerCase();
        
        const showTipo = !tipo || rowTipo.includes(tipo);
        const showSexo = !sexo || rowSexo.includes(sexo);
        
        if (showTipo && showSexo) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Função para avançar para o próximo passo
function nextStep(step, data = null) {
    // Salva os dados conforme avança
    if (step === 1) {
        inscricaoData.competicao = data;
        document.getElementById('competicao-selecionada').textContent = data;
        document.getElementById('confirm-competicao').textContent = data;
        document.getElementById('assuntoEmail').value = `Ficha de Inscrição - ${data}`;
    } else if (step === 2) {
        inscricaoData.categoria = data;
        document.getElementById('categoria-selecionada').textContent = data;
        document.getElementById('confirm-categoria').textContent = data;
    } else if (step === 3) {
        // Os dados do atleta são salvos no submit do formulário
    }
    
    // Esconde o passo atual
    document.getElementById(`step${step}-content`).classList.add('d-none');
    document.getElementById(`step${step}`).classList.remove('active');
    document.getElementById(`step${step}`).classList.add('completed');
    
    // Mostra o próximo passo
    currentStep = step + 1;
    document.getElementById(`step${currentStep}-content`).classList.remove('d-none');
    document.getElementById(`step${currentStep}`).classList.add('active');
    
    // Atualiza conectores
    updateConnectors();
    
    // Rola para o topo do próximo passo
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Função para voltar ao passo anterior
function prevStep(step) {
    // Esconde o passo atual
    document.getElementById(`step${step}-content`).classList.add('d-none');
    document.getElementById(`step${step}`).classList.remove('active');
    
    // Mostra o passo anterior
    currentStep = step - 1;
    document.getElementById(`step${currentStep}-content`).classList.remove('d-none');
    document.getElementById(`step${currentStep}`).classList.add('active');
    document.getElementById(`step${currentStep}`).classList.remove('completed');
    
    // Atualiza conectores
    updateConnectors();
    
    // Rola para o topo do passo anterior
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Função para atualizar os conectores entre os passos
function updateConnectors() {
    const steps = document.querySelectorAll('.step');
    steps.forEach((step, index) => {
        const connector = step.querySelector('.step-connector');
        if (connector) {
            if (index < currentStep - 1) {
                connector.style.backgroundColor = '#198754';
            } else {
                connector.style.backgroundColor = '#dee2e6';
            }
        }
    });
}

// Função para finalizar a inscrição
function finalizarInscricao() {
    // Aqui você normalmente enviaria os dados para o servidor
    // Para demonstração, vamos simular o envio
    
    // Mostra o modal de sucesso
    document.getElementById('successModal').style.display = 'block';
    
    // Limpa o formulário após 5 segundos (apenas para demonstração)
    setTimeout(() => {
        resetForm();
    }, 5000);
}

// Função para resetar o formulário
function resetForm() {
    // Reseta os dados
    inscricaoData.competicao = '';
    inscricaoData.categoria = '';
    inscricaoData.atleta = {
        nome: '',
        nascimento: '',
        sexo: '',
        peso: '',
        faixa: '',
        academia: '',
        foto: null
    };
    
    // Reseta os campos do formulário
    document.getElementById('form-atleta').reset();
    document.getElementById('foto-atleta').value = '';
    document.getElementById('foto-preview-container').classList.add('d-none');
    
    // Volta para o primeiro passo
    document.querySelectorAll('.step-content').forEach(el => {
        el.classList.add('d-none');
    });
    document.getElementById('step1-content').classList.remove('d-none');
    
    document.querySelectorAll('.step').forEach((step, index) => {
        step.classList.remove('active', 'completed');
        if (index === 0) {
            step.classList.add('active');
        }
    });
    
    currentStep = 1;
    updateConnectors();
}

// Função para abrir o modal de email
function openEmailModal() {
    document.getElementById('emailModal').style.display = 'block';
}

// Função para fechar o modal de email
function closeEmailModal() {
    document.getElementById('emailModal').style.display = 'none';
}

// Função para fechar o modal de sucesso
function closeSuccessModal() {
    document.getElementById('successModal').style.display = 'none';
}

// Função para enviar email (simulado)
function sendEmail() {
    const email = document.getElementById('emailDestino').value;
    const assunto = document.getElementById('assuntoEmail').value;
    const mensagem = document.getElementById('mensagemEmail').value;
    
    // Mostra spinner de carregamento
    document.getElementById('emailSubmitText').classList.add('d-none');
    document.getElementById('emailLoadingSpinner').classList.remove('d-none');
    
    // Simula o envio do email (em uma aplicação real, seria uma chamada AJAX)
    setTimeout(() => {
        // Esconde spinner
        document.getElementById('emailSubmitText').classList.remove('d-none');
        document.getElementById('emailLoadingSpinner').classList.add('d-none');
        
        // Mostra mensagem de sucesso
        alert(`Email enviado com sucesso para: ${email}\nAssunto: ${assunto}`);
        
        // Fecha o modal
        closeEmailModal();
    }, 1500);
}

// Função para recolher/expandir a barra lateral
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');
    const toggleBtn = document.getElementById('toggleSidebar');
    
    sidebar.classList.toggle('collapsed');
    content.classList.toggle('collapsed');
    
    // Alterna ícone do botão
    const icon = toggleBtn.querySelector('i');
    if (sidebar.classList.contains('collapsed')) {
        icon.classList.remove('bi-list');
        icon.classList.add('bi-chevron-right');
    } else {
        icon.classList.remove('bi-chevron-right');
        icon.classList.add('bi-list');
    }
}
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');
    const toggleBtn = document.getElementById('toggleSidebar');
    
    sidebar.classList.toggle('collapsed');
    content.classList.toggle('collapsed');
    
    // Não precisamos mais mudar o ícone, pois será sempre bi-list
}