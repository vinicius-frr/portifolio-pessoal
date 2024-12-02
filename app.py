from flask import Flask
from flask_login import LoginManager
from database import create_tables
from usuario import Usuario
import os

# Inicializando o aplicativo Flask
app = Flask(__name__)
# Tenta recuperar a chave secreta do ambiente, se não existir, gera uma chave segura
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24).hex())

# Configuração de uploads
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Inicializando o gerenciador de login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Rota de redirecionamento ao tentar acessar áreas protegidas

@login_manager.user_loader
def load_user(user_id):
    return Usuario.get_or_none(Usuario.id == user_id)

# Criar tabelas ao iniciar
create_tables()

# Importa as rotas (views) após as inicializações para evitar referências circulares
from views import *

if __name__ == "__main__":
    app.run(debug=True)
