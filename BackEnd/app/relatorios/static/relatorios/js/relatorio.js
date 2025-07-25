// Função para alternar a sidebar
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');
    
    if (window.innerWidth <= 992) {
        // Comportamento mobile
        sidebar.classList.toggle('show');
    } else {
        // Comportamento desktop
        if (sidebar.style.width === '250px') {
            sidebar.style.width = '60px';
            content.style.marginLeft = '60px';
            document.querySelectorAll('.sidebar a span').forEach(el => {
                el.style.display = 'none';
            });
            document.querySelector('.sidebar .small').style.display = 'none';
        } else {
            sidebar.style.width = '250px';
            content.style.marginLeft = '250px';
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
        document.getElementById('sidebar').style.width = '250px';
        document.getElementById('content').style.marginLeft = '250px';
        document.querySelectorAll('.sidebar a span').forEach(el => {
            el.style.display = 'inline';
        });
        document.querySelector('.sidebar .small').style.display = 'block';
    }
});

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