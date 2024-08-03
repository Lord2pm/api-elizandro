from flask import abort

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)
import validators

from api.utils.generate_password import generate_password
from api.models.models import Admin, Fornecedor, Cliente, Venda, Produto, db


def create_admin(data: dict) -> Admin | bool:
    if not validators.email(data["email"]):
        return abort(400, "E-mail inválido")

    old_admin = get_admin_by_email(data["email"])

    if not old_admin:
        try:
            new_admin = Admin(email=data["email"], senha=data["senha"])
            db.session.add(new_admin)
            db.session.commit()
            return new_admin
        except KeyError:
            return abort(
                400,
                "Verifique os campos exigidos no corpo da requisição e tente novamente",
            )

    return False


def admin_login(data: dict) -> bool | dict:
    email = data["email"]
    password = data["senha"]
    admin = get_admin_by_email(email)

    if admin:
        if admin.verify_password(password):
            return {
                "access": create_access_token(identity=admin.id),
                "refresh": create_refresh_token(identity=admin.id),
            }

    return False


def get_all_admins():
    return Admin.query.all()


def get_qtd_fornecedores():
    return len(Fornecedor.query.all())


def get_qtd_clientes():
    return len(Cliente.query.all())


def get_qtd_users():
    return get_qtd_clientes() + get_qtd_fornecedores()


def get_qtd_users_with_active_subscription():
    return len(Fornecedor.query.filter_by(subscription_status=True).all()) + len(
        Cliente.query.filter_by(subscription_status=True).all()
    )


def get_qtd_produtos():
    return len(Produto.query.all())


def get_qtd_vendas():
    return len(Venda.query.all())


def get_admin(id):
    admin = Admin.query.filter_by(id=id).first()
    return admin


def get_admin_by_email(email: str) -> Admin | None:
    return Admin.query.filter_by(email=email).first()


def admin_password_recovery(data: dict) -> Admin | bool:
    admin = get_admin_by_email(data["email"])
    senha = generate_password()
    admin.senha = admin.hash_senha(senha)
    db.session.commit()
    return admin, senha
