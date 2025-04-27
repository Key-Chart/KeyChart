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

document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.querySelector('input[type="text"]');
    const selectCompeticao = document.querySelector('select');
    const inputData = document.querySelector('input[type="date"]');
    const btnBuscar = document.querySelectorAll('button.btn-secondary')[1];
    const btnLimpar = document.querySelectorAll('button.btn-secondary')[0];
    const linhasPartidas = document.querySelectorAll("tbody tr");

    function normalizarTexto(texto) {
        return texto.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    }

    function aplicarFiltro() {
        const termoBusca = normalizarTexto(searchInput.value.trim());
        const competenciaSelecionada = selectCompeticao.value;
        const dataSelecionada = inputData.value;

        linhasPartidas.forEach(tr => {
            const textoCompleto = tr.innerText;
            const textoNormalizado = normalizarTexto(textoCompleto);

            const dataPartida = tr.children[0].textContent.trim().split('\n')[0].split("/").reverse().join("-");
            const competenciaMatch = competenciaSelecionada === "Todas as competições" || textoNormalizado.includes(normalizarTexto(competenciaSelecionada));
            const textoMatch = textoNormalizado.includes(termoBusca);
            const dataMatch = !dataSelecionada || dataSelecionada === dataPartida;

            if (competenciaMatch && textoMatch && dataMatch) {
                tr.style.display = "";
            } else {
                tr.style.display = "none";
            }
        });
    }

    function limparFiltros() {
        searchInput.value = "";
        selectCompeticao.selectedIndex = 0;
        inputData.value = "";
        aplicarFiltro();
    }

    btnBuscar.addEventListener("click", aplicarFiltro);
    btnLimpar.addEventListener("click", limparFiltros);

    // Filtro automático ao digitar
    searchInput.addEventListener("input", aplicarFiltro);
    selectCompeticao.addEventListener("change", aplicarFiltro);
    inputData.addEventListener("change", aplicarFiltro);
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