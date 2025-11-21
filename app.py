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
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER', 'seu_email_gmail@gmail.com')
# Senha para autenticação SMTP (sua App Password do Gmail)
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD', 'sua_app_password_aqui')
# Remetente padrão para os emails
app.config['MAIL_DEFAULT_SENDER'] = ('Consultora Gabriela', os.getenv('EMAIL_USER', 'seu_email_gmail@gmail.com'))

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
def enviar_contato():
    """
    Rota para receber dados do formulário de contato via AJAX (POST request).
    Envia emails de confirmação para o cliente e notificação para a corretora.
    """
    try:
        # Pega os dados JSON enviados pelo formulário
        dados = request.get_json()
        
        # Extrai e limpa os dados do formulário
        nome = dados.get('name', '').strip()
        email_cliente = dados.get('email', '').strip()
        telefone = dados.get('phone', '').strip()
        tipo_seguro = dados.get('insuranceType', '').strip()
        mensagem = dados.get('message', '').strip()
        
        # ======================================================================
        # VALIDAÇÕES BÁSICAS
        # ======================================================================
        if not nome or not email_cliente or not telefone:
            return jsonify({
                'sucesso': False, 
                'mensagem': 'Por favor, preencha todos os campos obrigatórios (Nome, Email, Telefone).'
            }), 400
        
        if '@' not in email_cliente or '.' not in email_cliente:
            return jsonify({
                'sucesso': False, 
                'mensagem': 'O endereço de e-mail fornecido é inválido.'
            }), 400
        
        # ======================================================================
        # ENVIO DE EMAIL PARA O CLIENTE (confirmação)
        # ======================================================================
        try:
            msg_cliente = Message(
                subject='✅ Sua Cotação foi Recebida - Consultora Gabriela',
                recipients=[email_cliente],  # Envia para o email que o cliente informou
                html=f"""
                <html>
                    <head>
                        <meta charset="utf-8">
                        <style>
                            body {{ font-family: Arial, sans-serif; color: #333; }}
                            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f5f5f5; border-radius: 8px; }}
                            .header {{ background-color: #1e3a8a; color: white; padding: 20px; border-radius: 5px 5px 0 0; text-align: center; }}
                            .content {{ background-color: white; padding: 20px; border-radius: 0 0 5px 5px; }}
                            .dados {{ background-color: #f0f0f0; padding: 15px; border-radius: 5px; margin: 15px 0; }}
                            .dados p {{ margin: 8px 0; }}
                            .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; }}
                            strong {{ color: #1e3a8a; }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <div class="header">
                                <h1>Obrigado pelo seu interesse! 💚</h1>
                            </div>
                            <div class="content">
                                <p>Olá <strong>{nome}</strong>,</p>
                                
                                <p>Recebemos sua solicitação de cotação com sucesso! Em breve nossa equipe entrará em contato com você para apresentar as melhores opções de seguros.</p>
                                
                                <div class="dados">
                                    <h3>📋 Seus Dados:</h3>
                                    <p><strong>Nome:</strong> {nome}</p>
                                    <p><strong>Email:</strong> {email_cliente}</p>
                                    <p><strong>Telefone:</strong> {telefone}</p>
                                    <p><strong>Tipo de Seguro:</strong> {tipo_seguro if tipo_seguro else 'Não especificado'}</p>
                                    {f'<p><strong>Observações:</strong> {mensagem}</p>' if mensagem else ''}
                                </div>
                                
                                <p>Se você tiver dúvidas, pode nos contatar via WhatsApp:</p>
                                <p><strong>📱 (69) 99844-97856</strong></p>
                                
                                <p>Atenciosamente,<br><strong>Consultora Gabriela</strong><br>Transparência Seguros</p>
                            </div>
                            <div class="footer">
                                <p>Este é um email automático. Não responda a este endereço.</p>
                            </div>
                        </div>
                    </body>
                </html>
                """
            )
            mail.send(msg_cliente)
            print(f"✅ Email de confirmação enviado para o cliente: {email_cliente}")
        
        except Exception as e:
            print(f"❌ Erro ao enviar email de confirmação para o cliente ({email_cliente}): {e}")
            # Se o email do cliente falhar, ainda tentamos enviar para a corretora
            # e informamos o cliente sobre o erro no retorno JSON.
            return jsonify({
                'sucesso': False, 
                'mensagem': f'Sua cotação foi recebida, mas houve um erro ao enviar a confirmação para seu e-mail: {str(e)}'
            }), 500
        
        # ======================================================================
        # ENVIO DE EMAIL PARA A CORRETORA (notificação de nova cotação)
        # ======================================================================
        try:
            # Pega o email da corretora do .env (para testes, usa francislley@gmail.com)
            email_corretora = os.getenv('EMAIL_CORRETORA', 'francislley@gmail.com')
            
            msg_corretora = Message(
                subject=f'🔔 Nova Cotação Recebida - {nome}',
                recipients=[email_corretora], # Envia para o email da corretora
                html=f"""
                <html>
                    <head>
                        <meta charset="utf-8">
                        <style>
                            body {{ font-family: Arial, sans-serif; color: #333; }}
                            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f5f5f5; border-radius: 8px; }}
                            .header {{ background-color: #1e3a8a; color: white; padding: 20px; border-radius: 5px 5px 0 0; text-align: center; }}
                            .content {{ background-color: white; padding: 20px; border-radius: 0 0 5px 5px; }}
                            .dados {{ background-color: #f0f0f0; padding: 15px; border-radius: 5px; margin: 15px 0; }}
                            .dados p {{ margin: 8px 0; }}
                            .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; }}
                            strong {{ color: #1e3a8a; }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <div class="header">
                                <h1>Nova Solicitação de Cotação</h1>
                            </div>
                            <div class="content">
                                <p>Uma nova cotação foi recebida pelo site!</p>
                                
                                <div class="dados">
                                    <h3>👤 Dados do Cliente:</h3>
                                    <p><strong>Nome:</strong> {nome}</p>
                                    <p><strong>Email:</strong> {email_cliente}</p>
                                    <p><strong>Telefone:</strong> {telefone}</p>
                                </div>
                                
                                <div class="dados">
                                    <h3>📊 Tipo de Seguro:</h3>
                                    <p><strong>{tipo_seguro if tipo_seguro else 'Não especificado'}</strong></p>
                                </div>
                                
                                {f'<div class="dados"><h3>📝 Observações:</h3><p>{mensagem}</p></div>' if mensagem else ''}
                                
                                <p><strong>Ação sugerida:</strong> Entre em contato com o cliente via WhatsApp ou email para apresentar as opções de seguros.</p>
                            </div>
                            <div class="footer">
                                <p>Este é um email automático do sistema.</p>
                            </div>
                        </div>
                    </body>
                </html>
                """
            )
            mail.send(msg_corretora)
            print(f"✅ Email de notificação enviado para a corretora: {email_corretora}")
        
        except Exception as e:
            print(f"❌ Erro ao enviar email de notificação para a corretora ({email_corretora}): {e}")
            # Este erro não impede o sucesso da requisição para o cliente,
            # pois o cliente já recebeu a confirmação.
        
        # ======================================================================
        # RESPOSTA DE SUCESSO PARA O CLIENTE
        # ======================================================================
        return jsonify({
            'sucesso': True, 
            'mensagem': 'Sua cotação foi enviada com sucesso! Verifique seu e-mail para a confirmação.'
        }), 200
    
    except Exception as e:
        # Captura qualquer outro erro inesperado durante o processamento
        print(f"❌ Erro geral ao processar solicitação de cotação: {e}")
        return jsonify({
            'sucesso': False, 
            'mensagem': f'Ocorreu um erro inesperado ao processar sua solicitação: {str(e)}'
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