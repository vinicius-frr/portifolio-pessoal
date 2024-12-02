from app import app
from flask import request, redirect, url_for, render_template
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from database import *
from peewee import DoesNotExist

UPLOAD_FOLDER = 'static/uploads'  # Diretório onde as fotos serão armazenadas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Função para verificar se a extensão do arquivo é permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/dashboard/<int:user_id>', methods=['GET', 'POST'])
@login_required  # Garante que apenas usuários autenticados possam acessar o dashboard
def dashboard(user_id):
    # Verifica se o ID do usuário na URL corresponde ao usuário logado
    if current_user.id != user_id:
        return redirect(url_for('dashboard', user_id=current_user.id))  # Redireciona para o dashboard do usuário logado

    # Recupera as informações pessoais, currículo e contato do usuário logado
    try:
        info_usuario = Info.get(Info.usuario == current_user)  # Recupera o portfólio do usuário logado
    except DoesNotExist:
        info_usuario = None  # Se não existir, não criamos nada (você pode criar um novo se necessário)

    try:
        curriculo_usuario = Curriculo.get(Curriculo.usuario == current_user)  # Recupera o currículo
    except DoesNotExist:
        curriculo_usuario = None  # Se não existir, criamos mais abaixo se necessário

    # Tentando pegar o contato, caso não exista, trata a exceção
    try:
        contato_usuario = Contato.get(Contato.usuario == current_user)  # Recupera o contato
    except DoesNotExist:
        contato_usuario = None  # Se não existir, criamos mais abaixo se necessário

    if request.method == 'POST':
        # Verifica se o formulário contém um arquivo de foto
        if 'foto' in request.files:
            foto = request.files['foto']
            
            if foto and allowed_file(foto.filename):
                # Salva a foto no diretório 'uploads' com um nome seguro
                filename = secure_filename(foto.filename)
                foto.save(os.path.join(UPLOAD_FOLDER, filename))

                # Atualiza o campo 'foto' no banco de dados
                if info_usuario:
                    info_usuario.foto = filename
                    info_usuario.save()

        # Atualiza ou cria o projeto
        if 'adicionar_projeto' in request.form:
            nome_projeto = request.form['nome_projeto']
            descricao_projeto = request.form['descricao_projeto']
            adicionar_projeto(nome_projeto, descricao_projeto, current_user.id)

        # Verifica qual botão foi pressionado e executa a atualização
        if 'editar_info' in request.form:
            # Atualizando informações pessoais
            if info_usuario:
                info_usuario.nome = request.form['nome']
                info_usuario.bio = request.form['bio']
                info_usuario.save()

        if 'editar_curriculo' in request.form:
            # Atualizando ou criando currículo
            if curriculo_usuario:
                curriculo_usuario.experiencia = request.form['experiencia']
                curriculo_usuario.educacao = request.form['educacao']
                curriculo_usuario.save()
            else:
                # Se o currículo não existir, criamos um novo
                curriculo_usuario = Curriculo.create(
                    usuario=current_user,
                    experiencia=request.form['experiencia'],
                    educacao=request.form['educacao']
                )

        if 'editar_contato' in request.form:
            # Atualizando ou criando contato
            if contato_usuario:
                contato_usuario.email = request.form['email']
                contato_usuario.telefone = request.form['telefone']
                contato_usuario.save()
            else:
                # Se o contato não existir, criamos um novo
                contato_usuario = Contato.create(
                    usuario=current_user,
                    email=request.form['email'],
                    telefone=request.form['telefone']
                )

        # Redireciona para o dashboard após salvar
        return redirect(url_for('dashboard', user_id=current_user.id))

    # Recuperando a lista de projetos para exibir no dashboard
    projetos = Projeto.select()

    return render_template('dashboard.html', info=info_usuario, curriculo=curriculo_usuario, contato=contato_usuario, projetos=projetos)


def adicionar_projeto(nome_projeto, descricao_projeto, usuario_id):
    try:
        # Verifica se o usuário existe
        usuario = Usuario.get(Usuario.id == usuario_id)
        
        # Cria o projeto associado ao usuário
        projeto = Projeto.create(
            nome=nome_projeto,
            descricao=descricao_projeto,
            usuario=usuario  # Relaciona o projeto com o usuário
        )
        return projeto  # Retorna o projeto criado

    except Usuario.DoesNotExist:
        # Caso o usuário não exista, levanta um erro
        raise ValueError(f"Usuário com ID {usuario_id} não encontrado.")


@app.route('/editar_projeto/<int:projeto_id>', methods=['GET', 'POST'])
def editar_projeto(projeto_id):
    # Busca o projeto
    try:
        projeto = Projeto.get(Projeto.id == projeto_id)
    except DoesNotExist:
        return "Projeto não encontrado ou você não tem permissão para editá-lo", 403
    
    # projeto = Projeto.get(Projeto.id == projeto_id)
    
    if request.method == 'POST':
        # Atualiza o projeto
        projeto.nome = request.form['nome_projeto']
        projeto.descricao = request.form['descricao_projeto']
        projeto.save()  # Salva as alterações no banco
        
        return redirect(url_for('dashboard', user_id=current_user.id))

    return render_template('editar_projeto.html', projeto=projeto)


@app.route('/deletar_projeto/<int:id>', methods=['POST'])
def deletar_projeto(id):
    try:
        db.connect()  # Conecta ao banco de dados
        projeto = Projeto.get(Projeto.id == id)  # Recupera o projeto a ser deletado
        projeto.delete_instance()  # Deleta o projeto do banco de dados
        return redirect(url_for('dashboard', user_id=current_user.id))  # Redireciona de volta ao dashboard após deletar
    finally:
        db.close()  # Fecha a conexão com o banco de dados