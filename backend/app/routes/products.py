from flask import Blueprint, request, jsonify
from ..models import Product, db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from ..utils import is_valid_image_url

products_bp = Blueprint('products', __name__)

# CREATE - Criar novo produto
@products_bp.route('/products', methods=['POST'])
def create_product():
    try:
        data = request.get_json()
        
    if not is_valid_image_url(data['image_url']):
        return jsonify({"error": "URL de imagem inválida"}), 400



        # Campos obrigatórios
        required_fields = ['name', 'description', 'image_url', 'categoria']
        if not all(field in data for field in required_fields):
            return jsonify({
                "error": "Dados incompletos",
                "required_fields": required_fields,
                "received_data": list(data.keys())
            }), 400
            
        now = datetime.utcnow()
        new_product = Product(
            name=data['name'],
            description=data['description'],
            alt_description=data.get('alt_description', ''),
            image_url=data['image_url'],
            categoria=data['categoria'],
            created_at=now,
            updated_at=now  # Inicializa com a mesma data de criação
        )
        
        db.session.add(new_product)
        db.session.commit()
        
        return jsonify({
            "message": "Produto criado com sucesso!",
            "id": new_product.id,
            "created_at": new_product.created_at.isoformat(),
            "updated_at": new_product.updated_at.isoformat()
        }), 201
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Erro no banco de dados", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Erro inesperado", "details": str(e)}), 500

# READ - Listar todos produtos (ordenados por atualização recente)
@products_bp.route('/products', methods=['GET'])
def get_products():
    try:
        products = Product.query.order_by(Product.updated_at.desc()).all()
        products_list = [{
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'alt_description': p.alt_description,
            'image_url': p.image_url,
            'categoria': p.categoria,
            'created_at': p.created_at.isoformat(),
            'updated_at': p.updated_at.isoformat()
        } for p in products]
        
        return jsonify({
            "count": len(products_list),
            "products": products_list
        })
        
    except SQLAlchemyError as e:
        return jsonify({"error": "Erro ao acessar o banco de dados", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Erro inesperado", "details": str(e)}), 500

# READ - Obter um produto específico
@products_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    try:
        product = Product.query.get(id)
        
        if not product:
            return jsonify({"error": "Produto não encontrado", "product_id": id}), 404
            
        return jsonify({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'alt_description': product.alt_description,
            'image_url': product.image_url,
            'categoria': product.categoria,
            'created_at': product.created_at.isoformat(),
            'updated_at': product.updated_at.isoformat()
        })
        
    except SQLAlchemyError as e:
        return jsonify({"error": "Erro no banco de dados", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Erro inesperado", "details": str(e)}), 500

# UPDATE - Atualizar produto
@products_bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    try:
        product = Product.query.get(id)
        if not product:
            return jsonify({"error": "Produto não encontrado", "product_id": id}), 404
            
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Nenhum dado fornecido para atualização"}), 400
            
        # Atualiza os campos
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'alt_description' in data:
            product.alt_description = data['alt_description']
        if 'image_url' in data:
            product.image_url = data['image_url']
        if 'categoria' in data:
            product.categoria = data['categoria']
        
        # Atualiza o timestamp de modificação
        product.updated_at = datetime.utcnow()
        
        db.session.commit()
        return jsonify({
            "message": "Produto atualizado com sucesso!",
            "product_id": id,
            "updated_at": product.updated_at.isoformat(),
            "updated_fields": list(data.keys())
        })
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Erro no banco de dados", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Erro inesperado", "details": str(e)}), 500

# DELETE - Remover produto
@products_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        product = Product.query.get(id)
        if not product:
            return jsonify({"error": "Produto não encontrado", "product_id": id}), 404
            
        deleted_data = {
            'name': product.name,
            'categoria': product.categoria,
            'created_at': product.created_at.isoformat(),
            'updated_at': product.updated_at.isoformat()
        }
        
        db.session.delete(product)
        db.session.commit()
        return jsonify({
            "message": "Produto deletado com sucesso!",
            "product_id": id,
            "deleted_product": deleted_data
        }), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Erro no banco de dados", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Erro inesperado", "details": str(e)}), 500