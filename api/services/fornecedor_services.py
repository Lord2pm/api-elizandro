from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)

from api.utils.generate_password import generate_password
from api.models.models import Fornecedor, db


def create_fornecedor(data: dict) -> Fornecedor | bool:
    old_fornecedor = get_fornecedor_by_email(data["email"])

    if not old_fornecedor:
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

    return False


def get_all_fornecedores() -> list:
    return Fornecedor.query.all()


def fornecedor_login(data: dict) -> bool | dict:
    email = data["email"]
    password = data["senha"]
    fornecedor = get_fornecedor_by_email(email)

    if fornecedor:
        if fornecedor.verify_password(password) and fornecedor.esta_activa:
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