from flask import abort
import validators

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)

from api.utils.generate_password import generate_password
from api.models.models import Fornecedor, db
from api.utils.calculate_subscription_time import (
    calculate_subscrption_time,
    verify_subscrption_time,
)


def create_fornecedor(data: dict) -> Fornecedor | bool:
    if not validators.email(data["email"]):
        return abort(400, "E-mail inválido")

    old_fornecedor = get_fornecedor_by_email(data["email"])

    if not old_fornecedor:
        try:
            new_fornecedor = Fornecedor(
                email=data["email"],
                nome_completo=data["nome_completo"],
                telefone=data["telefone"],
                senha=data["senha"],
                loja=data.get("loja"),
                endereco=data.get("endereco"),
                imagem=data.get("imagem"),
            )
            db.session.add(new_fornecedor)
            db.session.commit()
            return new_fornecedor
        except KeyError:
            return abort(
                400,
                "Verifique os campos exigidos no corpo da requisição e tente novamente",
            )

    return False


def get_all_fornecedores() -> list:
    return Fornecedor.query.all()


def fornecedor_login(data: dict) -> bool | dict:
    email = data["email"]
    password = data["senha"]
    fornecedor = get_fornecedor_by_email(email)

    if fornecedor:
        if not fornecedor.esta_activa:
            return abort(
                401,
                "A sua conta não está activa, verifique a sua caixa de e-mail para activar",
            )
        if fornecedor.verify_password(password):
            return {
                "access": create_access_token(identity=fornecedor.id),
                "refresh": create_refresh_token(identity=fornecedor.id),
            }

    return False


def get_fornecedor():
    fornecedor_id = get_jwt_identity()
    fornecedor = Fornecedor.query.filter_by(id=fornecedor_id).first()
    return fornecedor


def get_fornecedor_by_email(email: str) -> Fornecedor | None:
    return Fornecedor.query.filter_by(email=email).first()


def renovar_subscricao(email):
    fornecedor = get_fornecedor_by_email(email)

    if fornecedor:
        if not fornecedor.esta_activa:
            return abort(
                401,
                "A sua conta não está activa, verifique a sua caixa de e-mail para activar",
            )
        if not fornecedor.subscription_status:
            fornecedor.subscription_end_date = calculate_subscrption_time(1)
            fornecedor.subscription_status = True
            db.session.commit()

            return str(fornecedor.subscription_end_date), 200

        return abort(400, "A subscrição já está activa")

    return abort(404, "Usuário não encontrado")


def cancelar_subscricao(email):
    fornecedor = get_fornecedor_by_email(email)

    if fornecedor:
        if not fornecedor.esta_activa:
            return abort(
                401,
                "A sua conta não está activa, verifique a sua caixa de e-mail para activar",
            )
        if fornecedor.subscription_status:
            fornecedor.subscription_status = False
            db.session.commit()

            return "Subscrição cancelada com sucesso", 200

        return abort(400, "A subscrição não está activa")

    return abort(404, "Usuário não encontrado")


def activate_fornecedor(email: str):
    fornecedor = get_fornecedor_by_email(email)
    fornecedor.esta_activa = True
    db.session.commit()


def fornecedor_password_recovery(data: dict) -> Fornecedor | bool:
    fornecedor = get_fornecedor_by_email(data["email"])
    senha = generate_password()
    fornecedor.senha = fornecedor.hash_senha(senha)
    db.session.commit()
    return fornecedor, senha


def get_all_compras(email: str):
    return Fornecedor.query.filter_by(email=email).first().vendas
