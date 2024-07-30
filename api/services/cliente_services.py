from flask import abort

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)

from api.models.models import Cliente, db
from api.utils.generate_password import generate_password


def create_cliente(data: dict) -> Cliente | bool:
    old_cliente = get_cliente_by_email(data["email"])

    if not old_cliente:
        try:
            new_cliente = Cliente(
                email=data["email"],
                nome_completo=data["nome_completo"],
                telefone=data["telefone"],
                senha=data["senha"],
                endereco=data.get("endereco"),
                imagem=data.get("imagem"),
            )
            db.session.add(new_cliente)
            db.session.commit()
            return new_cliente
        except KeyError:
            return abort(
                400,
                "Verifique os campos exigidos no corpo da requisição e tente novamente",
            )

    return False


def get_all_clientes() -> list:
    return Cliente.query.all()


def cliente_login(data: dict) -> bool | dict:
    email = data["email"]
    password = data["senha"]
    cliente = get_cliente_by_email(email)

    if cliente:
        if cliente.verify_password(password) and cliente.esta_activa:
            return {
                "access": create_access_token(identity=cliente.id),
                "refresh": create_refresh_token(identity=cliente.id),
            }

    return False


def get_cliente():
    cliente_id = get_jwt_identity()
    cliente = Cliente.query.filter_by(id=cliente_id).first()
    return cliente


def get_cliente_by_email(email: str) -> Cliente | None:
    return Cliente.query.filter_by(email=email).first()


def activate_cliente(email: str):
    cliente = get_cliente_by_email(email)
    cliente.esta_activa = True
    db.session.commit()


def cliente_password_recovery(data: dict) -> Cliente | bool:
    cliente = get_cliente_by_email(data["email"])
    senha = generate_password()
    cliente.senha = cliente.hash_senha(senha)
    db.session.commit()
    return cliente, senha


def get_all_compras(email: str):
    return Cliente.query.filter_by(email=email).first().vendas
