// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Configura o input de foto
    document.getElementById('foto').addEventListener('change', function(e) {
        if (e.target.files && e.target.files[0]) {
            const file = e.target.files[0];
            
            // Verifica o tamanho do arquivo (max 2MB)
            if (file.size > 2 * 1024 * 1024) {
                alert('O arquivo é muito grande. Por favor, selecione uma imagem menor que 2MB.');
                e.target.value = '';
                return;
            }
            
            // Mostra preview da foto
            const reader = new FileReader();
            reader.onload = function(event) {
                const preview = document.getElementById('foto-preview');
                preview.src = event.target.result;
                preview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });
    
    // Configura os métodos de pagamento
    document.querySelectorAll('input[name="metodo-pagamento"]').forEach(radio => {
        radio.addEventListener('change', function() {
            document.getElementById('pix-section').classList.add('d-none');
            document.getElementById('cartao-section').classList.add('d-none');
            document.getElementById('boleto-section').classList.add('d-none');
            
            if (this.value === 'pix') {
                document.getElementById('pix-section').classList.remove('d-none');
            } else if (this.value === 'cartao') {
                document.getElementById('cartao-section').classList.remove('d-none');
            } else if (this.value === 'boleto') {
                document.getElementById('boleto-section').classList.remove('d-none');
            }
        });
    });
    
    // Botão para copiar código PIX
    document.getElementById('copy-pix').addEventListener('click', function() {
        const pixCode = document.getElementById('pix-code');
        pixCode.select();
        document.execCommand('copy');
        
        // Feedback visual
        const originalText = this.innerHTML;
        this.innerHTML = '<i class="bi bi-check"></i> Copiado!';
        setTimeout(() => {
            this.innerHTML = originalText;
        }, 2000);
    });

    // Botão para aceitar termos
    document.getElementById('acceptTerms').addEventListener('click', function() {
        document.getElementById('termos').checked = true;
    });

    // Máscaras para campos
    document.getElementById('cpf').addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length > 3) value = value.replace(/^(\d{3})(\d)/, '$1.$2');
        if (value.length > 6) value = value.replace(/^(\d{3})\.(\d{3})(\d)/, '$1.$2.$3');
        if (value.length > 9) value = value.replace(/^(\d{3})\.(\d{3})\.(\d{3})(\d)/, '$1.$2.$3-$4');
        e.target.value = value.substring(0, 14);
    });

    document.getElementById('telefone').addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length > 0) value = '(' + value;
        if (value.length > 3) value = value.replace(/^(\d{2})(\d)/, '$1) $2');
        if (value.length > 10) value = value.replace(/(\d{5})(\d)/, '$1-$2');
        e.target.value = value.substring(0, 15);
    });
    
    // Inicializa partículas no fundo
    particlesJS('particles-js', {
        "particles": {
            "number": {
                "value": 80,
                "density": {
                    "enable": true,
                    "value_area": 800
                }
            },
            "color": {
                "value": "#f8bb30"
            },
            "shape": {
                "type": "circle",
                "stroke": {
                    "width": 0,
                    "color": "#000000"
                },
                "polygon": {
                    "nb_sides": 5
                }
            },
            "opacity": {
                "value": 0.5,
                "random": false,
                "anim": {
                    "enable": false,
                    "speed": 1,
                    "opacity_min": 0.1,
                    "sync": false
                }
            },
            "size": {
                "value": 3,
                "random": true,
                "anim": {
                    "enable": false,
                    "speed": 40,
                    "size_min": 0.1,
                    "sync": false
                }
            },
            "line_linked": {
                "enable": true,
                "distance": 150,
                "color": "#f8bb30",
                "opacity": 0.4,
                "width": 1
            },
            "move": {
                "enable": true,
                "speed": 2,
                "direction": "none",
                "random": false,
                "straight": false,
                "out_mode": "out",
                "bounce": false,
                "attract": {
                    "enable": false,
                    "rotateX": 600,
                    "rotateY": 1200
                }
            }
        },
        "interactivity": {
            "detect_on": "canvas",
            "events": {
                "onhover": {
                    "enable": true,
                    "mode": "grab"
                },
                "onclick": {
                    "enable": true,
                    "mode": "push"
                },
                "resize": true
            },
            "modes": {
                "grab": {
                    "distance": 140,
                    "line_linked": {
                        "opacity": 1
                    }
                },
                "bubble": {
                    "distance": 400,
                    "size": 40,
                    "duration": 2,
                    "opacity": 8,
                    "speed": 3
                },
                "repulse": {
                    "distance": 200,
                    "duration": 0.4
                },
                "push": {
                    "particles_nb": 4
                },
                "remove": {
                    "particles_nb": 2
                }
            }
        },
        "retina_detect": true
    });
});

