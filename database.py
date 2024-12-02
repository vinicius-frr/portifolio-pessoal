from peewee import MySQLDatabase, Model, CharField,  TextField, ForeignKeyField

# Configuração da conexão com o banco de dados
db = MySQLDatabase(
    'defaultdb',  # Nome do banco de dados
    user='avnadmin',  # Usuário
    password='AVNS_LRL-sCkJNHfx9FAaUXq',  # Senha
    host='portifolio-viniciusfrr7.j.aivencloud.com',  # Endereço do servidor
    port=10276  # Porta
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
    with db.connection_context():
        db.create_tables([Info, Projeto, Curriculo, Contato, Usuario])
        