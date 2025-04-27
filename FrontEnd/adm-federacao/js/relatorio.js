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

// Event listener para o botão toggle
document.getElementById('toggleSidebar').addEventListener('click', toggleSidebar);

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