// Função para avançar para o próximo passo
function nextStep(step) {
    // Valida o formulário atual antes de avançar
    let formValid = true;
    if (step === 1) {
        formValid = validateForm('personal-data-form');
    } else if (step === 2) {
        formValid = validateForm('sports-data-form');
    } else if (step === 3) {
        formValid = validateForm('payment-form');
    }

    if (!formValid) {
        alert('Por favor, preencha todos os campos obrigatórios corretamente.');
        return;
    }

    // Esconde o passo atual
    document.getElementById(`step${step}-content`).classList.add('d-none');
    document.getElementById(`step${step}`).classList.remove('active');
    document.getElementById(`step${step}`).classList.add('completed');

    // Mostra o próximo passo
    currentStep = step + 1;
    document.getElementById(`step${currentStep}-content`).classList.remove('d-none');
    document.getElementById(`step${currentStep}`).classList.add('active');

    // Atualiza conectores
    updateConnectors();

    // Rola para o topo do próximo passo
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Se for o último passo, mostra mensagem de sucesso
    if (currentStep === 4) {
        // Aqui você normalmente enviaria os dados para o servidor
        // Em produção, substitua por uma chamada AJAX real
        setTimeout(() => {
            // Simulação de envio bem-sucedido
            console.log('Inscrição enviada com sucesso!');
        }, 1000);
    }
}

// Função para voltar ao passo anterior
function prevStep(step) {
    // Esconde o passo atual
    document.getElementById(`step${step}-content`).classList.add('d-none');
    document.getElementById(`step${step}`).classList.remove('active');

    // Mostra o passo anterior
    currentStep = step - 1;
    document.getElementById(`step${currentStep}-content`).classList.remove('d-none');
    document.getElementById(`step${currentStep}`).classList.add('active');
    document.getElementById(`step${currentStep}`).classList.remove('completed');

    // Atualiza conectores
    updateConnectors();

    // Rola para o topo do passo anterior
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Função para validar formulário
function validateForm(formId) {
    const form = document.getElementById(formId);
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }

        // Validações específicas
        if (field.id === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(field.value)) {
            field.classList.add('is-invalid');
            isValid = false;
        }

        if (field.id === 'cpf' && field.value.length < 14) {
            field.classList.add('is-invalid');
            isValid = false;
        }

        if (field.id === 'telefone' && field.value.length < 15) {
            field.classList.add('is-invalid');
            isValid = false;
        }
    });

    return isValid;
}

// Função para atualizar os conectores entre os passos
function updateConnectors() {
    const steps = document.querySelectorAll('.step');
    steps.forEach((step, index) => {
        const connector = step.querySelector('.step-connector');
        if (connector) {
            if (index < currentStep - 1) {
                connector.style.backgroundColor = 'var(--accent-color)';
                connector.style.boxShadow = '0 0 5px rgba(217, 4, 41, 0.5)';
            } else {
                connector.style.backgroundColor = '#ddd';
                connector.style.boxShadow = 'none';
            }
        }
    });
}