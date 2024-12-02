from peewee import MySQLDatabase, Model, CharField,  TextField, ForeignKeyField
import os

# Configuração da conexão com o banco de dados
db = MySQLDatabase(
    os.getenv("DB_NAME"),  # Nome do banco de dados
    user=os.getenv("DB_USER"),  # Usuário
    password=os.getenv("DB_PASSWORD"),  # Senha
    host=os.getenv("DB_HOST"),  # Endereço do servidor
    port=int(os.getenv("DB_PORT"))  # Porta
)
from usuario import Usuario

# Modelo de informações pessoais
class Info(Model):
    nome = CharField()
    bio = TextField()
    foto = CharField(max_length=255, null=True)
    usuario = ForeignKeyField(Usuario, backref='info')  # Adiciona o relacionamento com o usuário

    class Meta:
        database = db


# Modelo de projetos
class Projeto(Model):
    nome = CharField()
    descricao = TextField()
    usuario = ForeignKeyField(Usuario, backref='projetos')  # Adiciona o relacionamento com o usuário

    class Meta:
        database = db


# Modelo de currículo
class Curriculo(Model):
    experiencia = TextField()
    educacao = TextField()
    usuario = ForeignKeyField(Usuario, backref='curriculos')  # Relaciona com o usuário

    class Meta:
        database = db


# Modelo de contato
class Contato(Model):
    email = CharField()
    telefone = CharField()
    usuario = ForeignKeyField(Usuario, backref='contatos')  # Relaciona com o usuário

    class Meta:
        database = db


def create_tables():
    try:
        with db.connection_context():
            db.create_tables([Info, Projeto, Curriculo, Contato, Usuario])
    except Exception as e:
        print("Erro ao criar as tabelas:", e)
        