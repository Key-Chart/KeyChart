// Função para calcular o total de uma linha
function calcularTotal(row) {
    let notas = row.querySelectorAll('.nota');
    let total = 0;
    let count = 0;
    
    notas.forEach(input => {
        if (input.value && !isNaN(parseFloat(input.value))) {
            total += parseFloat(input.value);
            count++;
        }
    });
    
    // Calcula a média se houver notas válidas
    let resultado = count > 0 ? (total / count).toFixed(1) : '0.0';
    row.querySelector('.total').textContent = resultado;
    return resultado;
}

// Adiciona eventos para calcular quando uma nota é alterada (mas não salva)
document.querySelector('#kataTable').addEventListener('change', function(e) {
    if (e.target.classList.contains('nota')) {
        calcularTotal(e.target.closest('tr'));
    }
});

// Salvar os dados via AJAX
document.querySelector('#kataTable').addEventListener('click', function(e) {
    if (e.target.classList.contains('btn-salvar') || e.target.closest('.btn-salvar')) {
        const btn = e.target.classList.contains('btn-salvar') ? e.target : e.target.closest('.btn-salvar');
        const row = btn.closest('tr');
        const atletaId = row.getAttribute('data-atleta-id');
        
        // Coletar dados
        const data = {
            'id': atletaId,
            'nota1': row.querySelector('[name="nota1"]').value,
            'nota2': row.querySelector('[name="nota2"]').value,
            'nota3': row.querySelector('[name="nota3"]').value,
            'nota4': row.querySelector('[name="nota4"]').value,
            'nota5': row.querySelector('[name="nota5"]').value,
            'nota6': row.querySelector('[name="nota6"]').value,
            'total': calcularTotal(row)
        };
        
        // Enviar para o backend (substitua pela sua URL)
        fetch('/api/kata/salvar/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify(data)
        })

        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('Dados salvos com sucesso!', 'success');
            } else {
                showAlert('Erro ao salvar: ' + data.error, 'danger');
            }
        })
        .catch(error => {
            showAlert('Erro na conexão: ' + error, 'danger');
        });
    }
    
    // Remover atleta
    if (e.target.classList.contains('btn-remover') || e.target.closest('.btn-remover')) {
        if (confirm('Tem certeza que deseja remover este atleta?')) {
            const btn = e.target.classList.contains('btn-remover') ? e.target : e.target.closest('.btn-remover');
            const row = btn.closest('tr');
            const atletaId = row.getAttribute('data-atleta-id');
            
            // Enviar requisição para remover
            fetch(`/api/kata/remover/${atletaId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    row.remove();
                    showAlert('Atleta removido com sucesso!', 'success');
                } else {
                    showAlert('Erro ao remover: ' + data.error, 'danger');
                }
            });
        }
    }
});

// Adicionar novo atleta
document.getElementById('addAtleta').addEventListener('click', function() {
    fetch('/api/kata/novo/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const tbody = document.querySelector('#kataTable tbody');
            const newRow = document.createElement('tr');
            newRow.setAttribute('data-atleta-id', data.id);
            
            newRow.innerHTML = `
                <td>${data.nome}</td>
                <td><input type="number" class="form-control nota" name="nota1" min="0" max="10" step="0.1"></td>
                <td><input type="number" class="form-control nota" name="nota2" min="0" max="10" step="0.1"></td>
                <td><input type="number" class="form-control nota" name="nota3" min="0" max="10" step="0.1"></td>
                <td><input type="number" class="form-control nota" name="nota4" min="0" max="10" step="0.1"></td>
                <td><input type="number" class="form-control nota" name="nota5" min="0" max="10" step="0.1"></td>
                <td><input type="number" class="form-control nota" name="nota6" min="0" max="10" step="0.1"></td>
                <td class="total">0.0</td>
                <td>
                    <button class="btn btn-sm btn-success btn-salvar">
                        <i class="bi bi-save"></i> Salvar
                    </button>
                    <button class="btn btn-sm btn-danger btn-remover ms-1">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            `;
            
            tbody.appendChild(newRow);
            showAlert('Novo atleta adicionado!', 'success');
        } else {
            showAlert('Erro ao adicionar atleta: ' + data.error, 'danger');
        }
    });
});

// Função para mostrar alertas
function showAlert(message, type) {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.role = 'alert';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const header = document.querySelector('.header');
    header.insertAdjacentElement('afterend', alert);
    
    setTimeout(() => {
        alert.classList.remove('show');
        setTimeout(() => alert.remove(), 150);
    }, 3000);
}