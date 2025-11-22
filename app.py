from flask import send_from_directory
from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Inicialização do aplicativo Flask
app = Flask(__name__)

# Configuração da chave secreta para segurança (pode ser usada para sessões, etc.)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-secreta-consultora-gabriela-padrao')

# ==============================================================================
# CONFIGURAÇÃO DE EMAIL COM FLASK-MAIL
# ==============================================================================
# Servidor SMTP do Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# Porta padrão para TLS
app.config['MAIL_PORT'] = 587
# Habilita Transport Layer Security (TLS)
app.config['MAIL_USE_TLS'] = True
# Nome de usuário para autenticação SMTP (seu email Gmail)
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER', 'corretoradesegurostransparenci@gmail.com')
# Senha para autenticação SMTP (sua App Password do Gmail)
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD', 'hwnnuzpiyeanmqhi')
# Remetente padrão para os emails
app.config['MAIL_DEFAULT_SENDER'] = ('Consultora Gabriela', os.getenv('EMAIL_USER', 'corretoradesegurostransparenci@gmail.com'))

# Inicializa o objeto Mail com as configurações do app
mail = Mail(app)

# ==============================================================================
# ROTAS DO APLICATIVO
# ==============================================================================

@app.route('/')
def index():
    """
    Rota principal que renderiza a página inicial (index.html).
    """
    return render_template('index.html')

@app.route('/enviar-contato', methods=['POST'])
@app.route('/enviar-contato', methods=['POST'])
def enviar_contato():
    """
    Recebe dados do formulário e envia emails
    """
    try:
        dados = request.get_json()
        
        # Validar dados
        if not all([dados.get('name'), dados.get('email'), dados.get('phone'), dados.get('insuranceType')]):
            return jsonify({'mensagem': 'Todos os campos obrigatórios devem ser preenchidos'}), 400
        
        # Preparar email para o cliente
        assunto_cliente = f"✅ Cotação recebida - Transparência Corretora"
        corpo_cliente = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h2 style="color: #d4af37;">Olá, {dados.get('name')}! 👋</h2>
                <p>Sua cotação foi <strong>recebida com sucesso!</strong></p>
                <p>Em breve, Gabriela entrará em contato com você para apresentar as melhores opções.</p>
                <hr>
                <p><strong>Seus dados:</strong></p>
                <ul>
                    <li><strong>Email:</strong> {dados.get('email')}</li>
                    <li><strong>Telefone:</strong> {dados.get('phone')}</li>
                    <li><strong>Tipo de Seguro:</strong> {dados.get('insuranceType')}</li>
                </ul>
                <hr>
                <p>Qualquer dúvida, entre em contato via WhatsApp: <strong>(69) 98449-7856</strong></p>
                <p style="color: #999; font-size: 12px;">Transparência Corretora de Seguros © 2025</p>
            </body>
        </html>
        """
        
        # Preparar email para a corretora
        assunto_corretora = f"📋 Nova Cotação - {dados.get('insuranceType')}"
        corpo_corretora = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h2 style="color: #d4af37;">📋 Nova Solicitação de Cotação</h2>
                <p><strong>Nome:</strong> {dados.get('name')}</p>
                <p><strong>Email:</strong> {dados.get('email')}</p>
                <p><strong>Telefone:</strong> {dados.get('phone')}</p>
                <p><strong>Tipo de Seguro:</strong> {dados.get('insuranceType')}</p>
                <p><strong>Mensagem:</strong></p>
                <p>{dados.get('message', 'Sem mensagem adicional')}</p>
                <hr>
                <p style="color: #d4af37;"><strong>⚡ Responda prontamente!</strong></p>
            </body>
        </html>
        """
        
        # Enviar emails
        try:
            # Email para cliente
            msg_cliente = Message(
                subject=assunto_cliente,
                recipients=[dados.get('email')],
                html=corpo_cliente,
                sender=app.config['MAIL_DEFAULT_SENDER']
            )
            mail.send(msg_cliente)
            print(f"✅ Email enviado para cliente: {dados.get('email')}")
            
        except Exception as e:
            print(f"⚠️ Erro ao enviar email para cliente: {str(e)}")
        
        try:
            # Email para corretora
            msg_corretora = Message(
                subject=assunto_corretora,
                recipients=[os.getenv('EMAIL_CORRETORA')],
                html=corpo_corretora,
                sender=app.config['MAIL_DEFAULT_SENDER']
            )
            mail.send(msg_corretora)
            print(f"✅ Email enviado para corretora: {os.getenv('EMAIL_CORRETORA')}")
            
        except Exception as e:
            print(f"⚠️ Erro ao enviar email para corretora: {str(e)}")
        
        # Retornar sucesso mesmo se um email falhar
        return jsonify({
            'mensagem': '✅ Cotação enviada com sucesso! Verifique seu email.',
            'sucesso': True
        }), 200
        
    except Exception as e:
        print(f"❌ Erro geral: {str(e)}")
        return jsonify({
            'mensagem': f'Erro ao processar cotação: {str(e)}',
            'sucesso': False
        }), 500

# ==============================================================================
# TRATAMENTO DE ERROS HTTP
# ==============================================================================

@app.errorhandler(404)
def page_not_found(e):
    """
    Trata erros 404 (Página Não Encontrada) redirecionando para a página inicial.
    """
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """
    Trata erros 500 (Erro Interno do Servidor) retornando uma mensagem JSON.
    """
    return jsonify({
        'sucesso': False, 
        'mensagem': 'Erro interno do servidor. Por favor, tente novamente mais tarde.'
    }), 500

# ==============================================================================
# INICIALIZAÇÃO DO SERVIDOR FLASK
# ==============================================================================

if __name__ == '__main__':
    # Executa o aplicativo Flask.
    # debug=False é crucial para ambientes de produção.
    app.run(debug=False)

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

#@app.route('/sitemap.xml')
#def sitemap():
#    return '''<?xml version="1.0" encoding="UTF-8"?>
#<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
#    <url>
#        <loc>https://corretoradesegurostransparenci.pythonanywhere.com/</loc>
#        <lastmod>2025-11-21</lastmod>
#        <changefreq>weekly</changefreq>
#        <priority>1.0</priority>
#    </url>
#    <url>
#        <loc>https://corretoradesegurostransparenci.pythonanywhere.com/#sobre</loc>
#        <changefreq>monthly</changefreq>
#        <priority>0.8</priority>
#    </url>
#    <url>
#        <loc>https://corretoradesegurostransparenci.pythonanywhere.com/#servicos</loc>
#        <changefreq>monthly</changefreq>
#        <priority>0.8</priority>
#    </url>
#    <url>
#        <loc>https://corretoradesegurostransparenci.pythonanywhere.com/#black-friday</loc>
#        <changefreq>weekly</changefreq>
#        <priority>0.9</priority>
#    </url>
#    <url>
#        <loc>https://corretoradesegurostransparenci.pythonanywhere.com/#contato</loc>
#        <changefreq>monthly</changefreq>
#        <priority>0.8</priority>
#    </url>
#</urlset>''', 200, {'Content-Type': 'application/xml'}