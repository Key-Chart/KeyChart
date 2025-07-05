// Função para alternar a barra lateral
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');
    
    sidebar.classList.toggle('sidebar-hidden');
    content.classList.toggle('content-expanded');
}

// Visualização da logo antes de upload
document.getElementById('uploadLogo').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            document.getElementById('logoPreview').src = event.target.result;
        };
        reader.readAsDataURL(file);
    }
});

// Seleção de tema de cores
document.querySelectorAll('.theme-color').forEach(color => {
    color.addEventListener('click', function() {
        document.querySelectorAll('.theme-color').forEach(c => c.classList.remove('selected'));
        this.classList.add('selected');
        // Aqui você adicionaria o código para aplicar o tema selecionado
    });
});

// Copiar chave da API
document.getElementById('copiarApiKey').addEventListener('click', function() {
    const apiKey = document.querySelector('input[value^="sk_test"]');
    apiKey.select();
    document.execCommand('copy');
    alert('Chave da API copiada para a área de transferência!');
});

// Script para controlar os modais
document.addEventListener('DOMContentLoaded', function() {
    // Modal de Verificar Atualizações
    const verificarAtualizacoesBtn = document.querySelector('button[data-bs-target="#verificarAtualizacoesModal"]');
    if (verificarAtualizacoesBtn) {
        verificarAtualizacoesBtn.addEventListener('click', function() {
            const modal = new bootstrap.Modal(document.getElementById('verificarAtualizacoesModal'));
            modal.show();
            
            // Simular verificação de atualizações
            setTimeout(function() {
                document.getElementById('atualizacaoStatus').style.display = 'none';
                
                // Simular que há uma atualização disponível (50% de chance)
                if (Math.random() > 0.5) {
                    document.getElementById('atualizacaoDisponivel').style.display = 'block';
                    
                    // Simular download da atualização
                    document.getElementById('btnBaixarAtualizacao').addEventListener('click', function() {
                        this.innerHTML = '<i class="bi bi-arrow-repeat spinner"></i> Baixando...';
                        this.disabled = true;
                        
                        setTimeout(function() {
                            document.getElementById('btnBaixarAtualizacao').innerHTML = '<i class="bi bi-check-circle"></i> Atualização instalada com sucesso!';
                            document.getElementById('btnBaixarAtualizacao').className = 'btn btn-success';
                        }, 3000);
                    });
                } else {
                    document.getElementById('semAtualizacao').style.display = 'block';
                }
            }, 2000);
        });
    }
    
    // Modal de Renovar Licença
    const renovarLicencaBtn = document.querySelector('button[data-bs-target="#renovarLicencaModal"]');
    if (renovarLicencaBtn) {
        renovarLicencaBtn.addEventListener('click', function() {
            
            modal.show();
            
            // Atualizar preço quando selecionar outro tipo de licença
            document.querySelectorAll('input[name="tipoLicenca"]').forEach(radio => {
                radio.addEventListener('change', function() {
                    // Aqui você pode adicionar lógica para atualizar valores
                });
            });
            
            // Simular pagamento
            document.getElementById('btnFinalizarRenovacao').addEventListener('click', function() {
                this.innerHTML = '<i class="bi bi-arrow-repeat spinner"></i> Processando pagamento...';
                this.disabled = true;
                
                setTimeout(function() {
                    const modalInstance = bootstrap.Modal.getInstance(document.getElementById('verificarAtualizacoesModal'));
                    modalInstance.hide();
                    
                    // Mostrar alerta de sucesso
                    const alertDiv = document.createElement('div');
                    alertDiv.className = 'alert alert-success alert-dismissible fade show fixed-top m-3';
                    alertDiv.innerHTML = `
                        <i class="bi bi-check-circle-fill"></i> <strong>Licença renovada com sucesso!</strong> Sua licença agora é válida até 15/11/2024.
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    `;
                    document.body.appendChild(alertDiv);
                    
                    // Atualizar o texto da licença na página
                    const licencaText = document.querySelector('#sobre .card-body p strong:contains("Expira em:")').nextSibling;
                    if (licencaText) {
                        licencaText.textContent = ' 15/11/2024';
                    }
                }, 2000);
            });
        });
    }
});