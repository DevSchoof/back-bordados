from backend.app import create_app
from backend.app.models import db, Product, User
from werkzeug.security import generate_password_hash

def recreate_database():
    app = create_app()
    with app.app_context():
        # Remove todas as tabelas existentes
        db.drop_all()
        
        # Cria todas as tabelas com as novas definições
        db.create_all()
        
        # Adiciona usuário admin se não existir
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                password=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Banco de dados recriado com sucesso!")
            print("👤 Usuário admin criado: admin/admin123")

if __name__ == '__main__':
    recreate_database()