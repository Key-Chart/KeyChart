const InscricoesApp = {
  // Estado da aplicação
  state: {
    currentStep: 1,
    selected: {
      competicao: { id: null, nome: '' },
      categoria: { id: null, nome: '' },
      academia: { id: null, nome: '' }
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
        academia: ''
      },
      foto: null
    }
  },

  // Inicialização
  init() {
    this.bindEvents();
    this.debugInitialCheck();
    this.updateUI();
  },

  // Vinculação de eventos
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

  // Validação do passo 3
  validateStep3() {
    const requiredFields = [
      'nome-atleta', 'nascimento-atleta', 'sexo-atleta',
      'email-atleta', 'telefone-atleta', 'faixa-atleta',
      'cidade-atleta', 'estado-atleta', 'academia-atleta'
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

  // Navegação entre passos
  nextStep(step, nome, id) {
    if (step === 1) {
      this.state.selected.competicao = { id, nome };
      this.updateCompeticaoUI(nome);
      this.loadCategoriesForCompetition(id);
    }
    else if (step === 2) {
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

  // Manipulação de dados
  saveFormData() {
    const fields = [
      'nome', 'nascimento', 'sexo', 'idade', 'peso', 'altura',
      'email', 'telefone', 'faixa', 'cidade', 'estado', 'academia'
    ];

    fields.forEach(field => {
      const element = document.getElementById(`${field}-atleta`);
      if (element) {
        this.state.atleta.dados[field] = element.value;
      }
    });

    // Atualiza academia selecionada
    const academiaSelect = document.getElementById('academia-atleta');
    if (academiaSelect) {
      this.state.selected.academia = {
        id: academiaSelect.value,
        nome: academiaSelect.options[academiaSelect.selectedIndex]?.text
      };
    }
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

  // Cálculo de idade
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

  // Carregamento de categorias
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

  // Atualização da UI
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
      'input-faixa': a.faixa,
      'input-cidade': a.cidade,
      'input-estado': a.estado,
      'input-academia': a.academia
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
      'confirm-sexo': a.sexo,
      'confirm-peso': a.peso ? `${a.peso} kg` : '-',
      'confirm-faixa': a.faixa,
      'confirm-cidade': a.cidade,
      'confirm-estado': a.estado,
      'confirm-academia': a.academia
    };

    Object.entries(confirmationFields).forEach(([id, value]) => {
      const el = document.getElementById(id);
      if (el) el.textContent = value;
    });

    // Atualiza a visualização da foto
    const fotoContainer = document.getElementById('foto-preview-container');
    const fotoPreview = document.getElementById('foto-preview');

    if (this.state.atleta.foto && fotoPreview) {
      const reader = new FileReader();
      reader.onload = (e) => {
        fotoPreview.src = e.target.result;
        if (fotoContainer) fotoContainer.classList.remove('d-none');
      };
      reader.readAsDataURL(this.state.atleta.foto);
    } else if (fotoContainer) {
      fotoContainer.classList.add('d-none');
    }
  },

  // Manipulador de envio final
  handleFinalSubmit(e) {
    const submitBtn = document.getElementById('confirm-submit-btn');
    if (!submitBtn) return;

    const originalText = submitBtn.innerHTML;

    // Mostrar estado de carregamento
    submitBtn.disabled = true;
    submitBtn.innerHTML = `
      <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
      Processando...
    `;

    // Se houver foto, precisamos enviar via FormData
    if (this.state.atleta.foto) {
      const form = e.target;
      const formData = new FormData(form);
      formData.append('foto', this.state.atleta.foto);

      fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
          'X-CSRFToken': this.getCookie('csrftoken')
        }
      })
      .then(response => {
        if (response.redirected) {
          window.location.href = response.url;
        } else {
          return response.json().then(data => {
            if (data.success) {
              this.showSuccessModal(data.message);
            } else {
              alert(data.message || 'Erro ao processar inscrição');
            }
          });
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
    } else {
      // Se não houver foto, o formulário será enviado normalmente
      return true;
    }

    e.preventDefault();
  },

  // Utilitários
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
    console.log('InscricoesApp inicializado');
  }
};

// Inicializa quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
  InscricoesApp.init();
});

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