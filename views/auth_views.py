from app import app
from flask import redirect, url_for, request, render_template
from flask_login import current_user, login_user, logout_user, LoginManager
from usuario import Usuario
from database import Info

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard', user_id=current_user.id))

    # Verifica se já existe pelo menos uma conta no sistema
    conta_existente = Usuario.select().exists()

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuario.find_by_email(email)

        if usuario and usuario.check_password(senha):
            login_user(usuario)
            return redirect(url_for('dashboard', user_id=current_user.id))

        error = 'Credenciais incorretas. Tente novamente.'
        return render_template('login.html', error=error, conta_existente=conta_existente)

    return render_template('login.html', conta_existente=conta_existente)

@app.route('/logout')
def logout():
    # session.pop('usuario_logado', None)  # Remove o usuário da sessão
    logout_user()  # Faz o logout do usuário
    return redirect(url_for('login'))  # Redireciona para a página inicial

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    # Verifica se já existe uma conta criada
    if Usuario.select().count() > 0:
        return redirect(url_for('login'))  # Se uma conta já existir, redireciona para login

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']

        # Validações
        if not nome or not email or not senha:
            error = 'Todos os campos são obrigatórios.'
            return render_template('sign_up.html', error=error)

        if senha != confirmar_senha:
            error = 'As senhas não coincidem.'
            return render_template('sign_up.html', error=error)

        # Verifica se o usuário já existe
        if Usuario.get_or_none(Usuario.email == email):
            error = 'Esse email já está em uso. Tente outro.'
            return render_template('sign_up.html', error=error)

        # Cria o usuário com hashing seguro na senha
        usuario = Usuario(nome=nome, email=email)
        usuario.set_password(senha)  # Deve implementar hashing, como bcrypt
        usuario.save()

        # Cria automaticamente informações básicas para o portfólio do usuário
        Info.create(
            nome=nome,
            bio="",
            usuario=usuario  # Relaciona com o usuário recém-criado
        )

        return redirect(url_for('login'))  # Redireciona para login após criação

    return render_template('sign_up.html')