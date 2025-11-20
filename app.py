from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-secreta-consultora-gabriela')

# ===== CONFIGURAÇÃO DE EMAIL =====
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER', 'francislley@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD', 'vmng byaa zbmw jzqo')
app.config['MAIL_DEFAULT_SENDER'] = ('Consultora Gabriela', os.getenv('EMAIL_USER', 'francislley@gmail.com'))

mail = Mail(app)

# ===== ROTAS =====

@app.route('/')
def index():
    """Renderiza a página principal"""
    return render_template('index.html')

@app.route('/enviar-contato', methods=['POST'])
def enviar_contato():
    """Recebe dados do formulário e envia emails"""
    try:
        dados = request.get_json()
        
        # Validações básicas
        nome = dados.get('name', '').strip()
        email = dados.get('email', '').strip()
        telefone = dados.get('phone', '').strip()
        tipo_seguro = dados.get('insuranceType', '').strip()
        mensagem = dados.get('message', '').strip()
        
        if not nome or not email or not telefone:
            return jsonify({
                'sucesso': False, 
                'mensagem': 'Preencha todos os campos obrigatórios (Nome, Email, Telefone)'
            }), 400
        
        # Validar email básico
        if '@' not in email:
            return jsonify({
                'sucesso': False, 
                'mensagem': 'Email inválido'
            }), 400
        
        # ===== EMAIL PARA O CLIENTE =====
        try:
            msg_cliente = Message(
                subject='✅ Cotação Recebida - Consultora Gabriela',
                recipients=[email],
                html=f"""
                <html>
                    <head>
                        <meta charset="utf-8">
                        <style>
                            body {{ font-family: Arial, sans-serif; color: #333; }}
                            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f5f5f5; }}
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
                                    <p><strong>Email:</strong> {email}</p>
                                    <p><strong>Telefone:</strong> {telefone}</p>
                                    <p><strong>Tipo de Seguro:</strong> {tipo_seguro if tipo_seguro else 'Não especificado'}</p>
                                    {f'<p><strong>Observações:</strong> {mensagem}</p>' if mensagem else ''}
                                </div>
                                
                                <p>Se você tiver dúvidas, pode nos contatar via WhatsApp:</p>
                                <p><strong>📱 (69) 99844-9786</strong></p>
                                
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
            print(f"✅ Email enviado para cliente: {email}")
        
        except Exception as e:
            print(f"❌ Erro ao enviar email para cliente: {e}")
            return jsonify({
                'sucesso': False, 
                'mensagem': f'Erro ao enviar confirmação: {str(e)}'
            }), 500
        
        # ===== EMAIL PARA A CORRETORA =====
        try:
            msg_corretora = Message(
                subject=f'🔔 Nova Cotação Recebida - {nome}',
                recipients=['corretoradesegurostransparenci@gmail.com'],
                html=f"""
                <html>
                    <head>
                        <meta charset="utf-8">
                        <style>
                            body {{ font-family: Arial, sans-serif; color: #333; }}
                            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f5f5f5; }}
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
                                    <p><strong>Email:</strong> {email}</p>
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
            print(f"✅ Email enviado para corretora: corretoradesegurostransparenci@gmail.com")
        
        except Exception as e:
            print(f"❌ Erro ao enviar email para corretora: {e}")
            # Não retorna erro aqui, pois o cliente já recebeu confirmação
        
        # Resposta de sucesso
        return jsonify({
            'sucesso': True, 
            'mensagem': 'Cotação enviada com sucesso! Verifique seu email para confirmação.'
        }), 200
    
    except Exception as e:
        print(f"❌ Erro geral ao processar cotação: {e}")
        return jsonify({
            'sucesso': False, 
            'mensagem': f'Erro ao processar sua solicitação: {str(e)}'
        }), 500

# ===== TRATAMENTO DE ERROS =====

@app.errorhandler(404)
def page_not_found(e):
    """Redireciona erros 404 para a página principal"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """Trata erros internos do servidor"""
    return jsonify({
        'sucesso': False, 
        'mensagem': 'Erro interno do servidor'
    }), 500

# ===== INICIALIZAÇÃO =====

if __name__ == '__main__':
    app.run(debug=False)