// Função de scroll suave
function scrollTo(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

// Máscara de telefone
function formatPhone(phone) {
    phone = phone.replace(/\D/g, '');
    phone = phone.replace(/(\d{2})(\d)/, '($1) $2');
    phone = phone.replace(/(\d{5})(\d)/, '$1-$2');
    return phone;
}

// Validar email
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Manipular formulário
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

    if (!formData.name || formData.name.length < 3) {
        showError('nameError', 'Nome deve ter pelo menos 3 caracteres');
        isValid = false;
    } else {
        hideError('nameError');
    }

    if (!isValidEmail(formData.email)) {
        showError('emailError', 'Email inválido');
        isValid = false;
    } else {
        hideError('emailError');
    }

    if (!formData.phone || formData.phone.length < 14) {
        showError('phoneError', 'Telefone inválido');
        isValid = false;
    } else {
        hideError('phoneError');
    }

    if (!formData.insuranceType) {
        showError('insuranceTypeError', 'Selecione um tipo de seguro');
        isValid = false;
    } else {
        hideError('insuranceTypeError');
    }

    if (!isValid) return;

    // Enviar dados
    try {
        const response = await fetch('/api/contact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('successMessage').style.display = 'block';
            form.reset();
            
            // Scroll para mensagem de sucesso
            setTimeout(() => {
                document.getElementById('successMessage').scrollIntoView({ behavior: 'smooth' });
            }, 100);
        } else {
            document.getElementById('errorMessage').textContent = '❌ ' + (data.message || 'Erro ao enviar formulário');
            document.getElementById('errorMessage').style.display = 'block';
        }
    } catch (error) {
        console.error('Erro:', error);
        document.getElementById('errorMessage').textContent = '❌ Erro ao conectar ao servidor';
        document.getElementById('errorMessage').style.display = 'block';
    }
});

// Funções de validação
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

// Animações ao scroll
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