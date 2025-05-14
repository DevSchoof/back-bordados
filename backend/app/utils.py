import re
import requests


def convert_google_drive_link(url):
    """Converte link do Google Drive para link direto de imagem"""
    # Padrão para extrair o ID do arquivo
    pattern = r'https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/uc?export=view&id={file_id}"
    return url  # Retorna o original se não for um link do Drive




def validate_product_data(data):
    """Validação básica dos dados do produto"""
    errors = {}
    if not data.get('name'):
        errors['name'] = 'Nome é obrigatório'
    if not data.get('description'):
        errors['description'] = 'Descrição é obrigatória'
    return errors


def is_valid_image_url(url):
    try:
        response = requests.head(url, timeout=5)
        return response.headers['Content-Type'].startswith('image/')
    except:
        return False