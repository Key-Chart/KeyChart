// Função para alternar a visibilidade da sidebar (expandir/recolher)
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');
    sidebar.classList.toggle('sidebar-hidden');
    content.classList.toggle('content-expanded');
}

