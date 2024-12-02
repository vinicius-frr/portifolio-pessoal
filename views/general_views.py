from flask import render_template
from database import Info, Curriculo, Contato, Projeto
from . import bp
from app import app
from database import db

@app.route("/")
def home():
    # Conectando ao banco de dados
    try:
        db.connect()

        # Recuperar as informações pessoais, currículo, contato e projetos do banco
        informacoes_pessoais = Info.select().first()  # Primeira entrada de informações pessoais
        curriculo = Curriculo.select().first()  # Primeiro currículo
        contato = Contato.select().first()  # Primeiro contato
        projetos = Projeto.select()  # Recuperando todos os projetos no banco

        # Verificar se as informações existem
        informacoes_pessoais = informacoes_pessoais if informacoes_pessoais else {}
        curriculo = curriculo if curriculo else {}
        contato = contato if contato else {}

        return render_template("index.html", 
                               informacoes_pessoais=informacoes_pessoais, 
                               curriculo=curriculo, 
                               contato=contato,
                               projetos=projetos)

    finally:
        db.close()  # Fechar a conexão com o banco de dados
