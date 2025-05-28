# Importações principais do Flask e extensões
from flask import Flask, redirect, url_for, request, flash
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user, login_user
from .extensions import db, jwt, cors
from .models import Product, User
from .config import DevelopmentConfig
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import inspect
import os
from .routes.products import products_bp

# Configuração do gerenciador de login
login_manager = LoginManager()


class SecureModelView(ModelView):
    """View protegida que requer autenticação e privilégios de admin"""
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

class MyAdminIndexView(AdminIndexView):
    """View personalizada para a página inicial do admin"""
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    
    # Configuração da chave secreta (ESSENCIAL para sessões)
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'uma-chave-secreta-muito-segura-aqui')
    
    # Outras configurações
    app.config.from_object(config)
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    
    # Inicialização de extensões
    db.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # inicialização dos blueprints
    app.register_blueprint(products_bp)
    
    # Configuração do user_loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Configuração do painel administrativo
    def setup_admin(app):
        admin = Admin(
            app,
            name='Bordados Admin',
            template_mode='bootstrap3',
            index_view=MyAdminIndexView(name='Home')
        )
        admin.add_view(SecureModelView(Product, db.session, name='Produtos'))
        admin.add_view(SecureModelView(User, db.session, name='Usuários'))
    
    # Rota de login simples para Flask-Admin
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            
            if user and check_password_hash(user.password, password):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('admin.index'))
            flash('Credenciais inválidas')
        
        return '''
        <form method="post">
            <h2>Login Admin</h2>
            <div>
                <label>Usuário:</label>
                <input type="text" name="username" required>
            </div>
            <div>
                <label>Senha:</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit">Entrar</button>
        </form>
        '''
    
    # Criar usuário admin padrão
    def create_default_admin():
        with app.app_context():
            inspector = inspect(db.engine)
            if 'user' in inspector.get_table_names():
                if not User.query.filter_by(username='admin').first():
                    admin_user = User(
                        username='admin',
                        password=generate_password_hash('admin123'),
                        is_admin=True
                    )
                    db.session.add(admin_user)
                    db.session.commit()
    
    # Inicialização
    with app.app_context():
        db.create_all()
        setup_admin(app)
        create_default_admin()
    
    return app