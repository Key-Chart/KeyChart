
// Fechar sidebar ao clicar no conteúdo (mobile)
document.getElementById('content').addEventListener('click', function() {
    if (window.innerWidth <= 992) {
        document.getElementById('sidebar').classList.remove('show');
    }
});

// Atualizar ao redimensionar
window.addEventListener('resize', function() {
    if (window.innerWidth > 992) {
        document.getElementById('sidebar').style.width = '260px';
        document.getElementById('content').style.marginLeft = '260px';
        document.querySelectorAll('.sidebar a span').forEach(el => {
            el.style.display = 'inline';
        });
        document.querySelector('.sidebar .small').style.display = 'block';
    }
});

// Funções para manipulação dos formulários
/*document.getElementById('categoryForm').addEventListener('submit', function(e) {
    e.preventDefault();
    // Lógica para cadastrar categoria
    alert('Categoria cadastrada com sucesso!');
    this.reset();
});*/

document.getElementById('academyForm').addEventListener('submit', function(e) {
    e.preventDefault();
    // Lógica para cadastrar academia
    alert('Academia cadastrada com sucesso!');
    this.reset();
});

// Inicializar tooltips
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-mdb-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new mdb.Tooltip(tooltipTriggerEl);
    });
});

