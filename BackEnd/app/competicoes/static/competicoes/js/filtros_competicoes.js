/**
 * Sistema de Filtros Avançados para Competições
 * Autor: Sistema KeyChart
 * Versão: 1.0
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elementos do DOM
    const toggleFiltersBtn = document.getElementById('toggleFilters');
    const toggleIcon = document.getElementById('toggleIcon');
    const filtersContainer = document.getElementById('filtersContainer');
    const filterForm = document.getElementById('filterForm');
    const autoFilterToggle = document.getElementById('autoFilterToggle');
    const autoFilterStatus = document.getElementById('autoFilterStatus');
    const clearSearchBtn = document.getElementById('clearSearch');
    const searchInput = document.getElementById('searchInput');
    const viewToggle = document.getElementById('viewToggle');
    const cardViewToggle = document.getElementById('cardViewToggle');
    const tableView = document.getElementById('tableView');
    const cardView = document.getElementById('cardView');

    // Estado dos filtros
    let filtersCollapsed = localStorage.getItem('filtersCollapsed') === 'true';
    let autoFilterEnabled = localStorage.getItem('autoFilterEnabled') === 'true';
    let currentView = localStorage.getItem('competitionsView') || 'table';

    // Inicializar estados
    initializeFiltersState();
    initializeViewState();
    initializeAutoFilter();

    // Event Listeners
    if (toggleFiltersBtn) {
        toggleFiltersBtn.addEventListener('click', toggleFilters);
    }

    if (autoFilterToggle) {
        autoFilterToggle.addEventListener('click', toggleAutoFilter);
    }

    if (clearSearchBtn) {
        clearSearchBtn.addEventListener('click', clearSearch);
    }

    if (viewToggle) {
        viewToggle.addEventListener('click', () => switchView('table'));
    }

    if (cardViewToggle) {
        cardViewToggle.addEventListener('click', () => switchView('cards'));
    }

    // Auto filtro em tempo real
    if (autoFilterEnabled) {
        setupAutoFilter();
    }

    // Atalhos de teclado
    setupKeyboardShortcuts();

    /**
     * Inicializa o estado dos filtros
     */
    function initializeFiltersState() {
        if (filtersCollapsed) {
            document.body.classList.add('filters-collapsed');
            if (toggleIcon) {
                toggleIcon.classList.remove('bi-chevron-up');
                toggleIcon.classList.add('bi-chevron-down');
            }
        }
    }

    /**
     * Inicializa o estado da visualização
     */
    function initializeViewState() {
        if (currentView === 'cards') {
            switchView('cards');
        }
    }

    /**
     * Inicializa o auto filtro
     */
    function initializeAutoFilter() {
        if (autoFilterEnabled && autoFilterStatus && autoFilterToggle) {
            autoFilterStatus.textContent = 'Ligada';
            autoFilterToggle.classList.remove('btn-outline-info');
            autoFilterToggle.classList.add('btn-info', 'text-white');
            document.body.classList.add('auto-search-active');
        }
    }

    /**
     * Alterna o estado dos filtros (expandido/colapsado)
     */
    function toggleFilters() {
        filtersCollapsed = !filtersCollapsed;
        localStorage.setItem('filtersCollapsed', filtersCollapsed);
        
        if (filtersCollapsed) {
            document.body.classList.add('filters-collapsed');
            if (toggleIcon) {
                toggleIcon.classList.remove('bi-chevron-up');
                toggleIcon.classList.add('bi-chevron-down');
            }
        } else {
            document.body.classList.remove('filters-collapsed');
            if (toggleIcon) {
                toggleIcon.classList.remove('bi-chevron-down');
                toggleIcon.classList.add('bi-chevron-up');
            }
        }
    }

    /**
     * Alterna o auto filtro
     */
    function toggleAutoFilter() {
        autoFilterEnabled = !autoFilterEnabled;
        localStorage.setItem('autoFilterEnabled', autoFilterEnabled);
        
        if (autoFilterEnabled) {
            if (autoFilterStatus) autoFilterStatus.textContent = 'Ligada';
            if (autoFilterToggle) {
                autoFilterToggle.classList.remove('btn-outline-info');
                autoFilterToggle.classList.add('btn-info', 'text-white');
            }
            document.body.classList.add('auto-search-active');
            setupAutoFilter();
        } else {
            if (autoFilterStatus) autoFilterStatus.textContent = 'Desligada';
            if (autoFilterToggle) {
                autoFilterToggle.classList.remove('btn-info', 'text-white');
                autoFilterToggle.classList.add('btn-outline-info');
            }
            document.body.classList.remove('auto-search-active');
            removeAutoFilter();
        }
    }

    /**
     * Configura o auto filtro em tempo real
     */
    function setupAutoFilter() {
        if (!filterForm) return;

        const inputs = filterForm.querySelectorAll('input, select');
        inputs.forEach(input => {
            if (input.type === 'submit') return;
            
            const eventType = input.type === 'text' ? 'input' : 'change';
            input.addEventListener(eventType, debounce(autoSubmitForm, 500));
        });
    }

    /**
     * Remove os listeners do auto filtro
     */
    function removeAutoFilter() {
        if (!filterForm) return;

        const inputs = filterForm.querySelectorAll('input, select');
        inputs.forEach(input => {
            if (input.type === 'submit') return;
            input.removeEventListener('input', autoSubmitForm);
            input.removeEventListener('change', autoSubmitForm);
        });
    }

    /**
     * Submete o formulário automaticamente
     */
    function autoSubmitForm() {
        if (autoFilterEnabled && filterForm) {
            showLoading();
            filterForm.submit();
        }
    }

    /**
     * Limpa o campo de busca
     */
    function clearSearch() {
        if (searchInput) {
            searchInput.value = '';
            if (autoFilterEnabled) {
                autoSubmitForm();
            }
        }
    }

    /**
     * Alterna entre visualização em tabela e cards
     */
    function switchView(view) {
        currentView = view;
        localStorage.setItem('competitionsView', view);
        
        if (view === 'table' && tableView && cardView) {
            tableView.classList.remove('d-none');
            cardView.classList.add('d-none');
            
            if (viewToggle) {
                viewToggle.classList.remove('btn-light');
                viewToggle.classList.add('btn-outline-light');
            }
            if (cardViewToggle) {
                cardViewToggle.classList.remove('btn-outline-light');
                cardViewToggle.classList.add('btn-light');
            }
        } else if (view === 'cards' && tableView && cardView) {
            tableView.classList.add('d-none');
            cardView.classList.remove('d-none');
            
            if (viewToggle) {
                viewToggle.classList.remove('btn-outline-light');
                viewToggle.classList.add('btn-light');
            }
            if (cardViewToggle) {
                cardViewToggle.classList.remove('btn-light');
                cardViewToggle.classList.add('btn-outline-light');
            }
        }
    }

    /**
     * Configura atalhos de teclado
     */
    function setupKeyboardShortcuts() {
        document.addEventListener('keydown', function(e) {
            // "/" para focar no campo de busca
            if (e.key === '/' && !e.ctrlKey && !e.metaKey && !e.altKey) {
                e.preventDefault();
                if (searchInput) {
                    searchInput.focus();
                }
            }

            // ESC para limpar busca
            if (e.key === 'Escape' && document.activeElement === searchInput) {
                clearSearch();
                searchInput.blur();
            }

            // Ctrl+F para focar na busca
            if (e.ctrlKey && e.key === 'f') {
                e.preventDefault();
                if (searchInput) {
                    searchInput.focus();
                    searchInput.select();
                }
            }

            // F3 para alternar entre visualizações
            if (e.key === 'F3') {
                e.preventDefault();
                const newView = currentView === 'table' ? 'cards' : 'table';
                switchView(newView);
            }
        });
    }

    /**
     * Mostra indicador de carregamento
     */
    function showLoading() {
        document.body.classList.add('loading');
        
        // Remove o loading após um timeout para evitar que fique preso
        setTimeout(() => {
            hideLoading();
        }, 5000);
    }

    /**
     * Esconde indicador de carregamento
     */
    function hideLoading() {
        document.body.classList.remove('loading');
    }

    /**
     * Função de debounce para otimizar performance
     */
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Interceptar submissão do formulário para mostrar loading
    if (filterForm) {
        filterForm.addEventListener('submit', function() {
            showLoading();
        });
    }

    // Esconder loading quando a página carregar
    window.addEventListener('load', hideLoading);

    // Inicializar tooltips
    try {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[title]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            }
        });
    } catch (error) {
        console.warn('Bootstrap Tooltip não está disponível:', error);
    }

    console.log('✅ Sistema de filtros avançados inicializado com sucesso!');
    console.log('💡 Dicas:');
    console.log('   - Pressione "/" para focar na busca');
    console.log('   - Pressione "ESC" para limpar a busca');
    console.log('   - Pressione "F3" para alternar visualizações');
    console.log('   - Pressione "Ctrl+F" para focar e selecionar a busca');
});

/**
 * Funções utilitárias globais
 */
window.CompetitionFilters = {
    /**
     * Limpa todos os filtros
     */
    clearAllFilters: function() {
        const form = document.getElementById('filterForm');
        if (form) {
            const inputs = form.querySelectorAll('input, select');
            inputs.forEach(input => {
                if (input.type !== 'submit') {
                    input.value = '';
                }
            });
            
            // Submeter se auto filtro estiver ativo
            const autoFilterEnabled = localStorage.getItem('autoFilterEnabled') === 'true';
            if (autoFilterEnabled) {
                form.submit();
            }
        }
    },

    /**
     * Exporta os dados filtrados
     */
    exportFiltered: function() {
        // TODO: Implementar funcionalidade de exportação
        console.log('Exportando dados filtrados...');
    },

    /**
     * Imprime os dados filtrados
     */
    printFiltered: function() {
        window.print();
    }
};
