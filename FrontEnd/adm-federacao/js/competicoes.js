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