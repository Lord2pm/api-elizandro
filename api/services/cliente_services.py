from flask import abort
import validators

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)

from api.models.models import Cliente, db
from api.utils.calculate_subscription_time import calculate_subscrption_time
from api.utils.generate_password import generate_password


def create_cliente(data: dict) -> Cliente | bool:
    if not validators.email(data["email"]):
        return abort(400, "E-mail inválido")

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
        if not cliente.esta_activa:
            return abort(
                401,
                "A sua conta não está activa, verifique a sua caixa de e-mail para activar",
            )
        if cliente.verify_password(password):
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


def renovar_subscricao(email):
    cliente = get_cliente_by_email(email)

    if cliente:
        if not cliente.esta_activa:
            return abort(
                401,
                "A sua conta não está activa, verifique a sua caixa de e-mail para activar",
            )
        if not cliente.subscription_status:
            cliente.subscription_end_date = calculate_subscrption_time(1)
            cliente.subscription_status = True
            db.session.commit()

            return str(cliente.subscription_end_date), 200

        return abort(400, "A subscrição já está activa")

    return abort(404, "Usuário não encontrado")


def cancelar_subscricao(email):
    cliente = get_cliente_by_email(email)

    if cliente:
        if not cliente.esta_activa:
            return abort(
                401,
                "A sua conta não está activa, verifique a sua caixa de e-mail para activar",
            )
        if cliente.subscription_status:
            cliente.subscription_status = False
            db.session.commit()

            return "Subscrição cancelada com sucesso", 200

        return abort(400, "A subscrição não está activa")

    return abort(404, "Usuário não encontrado")


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
