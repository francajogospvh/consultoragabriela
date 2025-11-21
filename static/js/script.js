// ==================== SCROLL SUAVE ====================
function scrollTo(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

// ==================== MÁSCARA DE TELEFONE ====================
function formatPhone(phone) {
    phone = phone.replace(/\D/g, '');
    phone = phone.replace(/(\d{2})(\d)/, '($1) $2');
    phone = phone.replace(/(\d{5})(\d)/, '$1-$2');
    return phone;
}

// ==================== VALIDAR EMAIL ====================
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// ==================== MANIPULAR FORMULÁRIO ====================
const form = document.getElementById('contactForm');
const phoneInput = document.getElementById('phone');

// Formatar telefone enquanto digita
phoneInput?.addEventListener('input', (e) => {
    e.target.value = formatPhone(e.target.value);
});

// Enviar formulário
form?.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Limpar mensagens anteriores
    document.getElementById('successMessage').style.display = 'none';
    document.getElementById('errorMessage').style.display = 'none';
    
    // Coletar dados
    const formData = {
        name: document.getElementById('name').value.trim(),
        email: document.getElementById('email').value.trim(),
        phone: document.getElementById('phone').value.trim(),
        insuranceType: document.getElementById('insuranceType').value,
        message: document.getElementById('message').value.trim()
    };

    // Validar dados
    let isValid = true;

    // Validar Nome
    if (!formData.name || formData.name.length < 3) {
        showError('nameError', 'Nome deve ter pelo menos 3 caracteres');
        isValid = false;
    } else {
        hideError('nameError');
    }

    // Validar Email
    if (!isValidEmail(formData.email)) {
        showError('emailError', 'Email inválido');
        isValid = false;
    } else {
        hideError('emailError');
    }

    // Validar Telefone
    if (!formData.phone || formData.phone.length < 14) {
        showError('phoneError', 'Telefone inválido');
        isValid = false;
    } else {
        hideError('phoneError');
    }

    // Validar Tipo de Seguro
    if (!formData.insuranceType) {
        showError('insuranceTypeError', 'Selecione um tipo de seguro');
        isValid = false;
    } else {
        hideError('insuranceTypeError');
    }

    if (!isValid) return;

    // ==================== ENVIAR DADOS PARA FLASK ====================
    try {
        // Desabilitar botão enquanto envia
        const submitButton = form.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        submitButton.textContent = 'Enviando...';

        // Enviar para a rota /enviar-contato do Flask
        const response = await fetch('/enviar-contato', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        // Re-habilitar botão
        submitButton.disabled = false;
        submitButton.textContent = 'Solicitar Atendimento Agora 📍';

        if (response.ok) {
            // ✅ Sucesso!
            document.getElementById('successMessage').textContent = 
                '✅ ' + (data.mensagem || 'Cotação enviada com sucesso! Verifique seu email.');
            document.getElementById('successMessage').style.display = 'block';
            
            // Limpar formulário
            form.reset();
            
            // Scroll para mensagem de sucesso
            setTimeout(() => {
                document.getElementById('successMessage').scrollIntoView({ behavior: 'smooth' });
            }, 300);

            // Esconder mensagem de sucesso após 5 segundos
            setTimeout(() => {
                document.getElementById('successMessage').style.display = 'none';
            }, 5000);
        } else {
            // ❌ Erro do servidor
            document.getElementById('errorMessage').textContent = 
                '❌ ' + (data.mensagem || 'Erro ao enviar cotação');
            document.getElementById('errorMessage').style.display = 'block';
            document.getElementById('errorMessage').style.color = '#d32f2f';
        }
    } catch (error) {
        console.error('Erro ao enviar:', error);
        
        // Re-habilitar botão em caso de erro
        const submitButton = form.querySelector('button[type="submit"]');
        submitButton.disabled = false;
        submitButton.textContent = 'Solicitar Atendimento Agora 📍';

        document.getElementById('errorMessage').textContent = 
            '❌ Erro ao conectar ao servidor. Tente novamente ou entre em contato via WhatsApp.';
        document.getElementById('errorMessage').style.display = 'block';
        document.getElementById('errorMessage').style.color = '#d32f2f';
    }
});

// ==================== FUNÇÕES DE VALIDAÇÃO ====================
function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = message;
        element.classList.add('show');
    }
}

function hideError(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = '';
        element.classList.remove('show');
    }
}

// ==================== ANIMAÇÕES AO SCROLL ====================
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.card-servico, .diferencial, .destaque').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s, transform 0.6s';
    observer.observe(el);
});

// ==================== FECHAR MENSAGENS AO CLICAR FORA ====================
document.addEventListener('click', (e) => {
    const successMsg = document.getElementById('successMessage');
    const errorMsg = document.getElementById('errorMessage');
    
    if (successMsg && e.target === successMsg) {
        successMsg.style.display = 'none';
    }
    
    if (errorMsg && e.target === errorMsg) {
        errorMsg.style.display = 'none';
    }
});

// ==================== FECHAR MENSAGENS COM ESC ====================
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.getElementById('successMessage').style.display = 'none';
        document.getElementById('errorMessage').style.display = 'none';
    }
});