/**
 * Sistema de Inscrições - JavaScript Controller
 * Versão 3.0 - Carregamento Direto de Categorias
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
    // Formulário principal
    document.getElementById('form-atleta')?.addEventListener('submit', (e) => {
      e.preventDefault();
      this.saveFormData();
      this.nextStep();
    });

    // Upload de foto
    document.getElementById('foto-atleta')?.addEventListener('change', (e) => {
      this.handleFotoUpload(e);
    });

    // Cálculo automático de idade
    document.getElementById('nascimento-atleta')?.addEventListener('change', () => {
      this.calcularIdade();
    });

    // Sidebar
    document.getElementById('toggleSidebar')?.addEventListener('click', () => {
      this.toggleSidebar();
    });

    // Modais
    document.querySelectorAll('[data-modal]').forEach(el => {
      el.addEventListener('click', (e) => {
        this.handleModalActions(e);
      });
    });
  },

  // Verificação inicial
  debugInitialCheck() {
    const competicaoRows = document.querySelectorAll('#step1-content tbody tr');
    console.log('[DEBUG] Competições no template:', competicaoRows.length > 1 ? competicaoRows.length - 1 : 0);

    if (competicaoRows.length <= 1) {
      console.warn('[DEBUG] Nenhuma competição encontrada no template. Verifique:');
      console.warn('1. Se existem competições com inscricoes_abertas=True no banco');
      console.warn('2. Se a view está passando o contexto corretamente');
    }
  },

  // Controle de fluxo
  nextStep(stepData = {}) {
    const { step, nome, id } = stepData;

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

  // Manipulação de dados
  saveFormData() {
    const fields = [
      'nome', 'nascimento', 'sexo', 'idade', 'peso', 'altura',
      'email', 'telefone', 'faixa', 'cidade', 'estado', 'academia'
    ];

    fields.forEach(field => {
      this.state.atleta.dados[field] =
        document.getElementById(`${field}-atleta`)?.value || '';
    });

    this.updateConfirmationUI();
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

  // Cálculos
  calcularIdade() {
    const nascimento = new Date(document.getElementById('nascimento-atleta').value);
    if (isNaN(nascimento.getTime())) return;

    const hoje = new Date();
    let idade = hoje.getFullYear() - nascimento.getFullYear();
    const mes = hoje.getMonth() - nascimento.getMonth();

    if (mes < 0 || (mes === 0 && hoje.getDate() < nascimento.getDate())) {
      idade--;
    }

    document.getElementById('idade-atleta').value = idade;
    this.state.atleta.dados.idade = idade;
  },

  // Carregamento de categorias sem AJAX
  loadCategoriesForCompetition(competicaoId) {
    // Esconde todas as categorias primeiro
    document.querySelectorAll('.categoria-row').forEach(row => {
      row.style.display = 'none';
    });

    // Mostra apenas as categorias da competição selecionada
    const categoriasVisiveis = document.querySelectorAll(`.categoria-row[data-competicao-id="${competicaoId}"]`);

    if (categoriasVisiveis.length === 0) {
      document.querySelector('#categorias-body').innerHTML = `
        <tr>
          <td colspan="4" class="text-center text-muted">
            Nenhuma categoria disponível para esta competição
          </td>
        </tr>`;
    } else {
      categoriasVisiveis.forEach(row => {
        row.style.display = '';
      });
      this.filterCategories(); // Aplica os filtros atuais
    }
  },

  // Filtro de categorias
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

  // Finalização
  finalizarInscricao() {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '{% url "salvar_inscricao" %}';
    form.enctype = 'multipart/form-data';
    form.style.display = 'none';

    // CSRF Token
    this.addHiddenInput(form, 'csrfmiddlewaretoken', '{{ csrf_token }}');

    // Dados da inscrição
    this.addHiddenInput(form, 'competicao_id', this.state.selected.competicao.id);
    this.addHiddenInput(form, 'categoria_id', this.state.selected.categoria.id);

    // Dados do atleta
    Object.entries(this.state.atleta.dados).forEach(([key, value]) => {
      this.addHiddenInput(form, `atleta_${key}`, value);
    });

    // Foto do atleta
    if (this.state.atleta.foto) {
      const fileInput = document.createElement('input');
      fileInput.type = 'file';
      fileInput.name = 'atleta_foto';

      const dataTransfer = new DataTransfer();
      dataTransfer.items.add(this.state.atleta.foto);
      fileInput.files = dataTransfer.files;

      form.appendChild(fileInput);
    }

    document.body.appendChild(form);
    form.submit();
  },

  // Atualização da UI
  updateStepUI(step, isPrev = false) {
    // Passo atual
    const currentContent = document.getElementById(`step${step}-content`);
    const currentStepEl = document.getElementById(`step${step}`);

    if (!isPrev) {
      currentContent?.classList.add('d-none');
      currentStepEl?.classList.remove('active');
      currentStepEl?.classList.add('completed');
    } else {
      currentContent?.classList.add('d-none');
      currentStepEl?.classList.remove('active');
    }

    // Novo passo
    document.getElementById(`step${this.state.currentStep}-content`)?.classList.remove('d-none');
    document.getElementById(`step${this.state.currentStep}`)?.classList.add('active');

    this.updateConnectors();
  },

  updateCompeticaoUI(nome) {
    const competicaoElement = document.getElementById('competicao-selecionada');
    const confirmCompeticao = document.getElementById('confirm-competicao');
    const assuntoEmail = document.getElementById('assuntoEmail');

    if (competicaoElement) competicaoElement.textContent = nome;
    if (confirmCompeticao) confirmCompeticao.textContent = nome;
    if (assuntoEmail) assuntoEmail.value = `Ficha de Inscrição - ${nome}`;
  },

  updateCategoriaUI(nome) {
    const categoriaElement = document.getElementById('categoria-selecionada');
    const confirmCategoria = document.getElementById('confirm-categoria');

    if (categoriaElement) categoriaElement.textContent = nome;
    if (confirmCategoria) confirmCategoria.textContent = nome;
  },

  updateConfirmationUI() {
    const a = this.state.atleta.dados;

    document.getElementById('confirm-nome').textContent = a.nome;
    document.getElementById('confirm-nascimento').textContent = this.formatDate(a.nascimento);
    document.getElementById('confirm-sexo').textContent = this.capitalize(a.sexo);
    document.getElementById('confirm-idade').textContent = a.idade ? `${a.idade} anos` : '-';
    document.getElementById('confirm-peso').textContent = a.peso || '-';
    document.getElementById('confirm-faixa').textContent = this.capitalize(a.faixa);
    document.getElementById('confirm-cidade').textContent = a.cidade;
    document.getElementById('confirm-estado').textContent = a.estado;
    document.getElementById('confirm-academia').textContent = a.academia;
  },

  showImagePreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      const preview = document.getElementById('foto-preview');
      if (preview) {
        preview.src = e.target.result;
        document.getElementById('foto-preview-container')?.classList.remove('d-none');
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

  // Utilitários
  addHiddenInput(form, name, value) {
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = name;
    input.value = value || '';
    form.appendChild(input);
  },

  formatDate(dateString) {
    return dateString ? new Date(dateString).toLocaleDateString('pt-BR') : '-';
  },

  capitalize(str) {
    return str?.charAt(0).toUpperCase() + str?.slice(1) || '';
  },

  scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  },

  toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');
    const icon = document.querySelector('#toggleSidebar i');

    sidebar?.classList.toggle('collapsed');
    content?.classList.toggle('collapsed');

    if (icon) {
      icon.classList.toggle('bi-list');
      icon.classList.toggle('bi-chevron-right');
    }
  },

  handleModalActions(e) {
    const action = e.target.closest('[data-modal]').dataset.modal;

    if (action === 'open-email') {
      document.getElementById('emailModal').style.display = 'block';
    } else if (action === 'close') {
      e.target.closest('.modal-email').style.display = 'none';
    }
  }
};

// Inicializa a aplicação quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
  InscricoesApp.init();
});

// Funções globais para chamadas diretas do HTML
function nextStep(step, nome, id) {
  InscricoesApp.nextStep({step, nome, id});
}

function prevStep(step) {
  InscricoesApp.prevStep(step);
}

function filterCategories() {
  InscricoesApp.filterCategories();
}