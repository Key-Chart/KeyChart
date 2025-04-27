document.addEventListener('DOMContentLoaded', function() {
    // Elementos do formulário
    const filterForm = document.querySelector('.row.g-3');
    const filterName = document.getElementById('filterName');
    const filterAge = document.getElementById('filterAge');
    const filterCategory = document.getElementById('filterCategory');
    const clearButton = document.querySelector('.btn.btn-secondary');
    const athleteRows = document.querySelectorAll('tbody tr');
    
    // Modal elements (simulados para validação)
    const editModal = {
        form: document.createElement('form'),
        name: document.createElement('input'),
        age: document.createElement('input'),
        category: document.createElement('select'),
        status: document.createElement('select')
    };
    
    // Inicialização dos elementos do modal (simulação)
    function initModalElements() {
        editModal.form.id = 'editAthleteForm';
        editModal.name.id = 'editAthleteName';
        editModal.name.type = 'text';
        editModal.name.required = true;
        editModal.age.id = 'editAthleteAge';
        editModal.age.type = 'number';
        editModal.age.min = '1';
        editModal.age.max = '120';
        editModal.age.required = true;
        editModal.category.id = 'editAthleteCategory';
        editModal.category.innerHTML = `
            <option value="">Selecione uma categoria</option>
            <option value="kata">Kata</option>
            <option value="kumite">Kumite</option>
        `;
        editModal.status.id = 'editAthleteStatus';
        editModal.status.innerHTML = `
            <option value="">Selecione um status</option>
            <option value="active">Ativo</option>
            <option value="inactive">Inativo</option>
        `;
        
        editModal.form.appendChild(editModal.name);
        editModal.form.appendChild(editModal.age);
        editModal.form.appendChild(editModal.category);
        editModal.form.appendChild(editModal.status);
    }
    
    initModalElements();
    
    // Validação do formulário de filtros
    function validateFilters() {
        let isValid = true;
        
        // Validação do nome (se preenchido)
        if (filterName.value.trim() !== '') {
            if (filterName.value.trim().length < 3) {
                showError(filterName, 'O nome deve ter pelo menos 3 caractere');
                isValid = false;
            } else {
                clearError(filterName);
            }
        }
        
        // Validação da idade (se preenchida)
        if (filterAge.value.trim() !== '') {
            const age = parseInt(filterAge.value);
            if (isNaN(age) || age < 1 || age > 120) {
                showError(filterAge, 'Idade deve ser entre 1 e 120 anos');
                isValid = false;
            } else {
                clearError(filterAge);
            }
        }
        
        return isValid;
    }
    
    // Validação do formulário de edição
    function validateEditForm() {
        let isValid = true;
        
        // Validação do nome
        if (editModal.name.value.trim() === '') {
            showError(editModal.name, 'Nome é obrigatório');
            isValid = false;
        } else if (editModal.name.value.trim().length < 3) {
            showError(editModal.name, 'Nome deve ter pelo menos 3 caracteres');
            isValid = false;
        } else {
            clearError(editModal.name);
        }
        
        // Validação da idade
        if (editModal.age.value.trim() === '') {
            showError(editModal.age, 'Idade é obrigatória');
            isValid = false;
        } else {
            const age = parseInt(editModal.age.value);
            if (isNaN(age) || age < 1 || age > 120) {
                showError(editModal.age, 'Idade deve ser entre 1 e 120 anos');
                isValid = false;
            } else {
                clearError(editModal.age);
            }
        }
        
        // Validação da categoria
        if (editModal.category.value === '') {
            showError(editModal.category, 'Categoria é obrigatória');
            isValid = false;
        } else {
            clearError(editModal.category);
        }
        
        // Validação do status
        if (editModal.status.value === '') {
            showError(editModal.status, 'Status é obrigatório');
            isValid = false;
        } else {
            clearError(editModal.status);
        }
        
        return isValid;
    }
    
    // Mostrar erro
    function showError(input, message) {
        const formControl = input.closest('.form-control') || input.closest('.form-select') || input;
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        
        // Remove mensagens de erro existentes
        clearError(input);
        
        // Adiciona classe de inválido e mensagem
        formControl.classList.add('is-invalid');
        formControl.parentNode.appendChild(errorDiv);
    }
    
    // Limpar erro
    function clearError(input) {
        const formControl = input.closest('.form-control') || input.closest('.form-select') || input;
        formControl.classList.remove('is-invalid');
        
        const errorDiv = formControl.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            formControl.parentNode.removeChild(errorDiv);
        }
    }
    
    // Aplicar filtros
    function applyFilters() {
        if (!validateFilters()) {
            return;
        }
        
        const nameFilter = filterName.value.trim().toLowerCase();
        const ageFilter = filterAge.value.trim();
        const categoryFilter = filterCategory.value;
        
        athleteRows.forEach(row => {
            const name = row.querySelector('.fw-bold').textContent.toLowerCase();
            const ageText = row.querySelector('td:nth-child(2)').textContent;
            const age = parseInt(ageText);
            const category = row.querySelector('td:nth-child(3) span').textContent.toLowerCase();
            
            const nameMatch = nameFilter === '' || name.includes(nameFilter);
            const ageMatch = ageFilter === '' || age === parseInt(ageFilter);
            const categoryMatch = categoryFilter === '' || category === categoryFilter;
            
            if (nameMatch && ageMatch && categoryMatch) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }
    
    // Limpar filtros
    function clearFilters() {
        filterName.value = '';
        filterAge.value = '';
        filterCategory.value = '';
        
        clearError(filterName);
        clearError(filterAge);
        
        athleteRows.forEach(row => {
            row.style.display = '';
        });
    }
    
    // Simular edição de atleta
    function simulateEditAthlete(button) {
        const row = button.closest('tr');
        const name = row.querySelector('.fw-bold').textContent;
        const ageText = row.querySelector('td:nth-child(2)').textContent;
        const age = parseInt(ageText);
        const category = row.querySelector('td:nth-child(3) span').textContent.toLowerCase();
        const status = row.querySelector('td:nth-child(4) span').textContent.toLowerCase();
        
        // Preencher modal de edição
        editModal.name.value = name;
        editModal.age.value = age;
        editModal.category.value = category;
        editModal.status.value = status === 'ativo' ? 'active' : 'inactive';
        
        // Simular abertura do modal
        console.log('Modal de edição aberto para:', name);
        
        // Simular envio do formulário de edição
        editModal.form.onsubmit = function(e) {
            e.preventDefault();
            
            if (validateEditForm()) {
                console.log('Dados válidos, enviando...');
                // Aqui você faria a requisição AJAX ou atualizaria a tabela
                
                // Simular fechamento do modal
                console.log('Modal fechado após edição');
            }
        };
    }
    
    // Event Listeners
    filterName.addEventListener('input', applyFilters);
    filterAge.addEventListener('input', applyFilters);
    filterCategory.addEventListener('change', applyFilters);
    clearButton.addEventListener('click', clearFilters);
    
    // Adicionar eventos aos botões de edição
    document.querySelectorAll('.btn-outline-warning').forEach(button => {
        button.addEventListener('click', function() {
            simulateEditAthlete(this);
        });
    });
    
    // Adicionar eventos aos botões de ativar/inativar
    document.querySelectorAll('.btn-outline-danger, .btn-outline-success').forEach(button => {
        button.addEventListener('click', function() {
            const action = this.classList.contains('btn-outline-danger') ? 'inativar' : 'ativar';
            const athleteName = this.closest('tr').querySelector('.fw-bold').textContent;
            console.log(`Modal de confirmação para ${action} o atleta ${athleteName}`);
        });
    });
    
    // Adicionar eventos aos botões de paginação
    document.querySelectorAll('.pagination .page-link').forEach(link => {
        if (!link.parentElement.classList.contains('disabled') && 
            !link.parentElement.classList.contains('active')) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('Página alterada para:', this.textContent.trim());
            });
        }
    });
    
    // Adicionar eventos aos botões de impressão e exportação
    document.querySelector('.btn-outline-secondary.me-2').addEventListener('click', function() {
        console.log('Imprimir lista de atletas');
    });
    
    document.querySelector('.btn-outline-secondary:not(.me-2)').addEventListener('click', function() {
        console.log('Exportar lista de atletas');
    });
});

// Função para alternar a sidebar
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');
    
    if (window.innerWidth <= 992) {
        // Comportamento mobile
        sidebar.classList.toggle('show');
    } else {
        // Comportamento desktop
        if (sidebar.style.width === '280px') {
            sidebar.style.width = '60px';
            content.style.marginLeft = '60px';
            document.querySelectorAll('.sidebar a span').forEach(el => {
                el.style.display = 'none';
            });
            document.querySelector('.sidebar .small').style.display = 'none';
        } else {
            sidebar.style.width = '280px';
            content.style.marginLeft = '280px';
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
        document.getElementById('sidebar').style.width = '280px';
        document.getElementById('content').style.marginLeft = '280px';
        document.querySelectorAll('.sidebar a span').forEach(el => {
            el.style.display = 'inline';
        });
        document.querySelector('.sidebar .small').style.display = 'block';
    }
});

// Inicializar tooltips
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-mdb-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new mdb.Tooltip(tooltipTriggerEl);
    });
});