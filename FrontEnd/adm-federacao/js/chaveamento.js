// Função para carregar os chaveamentos via AJAX
function carregarChaveamentos() {
    // Simulando dados do backend - substitua por chamadas reais ao seu backend
    console.log("Carregando chaveamentos...");

    // Aqui você faria chamadas AJAX para buscar os dados reais
    // fetch('/api/chaveamento/kata/')
    //     .then(response => response.json())
    //     .then(data => {
    //         // Processar dados de Kata
    //     });

    // fetch('/api/chaveamento/kumite/')
    //     .then(response => response.json())
    //     .then(data => {
    //         // Processar dados de Kumite
    //     });
}

// Carrega os chaveamentos quando a página é aberta
document.addEventListener('DOMContentLoaded', carregarChaveamentos);
function verCategoria(id) {
    // Implemente a lógica para visualizar a categoria
    console.log("Visualizando categoria ID:", id);
    // Aqui você pode redirecionar para a página de detalhes ou abrir um modal
    // Exemplo: window.location.href = `/categoria/${id}`;

    // Alternativamente, você pode ativar a tab correspondente
    if (id === 1 || id === 2 || id === 5) {
        const kataTab = new bootstrap.Tab(document.getElementById('kata-tab'));
        kataTab.show();
    } else {
        const kumiteTab = new bootstrap.Tab(document.getElementById('kumite-tab'));
        kumiteTab.show();
    }
}

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