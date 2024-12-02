from flask_login import UserMixin
from peewee import Model, AutoField, CharField
from database import db
import bcrypt

class Usuario(UserMixin, Model):
    id = AutoField()  # Chave primária
    nome = CharField(max_length=100)
    email = CharField(max_length=100, unique=True)
    senha = CharField(max_length=255)  # Armazena o hash da senha

    class Meta:
        database = db  # Define qual banco de dados usar

    def __str__(self):
        return f"Usuario(id={self.id}, nome={self.nome}, email={self.email})"

    @classmethod
    def get_by_id(cls, user_id):
        """Busca um usuário pelo ID."""
        try:
            return cls.get(cls.id == user_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def find_by_email(cls, email):
        """Busca um usuário pelo email."""
        try:
            return cls.get(cls.email == email)
        except cls.DoesNotExist:
            return None

    def set_password(self, password):
        """Define a senha do usuário com hashing seguro."""
        self.senha = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.save()

    def check_password(self, password):
        """Verifica se a senha corresponde ao hash armazenado."""
        return bcrypt.checkpw(password.encode('utf-8'), self.senha.encode('utf-8'))
