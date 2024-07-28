import os
from flask import url_for
from werkzeug.utils import secure_filename

from api.models.models import Produto, Fornecedor, db


UPLOAD_FOLDER = "img/"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        return url_for("static", filename=filename, _external=True)
    return None


def get_all_produtos():
    return Produto.query.all()


def get_produto_by_id(id):
    return Produto.query.get_or_404(id)


def create_produto(data):
    produto = Produto(
        nome=data["nome"],
        preco=data["preco"],
        qtd_stock=data.get("qtd_stock"),
        vendedor_id=data["vendedor_id"],
    )
    db.session.add(produto)
    db.session.commit()
    return produto, 201


def update_produto(id, data):
    produto = get_produto_by_id(id)
    produto.nome = data.get("nome", produto.nome)
    produto.preco = data.get("preco", produto.preco)
    produto.qtd_stock = data.get("qtd_stock", produto.qtd_stock)
    db.session.commit()
    return produto


def delete_produto(id):
    produto = get_produto_by_id(id)
    db.session.delete(produto)
    db.session.commit()
    return "", 204


def get_produtos_by_fornecedor_email(email):
    fornecedor = Fornecedor.query.filter_by(email=email).first()
    if not fornecedor:
        return {"message": "Fornecedor não encontrado"}, 404
    return fornecedor.produtos
