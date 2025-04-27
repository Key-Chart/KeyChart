document.addEventListener("DOMContentLoaded", function () {
    // Elementos do DOM
    const searchInput = document.querySelector('input[placeholder="Buscar atleta..."]');
    const searchButton = document.querySelector('.btn.btn-primary');
    const citySelect = document.querySelectorAll("select")[0];
    const stateSelect = document.querySelectorAll("select")[1];
    const athleteCards = document.querySelectorAll(".athlete-card");

    // Função para obter valores dos cards
    function getCardValue(card, label) {
        const labels = card.querySelectorAll(".info-label");
        for (let i = 0; i < labels.length; i++) {
            if (labels[i].textContent.trim().toUpperCase() === label.toUpperCase()) {
                const valueElement = labels[i].nextElementSibling;
                return valueElement ? valueElement.textContent.trim().toLowerCase() : "";
            }
        }
        return "";
    }

    // Função principal de filtragem
    function filterAthletes() {
        const searchTerm = searchInput?.value.toLowerCase() || "";
        const selectedCity = citySelect?.value.toLowerCase() || "";
        const selectedState = stateSelect?.value.toLowerCase() || "";

        athleteCards.forEach(function (card) {
            // Verifica se os elementos necessários existem
            const nameElement = card.querySelector(".card-title");
            const idElement = card.querySelector(".text-muted");

            if (!nameElement || !idElement) {
                card.style.display = "none";
                return;
            }

            const name = nameElement.textContent.toLowerCase();
            const city = getCardValue(card, "CIDADE");
            const state = getCardValue(card, "ESTADO");
            const academy = getCardValue(card, "ACADEMIA");
            const id = idElement.textContent.toLowerCase();

            // Verifica se o atleta corresponde aos critérios de busca
            const matchesSearch = name.includes(searchTerm) ||
                                  id.includes(searchTerm) ||
                                  academy.includes(searchTerm);

            // Verifica os filtros de cidade e estado
            const matchesCity = selectedCity === "filtrar por cidade" || city === selectedCity;
            const matchesState = selectedState === "filtrar por estado" || state === selectedState;

            // Mostra ou esconde o card com base nos filtros
            card.style.display = (matchesSearch && matchesCity && matchesState) ? "block" : "none";
        });
    }

    // Adiciona os ouvintes de eventos aos filtros, se os elementos existirem
    if (searchInput) searchInput.addEventListener("input", filterAthletes);
    if (searchButton) searchButton.addEventListener("click", filterAthletes);
    if (citySelect) citySelect.addEventListener("change", filterAthletes);
    if (stateSelect) stateSelect.addEventListener("change", filterAthletes);

    // Filtro inicial para mostrar todos os atletas
    filterAthletes();
});

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');
    sidebar.classList.toggle('collapsed');
    content.classList.toggle('collapsed');
}