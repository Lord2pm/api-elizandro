from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


db = SQLAlchemy()


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    telefone = db.Column(db.String(20), nullable=False)
    nome_completo = db.Column(db.String(100))
    senha = db.Column(db.Text)
    imagem = db.Column(db.String(200), nullable=True)
    tipo_conta = db.Column(
        db.String(20), nullable=False, default="Cliente"
    )  # Fornecedor | Cliente
    endereco = db.Column(db.String(200), nullable=True)
    esta_activa = db.Column(db.Boolean, default=False)

    vendas = db.relationship("Venda", backref="cliente", lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(
        self,
        email: str,
        nome_completo: str,
        telefone: str,
        senha: str,
        endereco: str,
        imagem: str,
    ) -> None:
        self.email = email
        self.nome_completo = nome_completo
        self.telefone = telefone
        self.senha = self.hash_senha(senha)
        self.endereco = endereco
        self.imagem = imagem

    def hash_senha(self, senha):
        return generate_password_hash(senha)

    def verify_password(self, senha: str) -> bool:
        return check_password_hash(self.senha, senha)


class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    telefone = db.Column(db.String(20), nullable=False)
    nome_completo = db.Column(db.String(100))
    senha = db.Column(db.Text)
    imagem = db.Column(db.String(200), nullable=True)
    tipo_conta = db.Column(
        db.String(20), nullable=False, default="Fornecedor"
    )  # Fornecedor | Cliente
    loja = db.Column(db.String(100), nullable=True)
    endereco = db.Column(db.String(200), nullable=True)
    esta_activa = db.Column(db.Boolean, default=False)
    produtos = db.relationship("Produto", backref="fornecedor", lazy=True)
    vendas = db.relationship("Venda", backref="fornecedor", lazy=True)

    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(
        self,
        email: str,
        nome_completo: str,
        telefone: str,
        senha: str,
        loja: str,
        endereco: str,
        imagem: str,
    ) -> None:
        self.email = email
        self.nome_completo = nome_completo
        self.telefone = telefone
        self.senha = self.hash_senha(senha)
        self.loja = loja
        self.endereco = endereco
        self.imagem = imagem

    def hash_senha(self, senha):
        return generate_password_hash(senha)

    def verify_password(self, senha: str) -> bool:
        return check_password_hash(self.senha, senha)


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    qtd_stock = db.Column(db.Integer)
    imagem = db.Column(db.String(200), nullable=True)
    vendedor_id = db.Column(db.Integer, db.ForeignKey("fornecedor.id"), nullable=False)
    vendas = db.relationship("Venda", backref="produto", lazy=True)

    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())


class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    fornecedor_id = db.Column(
        db.Integer, db.ForeignKey("fornecedor.id"), nullable=False
    )

    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
