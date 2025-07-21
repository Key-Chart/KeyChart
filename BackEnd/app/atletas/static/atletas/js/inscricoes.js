/**
 * Aplicação de Inscrições - Controller Principal
 */
const InscricoesApp = {
    // Estado da aplicação
    state: {
        currentStep: 1,
        selected: {
            competicao: { id: null, nome: '' },
            categoria: { id: null, nome: '' }
        },
        atleta: {
            dados: {
                nome: '',
                nascimento: '',
                sexo: '',
                idade: '',
                peso: '',
                altura: '',
                email: '',
                telefone: '',
                faixa: '',
                cidade: '',
                estado: '',
                academia: '',
                cidade_academia: '',
                estado_academia: ''
            },
            foto: null
        }
    },

    /**
     * Inicialização da aplicação
     */
    init() {
        this.bindEvents();
        this.populateStateSelects();
        this.debugInitialCheck();
        this.updateUI();
    },

    /**
     * Vinculação de eventos
     */
    bindEvents() {
        // Formulário do atleta
        document.getElementById('form-atleta')?.addEventListener('submit', (e) => {
            e.preventDefault();
            if (this.validateStep3()) {
                this.saveFormData();
                this.goToConfirmation();
            }
        });

        // Upload de foto
        document.getElementById('foto-atleta')?.addEventListener('change', (e) => {
            this.handleFotoUpload(e);
        });

        // Cálculo automático de idade
        document.getElementById('nascimento-atleta')?.addEventListener('change', () => {
            this.calcularIdade();
        });

        // Formulário de confirmação final
        document.getElementById('form-finalizar')?.addEventListener('submit', (e) => {
            this.handleFinalSubmit(e);
        });
    },

    /**
     * Preenche os selects de estado
     */
    populateStateSelects() {
        const states = [
            'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO',
            'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI',
            'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
        ];

        const selects = [
            document.getElementById('estado-atleta'),
            document.getElementById('estado-academia')
        ];

        selects.forEach(select => {
            if (select) {
                states.forEach(state => {
                    const option = document.createElement('option');
                    option.value = state;
                    option.textContent = state;
                    select.appendChild(option);
                });
            }
        });
    },

    /**
     * Validação do passo 3 (Cadastro do Atleta)
     */
    validateStep3() {
        const requiredFields = [
            'nome-atleta', 'nascimento-atleta', 'sexo-atleta',
            'email-atleta', 'telefone-atleta', 'faixa-atleta',
            'cidade-atleta', 'estado-atleta', 'academia-atleta',
            'cidade-academia', 'estado-academia'
        ];

        let isValid = true;

        requiredFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (!field || !field.value) {
                isValid = false;
                field.classList.add('is-invalid');
            } else {
                field.classList.remove('is-invalid');
            }
        });

        if (!isValid) {
            alert('Por favor, preencha todos os campos obrigatórios.');
        }

        return isValid;
    },

    /**
     * Navegação entre passos
     */
    nextStep(step, nome, id) {
        if (step === 1) {
            this.state.selected.competicao = { id, nome };
            this.updateCompeticaoUI(nome);
            this.loadCategoriesForCompetition(id);
        } else if (step === 2) {
            this.state.selected.categoria = { id, nome };
            this.updateCategoriaUI(nome);
        }

        this.state.currentStep = step + 1;
        this.updateStepUI(step);
        this.scrollToTop();
    },

    prevStep(currentStep) {
        this.state.currentStep = currentStep - 1;
        this.updateStepUI(currentStep, true);
        this.scrollToTop();
    },

    goToConfirmation() {
        this.state.currentStep = 4;
        this.updateStepUI(3);
        this.updateConfirmationUI();
    },

    /**
     * Manipulação de dados
     */
    saveFormData() {
        const fields = [
            'nome', 'nascimento', 'sexo', 'idade', 'peso', 'altura',
            'email', 'telefone', 'faixa', 'cidade', 'estado', 'academia',
            'cidade_academia', 'estado_academia'
        ];

        fields.forEach(field => {
            const element = document.getElementById(`${field}-atleta`) ||
                            document.getElementById(`${field}-academia`);
            if (element) {
                this.state.atleta.dados[field] = element.value;
            }
        });
    },

    handleFotoUpload(event) {
        const file = event.target.files?.[0];
        if (!file) return;

        if (file.size > 2 * 1024 * 1024) {
            alert('A imagem deve ter menos de 2MB');
            event.target.value = '';
            return;
        }

        this.state.atleta.foto = file;
        this.showImagePreview(file);
    },

    calcularIdade() {
        const nascimentoInput = document.getElementById('nascimento-atleta');
        if (!nascimentoInput || !nascimentoInput.value) return;

        const nascimento = new Date(nascimentoInput.value);
        if (isNaN(nascimento.getTime())) return;

        const hoje = new Date();
        let idade = hoje.getFullYear() - nascimento.getFullYear();
        const mes = hoje.getMonth() - nascimento.getMonth();

        if (mes < 0 || (mes === 0 && hoje.getDate() < nascimento.getDate())) {
            idade--;
        }

        const idadeInput = document.getElementById('idade-atleta');
        if (idadeInput) {
            idadeInput.value = idade;
            this.state.atleta.dados.idade = idade;
        }
    },

    /**
     * Carregamento de categorias
     */
    loadCategoriesForCompetition(competicaoId) {
        document.querySelectorAll('.categoria-row').forEach(row => {
            row.style.display = 'none';
        });

        const categoriasVisiveis = document.querySelectorAll(`.categoria-row[data-competicao-id="${competicaoId}"]`);

        if (categoriasVisiveis.length === 0) {
            const tbody = document.querySelector('#categorias-body');
            if (tbody) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="4" class="text-center text-muted">
                            Nenhuma categoria disponível para esta competição
                        </td>
                    </tr>`;
            }
        } else {
            categoriasVisiveis.forEach(row => {
                row.style.display = '';
            });
            this.filterCategories();
        }
    },

    filterCategories() {
        const tipo = document.getElementById('tipo-categoria')?.value.toLowerCase() || '';
        const sexo = document.getElementById('sexo-categoria')?.value.toLowerCase() || '';

        document.querySelectorAll('.categoria-row').forEach(row => {
            if (row.style.display === 'none') return;

            const rowTipo = row.getAttribute('data-tipo').toLowerCase();
            const rowSexo = row.getAttribute('data-sexo').toLowerCase();

            const show = (!tipo || rowTipo.includes(tipo)) &&
                        (!sexo || rowSexo.includes(sexo));

            row.style.display = show ? '' : 'none';
        });
    },

    /**
     * Atualização da UI
     */
    updateStepUI(step, isPrev = false) {
        const currentContent = document.getElementById(`step${step}-content`);
        const currentStepEl = document.getElementById(`step${step}`);

        if (currentContent) currentContent.classList.add('d-none');
        if (currentStepEl) {
            currentStepEl.classList.remove('active');
            if (!isPrev) currentStepEl.classList.add('completed');
        }

        const nextContent = document.getElementById(`step${this.state.currentStep}-content`);
        const nextStepEl = document.getElementById(`step${this.state.currentStep}`);

        if (nextContent) nextContent.classList.remove('d-none');
        if (nextStepEl) nextStepEl.classList.add('active');

        this.updateConnectors();
    },

    updateCompeticaoUI(nome) {
        const elements = [
            'competicao-selecionada',
            'confirm-competicao'
        ];

        elements.forEach(id => {
            const el = document.getElementById(id);
            if (el) el.textContent = nome;
        });
    },

    updateCategoriaUI(nome) {
        const elements = [
            'categoria-selecionada',
            'confirm-categoria'
        ];

        elements.forEach(id => {
            const el = document.getElementById(id);
            if (el) el.textContent = nome;
        });
    },

    updateConfirmationUI() {
        const a = this.state.atleta.dados;
        const s = this.state.selected;

        // Preenche campos ocultos do formulário final
        const hiddenFields = {
            'input-competicao': s.competicao.id,
            'input-categoria': s.categoria.id,
            'input-nome': a.nome,
            'input-nascimento': a.nascimento,
            'input-idade': a.idade,
            'input-sexo': a.sexo,
            'input-peso': a.peso,
            'input-altura': a.altura,  // Adicionado
            'input-email': a.email,    // Adicionado
            'input-telefone': a.telefone, // Adicionado
            'input-faixa': a.faixa,
            'input-cidade': a.cidade,
            'input-estado': a.estado,
            'input-academia': a.academia,
            'input-cidade-academia': a.cidade_academia,
            'input-estado-academia': a.estado_academia
        };

        Object.entries(hiddenFields).forEach(([id, value]) => {
            const el = document.getElementById(id);
            if (el) el.value = value || '';
        });

        // Atualiza a visualização de confirmação
        const confirmationFields = {
            'confirm-nome': a.nome,
            'confirm-nascimento': a.nascimento,
            'confirm-idade': a.idade ? `${a.idade} anos` : '-',
            'confirm-sexo': this.formatSexo(a.sexo),
            'confirm-peso': a.peso ? `${a.peso} kg` : '-',
            'confirm-altura': a.altura ? `${a.altura} cm` : '-',  // Adicionado
            'confirm-email': a.email || '-',                     // Adicionado
            'confirm-telefone': a.telefone || '-',               // Adicionado
            'confirm-faixa': this.formatFaixa(a.faixa),
            'confirm-cidade': a.cidade,
            'confirm-estado': a.estado,
            'confirm-academia': a.academia,
            'confirm-cidade-academia': a.cidade_academia,
            'confirm-estado-academia': a.estado_academia
        };

        Object.entries(confirmationFields).forEach(([id, value]) => {
            const el = document.getElementById(id);
            if (el) el.textContent = value;
        });

        // Atualiza a visualização da foto
        this.updateFotoPreview();
    },

    formatSexo(sexo) {
        const map = {
            'masculino': 'Masculino',
            'feminino': 'Feminino'
        };
        return map[sexo] || sexo;
    },

    formatFaixa(faixa) {
        const map = {
            'branca': 'Branca',
            'azul': 'Azul',
            'amarela': 'Amarela',
            'laranja': 'Laranja',
            'verde': 'Verde',
            'roxa': 'Roxa',
            'marrom': 'Marrom',
            'preta': 'Preta'
        };
        return map[faixa] || faixa;
    },

    updateFotoPreview() {
        const fotoContainer = document.getElementById('foto-preview-container');
        const fotoPreview = document.getElementById('foto-preview');

        if (this.state.atleta.foto) {
            const reader = new FileReader();
            reader.onload = (e) => {
                if (fotoPreview) fotoPreview.src = e.target.result;
                if (fotoContainer) fotoContainer.classList.remove('d-none');
            };
            reader.readAsDataURL(this.state.atleta.foto);
        } else if (fotoContainer) {
            fotoContainer.classList.add('d-none');
        }
    },

    /**
     * Manipulador de envio final
     */
    handleFinalSubmit(e) {
        e.preventDefault();
        const form = e.target;
        const submitBtn = document.getElementById('confirm-submit-btn');
        const originalText = submitBtn.innerHTML;

        // Mostrar estado de carregamento
        submitBtn.disabled = true;
        submitBtn.innerHTML = `
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            Processando...
        `;

        // Criar FormData para enviar a foto
        const formData = new FormData(form);
        if (this.state.atleta.foto) {
            formData.append('foto', this.state.atleta.foto);
        }

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': this.getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            } else {
                return response.json();
            }
        })
        .then(data => {
            if (data?.success) {
                this.showSuccessModal(data.message);
            } else if (data?.message) {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao enviar formulário');
        })
        .finally(() => {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        });
    },

    showSuccessModal(message) {
        const modal = document.getElementById('successModal');
        if (modal) {
            document.getElementById('successMessage').textContent = message || 'Inscrição realizada com sucesso!';
            modal.style.display = 'block';
        }
    },

    closeModal() {
        const modal = document.getElementById('successModal');
        if (modal) {
            modal.style.display = 'none';
        }
    },

    /**
     * Utilitários
     */
    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },

    showImagePreview(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const preview = document.getElementById('foto-preview');
            if (preview) {
                preview.src = e.target.result;
                const container = document.getElementById('foto-preview-container');
                if (container) container.classList.remove('d-none');
            }
        };
        reader.readAsDataURL(file);
    },

    updateConnectors() {
        document.querySelectorAll('.step').forEach((step, index) => {
            const connector = step.querySelector('.step-connector');
            if (connector) {
                connector.style.backgroundColor = index < this.state.currentStep - 1 ? '#198754' : '#dee2e6';
            }
        });
    },

    scrollToTop() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    },

    debugInitialCheck() {
        console.log('InscricoesApp inicializado - Versão 3.0');
    }
};

// Funções globais para chamadas do HTML
function nextStep(step, nome, id) {
    InscricoesApp.nextStep(step, nome, id);
}

function prevStep(step) {
    InscricoesApp.prevStep(step);
}

function filterCategories() {
    InscricoesApp.filterCategories();
}

function openEmailModal() {
    // Implementação do modal de email
    console.log('Abrir modal de email');
}

// Inicializa quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    InscricoesApp.init();
});