from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import os
from config import config
from dotenv import load_dotenv

load_dotenv()

# Inicializar Flask
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

# Carregar configuração
app.config.from_object(config[os.getenv('FLASK_ENV', 'development')])

# Inicializar Mail
mail = Mail(app)

print("✅ Flask app inicializado com sucesso!")
print(f"📧 Email: {app.config.get('MAIL_USERNAME')}")
print(f"🔧 Debug: {app.debug}")

# ==================== ROTAS ====================

# Rota: Página Principal
@app.route('/')
def index():
    """Renderizar landing page"""
    print("📄 Acessando home page...")
    return render_template('index.html')

# Rota: Receber Formulário
@app.route('/api/contact', methods=['POST'])
def contact():
    """Processar formulário de cotação"""
    try:
        data = request.get_json()
        
        print(f"📨 Formulário recebido:")
        print(f"   Nome: {data.get('name')}")
        print(f"   Email: {data.get('email')}")
        print(f"   Telefone: {data.get('phone')}")
        print(f"   Tipo: {data.get('insuranceType')}")
        
        # Validar dados
        if not all([data.get('name'), data.get('email'), data.get('phone'), data.get('insuranceType')]):
            print("❌ Dados incompletos")
            return jsonify({'success': False, 'message': 'Dados incompletos'}), 400
        
        # Email para a corretora
        print("📤 Enviando email para corretora...")
        msg_corretora = Message(
            subject=f"Nova Cotação de Seguro - {data['insuranceType']}",
            recipients=['corretoradesegurostransparenci@gmail.com'],
            html=f"""
                <h2>Nova Solicitação de Cotação</h2>
                <p><strong>Nome:</strong> {data['name']}</p>
                <p><strong>Email:</strong> {data['email']}</p>
                <p><strong>Telefone:</strong> {data['phone']}</p>
                <p><strong>Tipo de Seguro:</strong> {data['insuranceType']}</p>
                <p><strong>Mensagem:</strong> {data.get('message', 'Sem observações')}</p>
            """
        )
        mail.send(msg_corretora)
        print("✅ Email enviado para corretora!")
        
        # Email de confirmação para o cliente
        print("📤 Enviando confirmação para cliente...")
        msg_cliente = Message(
            subject='Cotação Recebida - Transparência Seguros ✅',
            recipients=[data['email']],
            html=f"""
                <h2>Recebemos sua solicitação!</h2>
                <p>Olá <strong>{data['name']}</strong>,</p>
                <p>Recebemos sua solicitação de cotação para <strong>{data['insuranceType']}</strong>.</p>
                <p>Nossa equipe entrará em contato em breve através do WhatsApp: <strong>(69) 98449-7856</strong></p>
                <hr>
                <p>Abraços,<br><strong>Transparência Corretora de Seguros</strong></p>
            """
        )
        mail.send(msg_cliente)
        print("✅ Confirmação enviada para cliente!")
        
        return jsonify({
            'success': True, 
            'message': 'Cotação enviada com sucesso!'
        }), 200
    
    except Exception as e:
        print(f"❌ ERRO: {str(e)}")
        return jsonify({
            'success': False, 
            'message': f'Erro ao enviar cotação: {str(e)}'
        }), 500

# Rota: Teste de Email (apenas desenvolvimento)
@app.route('/test-email')
def test_email():
    """Testar envio de email"""
    print("🧪 Testando email...")
    try:
        msg = Message(
            subject='Teste de Email - Transparência Seguros',
            recipients=['corretoradesegurostransparenci@gmail.com'],
            body='Este é um email de teste! ✅'
        )
        mail.send(msg)
        print("✅ Email de teste enviado com sucesso!")
        return '✅ Email de teste enviado com sucesso!', 200
    except Exception as e:
        print(f"❌ Erro ao enviar email: {str(e)}")
        return f'❌ Erro: {str(e)}', 500

# Rota: Teste de Saúde
@app.route('/health')
def health():
    """Verificar se servidor está online"""
    return jsonify({'status': 'OK', 'message': 'Servidor está funcionando!'}), 200

# ==================== TRATAMENTO DE ERROS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Página não encontrada'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erro interno do servidor'}), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 INICIANDO SERVIDOR FLASK")
    print("="*50)
    print("📍 URL: http://127.0.0.1:5000")
    print("📍 Teste: http://127.0.0.1:5000/health")
    print("📧 Email: http://127.0.0.1:5000/test-email")
    print("="*50 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)