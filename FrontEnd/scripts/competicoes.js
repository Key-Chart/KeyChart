document.addEventListener("DOMContentLoaded", function () {
    // Seleciona os elementos de entrada dos filtros
    const searchInput = document.querySelector(".input-group input");
    const statusFilter = document.querySelector(".form-select");
    const dateFilter = document.querySelector(".form-control[type='date']");
    const tableRows = document.querySelectorAll("tbody tr");

    // Função para filtrar a tabela com base nos inputs
    function filterTable() {
        // Obtem os valores dos filtros
        const searchText = searchInput?.value.toLowerCase() || "";
        const selectedStatus = statusFilter?.value.toLowerCase().trim() || "";
        const selectedDate = dateFilter?.value || "";

        tableRows.forEach(row => {
            // Verifica se os elementos necessários existem na linha
            const nameElement = row.querySelector("td a");
            const statusElement = row.querySelector("td span");
            const dateCell = row.cells[1];

            if (!nameElement || !statusElement || !dateCell) {
                row.style.display = "none";
                return;
            }

            const name = nameElement.textContent.toLowerCase();
            const status = statusElement.textContent.toLowerCase().trim();
            const date = dateCell.textContent.trim().split("/").reverse().join("-");

            // Verifica se a linha corresponde aos filtros
            const matchesSearch = name.includes(searchText);
            const matchesStatus = selectedStatus === "todos os status" || status === selectedStatus;
            const matchesDate = !selectedDate || date === selectedDate;

            // Exibe ou oculta a linha com base nos filtros
            row.style.display = (matchesSearch && matchesStatus && matchesDate) ? "" : "none";
        });
    }

    // Adiciona os ouvintes de eventos aos filtros
    if (searchInput) searchInput.addEventListener("input", filterTable);
    if (statusFilter) statusFilter.addEventListener("change", filterTable);
    if (dateFilter) dateFilter.addEventListener("change", filterTable);
});

document.addEventListener("DOMContentLoaded", function () {
    //Seleciona o formulário e os campos de entrada
    const form = document.getElementById("createCompetitionForm");
    const nameInput = document.getElementById("createName");
    const modalitySelect = document.getElementById("createModality");
    const dateInput = document.getElementById("createDate");
    const timeInput = document.getElementById("createTime");
    const locationInput = document.getElementById("createLocation");
    const categories = document.querySelectorAll("input[type='checkbox']");
    const rulesTextarea = document.getElementById("createRules");
    const statusSelect = document.getElementById("createStatus");

    function showError(input, isValid, message){
        let errorElement = input.nextElementSibling;

        // Se existe erro
        if (errorElement && errorElement.classList.contains("error-message")) {
            if (isValid) {
                errorElement.remove();
            } else {
                errorElement.textContent = message;
            }
        } else if (!isValid) {
            errorElement = document.createElement("div");
            errorElement.className = "error-message alert alert-danger";
            errorElement.textContent = message;
            input.parentNode.appendChild(errorElement);
        }
    }

    function validateForm() {
        let isValid = true;

        // Validar Nome da Competição
        if (nameInput.value.trim() === "") {
            showError(nameInput, false, "O nome da competição é obrigatório.");
            isValid = false;
        } else {
            showError(nameInput, true);
        }

        // Validar Modalidade
        if (modalitySelect.value === "") {
            showError(modalitySelect, false, "Selecione uma modalidade.");
            isValid = false;
        } else {
            showError(modalitySelect, true);
        }

        // Validar Data
        const today = new Date().toISOString().split("T")[0];
        if (dateInput.value === "") {
            showError(dateInput, false, "A data de início é obrigatória.");
            isValid = false;
        } else if (dateInput.value < today) {
            showError(dateInput, false, "A data de início deve ser a partir de hoje.");
            isValid = false;
        } else {
            showError(dateInput, true);
        }

        // Validar Horário
        if (timeInput.value === "") {
            showError(timeInput, false, "O horário da competição é obrigatório.");
            isValid = false;
        } else {
            showError(timeInput, true);
        }

        // Validar Local
        let locationError = document.querySelector(".location-error");
        if (locationInput.value.trim() === "") {
            if (!locationError) { // Só exibe se ainda não existir a mensagem de erro
                let errorMessage = document.createElement("div");
                errorMessage.className = "error-message location-error alert alert-danger";
                errorMessage.textContent = "O local da competição deve ser obrigatório.";
                locationInput.parentNode.appendChild(errorMessage);
            }
            isValid = false;
        } else {
            if (locationError) {
                locationError.remove(); // Remove a mensagem caso o campo seja preenchido
            }
        }

        // Validar Categoria
        let categorySelected = Array.from(categories).some(checkbox => checkbox.checked);
        let categoryError = document.querySelector(".category-error");

        if (!categorySelected) {
            if (!categoryError) { // Só exibe se ainda não existir a mensagem de erro
                let errorMessage = document.createElement("div");
                errorMessage.className = "error-message category-error alert alert-danger";
                errorMessage.textContent = "Selecione pelo menos uma categoria.";
                categories[0].parentNode.appendChild(errorMessage);
            }
            isValid = false;
        } else {
            if (categoryError) {
                categoryError.remove(); // Remove a mensagem caso já tenha sido exibida
            }
        }

        // Validar Regras
        if (rulesTextarea.value.trim() === "") {
            showError(rulesTextarea, false, "Descreva as regras.");
            isValid = false;
        } else {
            showError(rulesTextarea, true);
        }

        // Validar Status
        if (statusSelect.value === "") {
            showError(statusSelect, false, "Selecione um status");
            isValid = false;
        } else {
            showError(statusSelect, true);
        }

        return isValid;
    }

    function createCompetition() {
        if (validateForm()) {
            alert("Competição criada com sucesso!");
            form.reset();
        }
    }

    document.querySelector(".btn-success").addEventListener("click", createCompetition);
});
