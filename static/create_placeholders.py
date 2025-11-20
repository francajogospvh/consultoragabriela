from PIL import Image, ImageDraw, ImageFont
import os

# Criar pasta se não existir
os.makedirs('static/fotos', exist_ok=True)

# Função para criar placeholder
def create_placeholder(filename, width, height, text):
    """Cria uma imagem placeholder"""
    # Cores
    background = (52, 79, 107)  # Azul da marca
    text_color = (212, 175, 55)  # Ouro da marca
    
    # Criar imagem
    img = Image.new('RGB', (width, height), background)
    draw = ImageDraw.Draw(img)
    
    # Desenhar texto
    try:
        # Tentar usar fonte do sistema
        font = ImageFont.truetype("arial.ttf", 30)
    except:
        # Se não encontrar, usar padrão
        font = ImageFont.load_default()
    
    # Centralizar texto
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) / 2
    y = (height - text_height) / 2
    
    draw.text((x, y), text, fill=text_color, font=font)
    
    # Salvar
    img.save(filename)
    print(f"✅ {filename} criada!")

# Criar placeholders se as imagens não existirem
placeholders = [
    ('static/fotos/IMG_5600.jpg', 400, 500, 'Gabriela Carvalho'),
    ('static/fotos/IMG_5458.jpg', 400, 300, 'Planos de Saúde'),
    ('static/fotos/IMG_5592.jpg', 400, 300, 'Planos Odontológicos'),
    ('static/fotos/Imagem-do-WhatsApp-de-2025-11-12-(s)-22.03.06_6aa551c0.jpg', 400, 300, 'Seguro de Vida'),
    ('static/fotos/Imagem-do-WhatsApp-de-2025-11-12-(s)-22.03.07_2cb0a543.jpg', 400, 300, 'Seguro Auto'),
    ('static/fotos/Post-de-Instagram-aseguradora-fotogrfico-azul.png', 500, 600, 'Transparência Seguros'),
]

for filepath, width, height, text in placeholders:
    if not os.path.exists(filepath):
        create_placeholder(filepath, width, height, text)
        print(f"📸 Placeholder criada: {filepath}")
    else:
        print(f"✅ Arquivo já existe: {filepath}")

print("\n✅ Todos os placeholders foram processados!")